#!/usr/bin/env python3
"""Read exact Book Forge manuscript versions without owning task continuation."""
from __future__ import annotations

import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sys

MAX_MANUSCRIPT_BYTES = 2 * 1024 * 1024
MAX_PREVIEW_CHARS = 24000


def project_file(root: Path, project: Path, ref: str) -> Path:
    if not isinstance(ref, str) or not ref:
        raise ValueError('A manuscript reference is required.')
    path = (root / ref).resolve(strict=True)
    if not path.is_relative_to(project) or not path.is_file():
        raise ValueError('Review references must be files inside the selected book.')
    return path


def object_file(root: Path, project: Path, ref: str) -> dict:
    value = json.loads(project_file(root, project, ref).read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('The owner index must be a JSON object.')
    return value


def choice(items: list[dict], field: str, defaults: dict) -> dict:
    return {'state': 'input_required', 'reason': f'{field}_selection_required',
            'input_schema': {'type': 'object', 'required': [field], 'properties': {
                field: {'type': 'string', 'title': 'Book' if field == 'book_id' else 'Manuscript',
                        'enum': [item['read_input'][field] for item in items],
                        'enumNames': [item['title'] for item in items]}}},
            'input_defaults': defaults, 'data': {'items': items}}


def manuscript(root: Path, project: Path, ref: str) -> tuple[dict, str]:
    path = project_file(root, project, ref)
    if path.suffix.lower() not in {'.md', '.markdown'}:
        raise ValueError('Select the author-facing Markdown manuscript; proof editing stays in its professional application.')
    with path.open('rb') as handle:
        content = handle.read(MAX_MANUSCRIPT_BYTES + 1)
    if len(content) > MAX_MANUSCRIPT_BYTES:
        raise ValueError('Select one chapter for review when a manuscript exceeds 2 MiB.')
    body = content.decode('utf-8')
    headings = []
    fenced = False
    for number, line in enumerate(body.splitlines(), 1):
        if re.match(r'^\s*(`{3,}|~{3,})', line):
            fenced = not fenced
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line) if not fenced else None
        if heading:
            headings.append({'level': len(heading[1]), 'title': heading[2], 'line': number})
    normalized = path.relative_to(root).as_posix()
    return ({'artifact_ref': normalized, 'path': str(path),
             'sha256': 'sha256:' + hashlib.sha256(content).hexdigest(),
             'bytes': len(content), 'headings': headings,
             'preview': body[:MAX_PREVIEW_CHARS], 'preview_truncated': len(body) > MAX_PREVIEW_CHARS}, body)


