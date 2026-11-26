#!/usr/bin/env python3
"""Exercise owner manuscript reads through the shared contribution adapter."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('book_review', ROOT / 'runtime/native_helpers/bookforge_app_review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class BookReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='obf-review-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.book = self.root / 'projects/book-a'
        self.book.mkdir(parents=True)
        (self.root / 'projects/book-b').mkdir()
        (self.root / 'workspace_index.json').write_text(json.dumps({'projects': [
            {'project_id': 'book-a', 'project_root': 'projects/book-a'},
            {'project_id': 'book-b', 'project_root': 'projects/book-b'}]}))
        (self.book / 'current.md').write_text('# 小书稿\n\n## 第一章\n新论点。\n\n## 第二章\n证据。\n')
        (self.book / 'baseline.md').write_text('# 小书稿\n\n## 第一章\n旧论点。\n')
        (self.root / 'projects/book-b/other.md').write_text('# Other book\n')
        self.input = {'book_id': 'book-a', 'artifact_path': 'projects/book-a/current.md',
                      'baseline_path': 'projects/book-a/baseline.md'}

    def read(self, value=None):
        return review.read_review(value if value is not None else self.input, str(self.root))

    def test_exact_versions_comparison_and_reopen(self):
        first = self.read()['data']['items'][0]
        self.assertEqual(first['current']['headings'][2]['title'], '第二章')
        self.assertIn('+新论点。', first['comparison']['text'])
        self.assertIn('-旧论点。', first['comparison']['text'])
        self.assertIn('旧论点。', first['preview']['before'])
        self.assertIn('新论点。', first['preview']['after'])
        self.assertEqual(len(first['review_context']['artifact_hashes']), 2)
        reopened = self.read(first['read_input'])['data']['items'][0]
        self.assertEqual(first['revision'], reopened['revision'])
        (self.book / 'current.md').write_text('# Concurrent edit\n')
        self.assertEqual(self.read(first['read_input'])['reason'], 'manuscript_revision_changed')
        self.assertNotEqual(self.read()['data']['items'][0]['revision'], first['revision'])

    def test_foreign_book_and_symlink_refused(self):
        with self.assertRaisesRegex(ValueError, 'selected book'):
            self.read({**self.input, 'baseline_path': 'projects/book-b/other.md'})
        (self.book / 'escaped.md').symlink_to(self.root / 'projects/book-b/other.md')
        with self.assertRaisesRegex(ValueError, 'selected book'):
            self.read({**self.input, 'artifact_path': 'projects/book-a/escaped.md'})

    def test_work_item_identity_and_inventory_must_agree(self):
        identity = {'identity_state': 'resolved', 'agent_id': 'obf', 'domain_id': 'opl-bookforge',
                    'domain_work_item_id': 'book-a', 'workspace_path': str(self.root),
                    'work_item_root': str(self.book)}
        result = self.read({**self.input, 'work_item_identity': identity})
        self.assertEqual(result['data']['review_context']['work_item_identity'], identity)
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            self.read({**self.input, 'work_item_identity': {**identity, 'domain_work_item_id': 'book-b'}})
        with self.assertRaisesRegex(ValueError, 'resolved Book Forge'):
            self.read({**self.input, 'work_item_identity': {**identity, 'agent_id': 'rca'}})
        with self.assertRaisesRegex(ValueError, 'paths conflict'):
            self.read({**self.input, 'work_item_identity': {**identity, 'work_item_root': str(self.root / 'projects/book-b')}})

    def test_inventory_selects_exact_book_and_only_declared_artifacts(self):
        self.assertEqual(self.read({})['state'], 'input_required')
        self.assertEqual(self.read({'book_id': 'book-a'})['reason'], 'manuscript_selection_required')
        index = self.book / 'control/opl/artifact_lifecycle/output_lifecycle.json'
        index.parent.mkdir(parents=True)
        index.write_text(json.dumps({'surface_kind': 'opl_workspace_output_lifecycle',
            'project_id': 'book-a', 'project_root': 'projects/book-a',
            'artifacts': [{'ref': 'projects/book-a/current.md'},
                          {'ref': 'projects/book-a/not-produced.md', 'exists': False}]}))
        result = self.read({'book_id': 'book-a'})
        self.assertEqual(result['data']['items'][0]['id'], 'projects/book-a/current.md')
        self.assertEqual(result['data']['diagnostics'],
                         [{'artifact_ref': 'projects/book-a/not-produced.md', 'status': 'missing'}])
        index.write_text(index.read_text().replace('"project_id": "book-a"', '"project_id": "book-b"'))
        with self.assertRaisesRegex(ValueError, 'projection does not belong'):
            self.read({'book_id': 'book-a'})

    def test_preview_is_bounded_but_hash_tracks_full_bytes(self):
        (self.book / 'current.md').write_text('# Chapter\n' + 'x' * (review.MAX_PREVIEW_CHARS + 50))
        first = self.read()['data']['items'][0]
        self.assertTrue(first['current']['preview_truncated'])
        self.assertIn('仅包含各稿前 24000 字符', first['summary'])
        self.assertLessEqual(len(first['current']['preview']), review.MAX_PREVIEW_CHARS)
        with (self.book / 'current.md').open('a') as handle:
            handle.write('tail change')
        self.assertNotEqual(self.read()['data']['items'][0]['revision'], first['revision'])

    def test_v2_contribution_handler_reads_same_owner(self):
        manifest = json.loads((ROOT / 'opl-package.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['schema_version'], 'opl.package.v2')
        self.assertIn('obf.workspace.v1#review', [view['data_ref'] for view in manifest['ui']['declarative']['views']])
        handler = manifest['provides']['contribution_handler']
        self.assertEqual(handler['kind'], 'cli')
        self.assertEqual(handler['transport'], 'stdin_json_stdout_json')

        request = {
            'schema_version': 'opl-package-app-contribution-request.v1',
            'operation': 'read',
            'package_id': 'obf',
            'ref': 'obf.workspace.v1#review',
            'input': self.input,
        }
        before = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob('*') if path.is_file()}
        completed = subprocess.run(
            [sys.executable, str(ROOT / handler['argv'][1])],
            input=json.dumps(request),
            text=True,
            capture_output=True,
            env={**os.environ, 'OPL_PROFILE_WORKSPACE': str(self.root)},
            cwd=ROOT,
            check=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result['state'], 'ready')
        self.assertFalse(result['data']['domain_quality_approved'])
        self.assertEqual(result['data']['book_id'], 'book-a')

        status_completed = subprocess.run(
            [sys.executable, str(ROOT / handler['argv'][1])],
            input=json.dumps({**request, 'ref': 'obf.workspace.v1#status', 'input': {'book_id': 'book-a'}}),
            text=True,
            capture_output=True,
            env={**os.environ, 'OPL_PROFILE_WORKSPACE': str(self.root)},
            cwd=ROOT,
            check=True,
        )
        status_result = json.loads(status_completed.stdout)
        self.assertEqual(status_result['state'], 'ready')
        self.assertEqual(status_result['data']['items'][0]['id'], 'book-a')

        after = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob('*') if path.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