def read_review(value: dict, workspace: str | None = None) -> dict:
    workspace = workspace or os.environ.get('OPL_PROFILE_WORKSPACE', '')
    if not workspace or not Path(workspace).is_absolute():
        return {'state': 'unavailable', 'reason': 'workspace_selection_required'}
    root = Path(workspace).resolve(strict=True)
    identity = value.get('work_item_identity') or {}
    if not isinstance(identity, dict):
        raise ValueError('work_item_identity must be an object.')
    if identity and (identity.get('identity_state') != 'resolved'
                     or identity.get('agent_id') != 'obf'
                     or identity.get('domain_id') != 'opl-bookforge'):
        raise ValueError('The selected work item must be a resolved Book Forge book.')
    book_id = identity.get('domain_work_item_id') or identity.get('work_item_id')
    if book_id and value.get('book_id') and value['book_id'] != book_id:
        raise ValueError('The selected book conflicts with the current work item.')
    book_id = book_id or value.get('book_id')
    inventory = object_file(root, root, 'workspace_index.json')
    projects = [p for p in inventory.get('projects', []) if isinstance(p, dict)]
    if book_id:
        projects = [p for p in projects if p.get('project_id') == book_id]
        if len(projects) != 1:
            raise ValueError('The selected book must have one workspace inventory entry.')
    elif len(projects) != 1:
        return choice([{'id': p['project_id'], 'title': p.get('title', p['project_id']),
                        'read_input': {'book_id': p['project_id']}}
                       for p in projects if p.get('project_id')], 'book_id', {})
    project_entry = projects[0]
    book_id = project_entry['project_id']
    project = (root / project_entry['project_root']).resolve(strict=True)
    if project == root or not project.is_relative_to(root) or not project.is_dir():
        raise ValueError('The registered book root must be inside the workspace.')
    for field, actual in [('workspace_path', root), ('work_item_root', project)]:
        if identity.get(field) and Path(identity[field]).resolve(strict=True) != actual:
            raise ValueError('The selected work-item paths conflict with the registered book.')
    selected = value.get('artifact_path')
    if not selected:
        index_path = project / 'control/opl/artifact_lifecycle/output_lifecycle.json'
        if not index_path.is_file():
            return {'state': 'input_required', 'reason': 'manuscript_selection_required',
                    'missing_fields': ['artifact_path'], 'input_defaults': {'book_id': book_id},
                    'data': {'items': [], 'book_id': book_id}}
        index = object_file(root, project, index_path.relative_to(root).as_posix())
        if (index.get('surface_kind') != 'opl_workspace_output_lifecycle'
                or index.get('project_id') != book_id
                or (root / index.get('project_root', '')).resolve() != project):
            raise ValueError('The artifact projection does not belong to the selected book.')
        refs = list(dict.fromkeys(item['ref'] for item in [*index.get('current_refs', []), *index.get('artifacts', [])]
                                 if isinstance(item, dict) and isinstance(item.get('ref'), str)
                                 and Path(item['ref']).suffix.lower() in {'.md', '.markdown'}))
        for ref in refs:
            project_file(root, project, ref)
        if len(refs) != 1:
            return choice([{'id': ref, 'title': Path(ref).name, 'artifact_ref': ref,
                            'read_input': {'book_id': book_id, 'artifact_path': ref}} for ref in refs],
                          'artifact_path', {'book_id': book_id})
        selected = refs[0]
    current, body = manuscript(root, project, selected)
    baseline, baseline_body = manuscript(root, project, value['baseline_path']) if value.get('baseline_path') else (None, None)
    sources = [current, *([baseline] if baseline else [])]
    revision = 'sha256:' + hashlib.sha256(json.dumps(
        [(source['artifact_ref'], source['sha256']) for source in sources], separators=(',', ':')).encode()).hexdigest()
    if value.get('revision') and value['revision'] != revision:
        return {'state': 'unavailable', 'reason': 'manuscript_revision_changed',
                'data': {'book_id': book_id, 'revision': revision, 'items': []}}
    reopen = {'book_id': book_id, 'artifact_path': current['artifact_ref'], 'revision': revision}
    if baseline:
        reopen['baseline_path'] = baseline['artifact_ref']
    diff = ''.join(difflib.unified_diff(baseline_body.splitlines(keepends=True), body.splitlines(keepends=True),
                                      fromfile=baseline['artifact_ref'], tofile=current['artifact_ref'])) if baseline else None
    review_context = {'artifact_refs': [source['artifact_ref'] for source in sources],
                      'artifact_hashes': [source['sha256'] for source in sources],
                      'source_refs': [source['artifact_ref'] for source in sources]}
    if identity:
        review_context['work_item_identity'] = identity
    item = {'id': current['artifact_ref'], 'title': Path(current['artifact_ref']).name,
            'summary': f"{len(current['headings'])} headings · exact manuscript review",
            'book_id': book_id, 'status': 'review_required', 'revision': revision,
            'read_input': reopen, 'current': current, 'baseline': baseline,
            'artifacts': [{'id': source['artifact_ref'], 'title': Path(source['artifact_ref']).name,
                           'artifact_ref': source['path'], 'sha256': source['sha256'], 'status': 'available'} for source in sources],
            'source_refs': review_context['source_refs'], 'review_context': review_context,
            'next_action': {'title': 'Return this review context to the current book task',
                            'summary': 'Use its current Framework action to submit the editorial decision; manuscript editing and publication acceptance remain with Book Forge.'}}
    if diff is not None:
        item['comparison'] = {'format': 'unified_diff', 'text': diff[:MAX_PREVIEW_CHARS],
                              'truncated': len(diff) > MAX_PREVIEW_CHARS}
    return {'state': 'ready', 'data': {'items': [item], 'book_id': book_id,
                                     'review_context': review_context, 'domain_quality_approved': False}}


def main() -> None:
    try:
        value = json.load(sys.stdin)
        if not isinstance(value, dict):
            raise ValueError('Review input must be an object.')
        result = read_review(value)
    except (OSError, ValueError, TypeError, KeyError) as error:
        result = {'state': 'unavailable', 'reason': 'book_review_unavailable', 'message': str(error)}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
