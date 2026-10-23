import json
import sys
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


REPO = Path(__file__).resolve().parents[1]


def test_publication_bundle_contract() -> None:
    contract = json.loads((REPO / "contracts/publication_bundle_contract.json").read_text(encoding="utf-8"))
    assert (REPO / contract["entrypoint_ref"]).is_file()
    assert (REPO / contract["table_width_filter_ref"]).is_file()
    assert contract["owning_action"] == "materialize-book"
    assert contract["content_integrity"]["minimum_source_coverage"] == 0.985
    assert {"pandoc", "xelatex", "soffice", "pdftoppm", "pdftotext", "pdffonts"} <= set(contract["required_commands"])
    assert contract["artifact_role"] == "publication_bundle"
    assert contract["quality_boundary"]["fast_path_is_orchestration_only"] is True
    assert contract["quality_boundary"]["publication_bundle_is_final_export"] is False
    assert contract["required_outputs"] == ["docx", "pdf", "bundle_manifest"]
    assert {
        "source_sha256",
        "docx_sha256",
        "pdf_sha256",
        "source_coverage_docx",
        "source_coverage_pdf",
        "pdf_font_readback",
        "docx_rendered_page_refs",
        "pdf_rendered_page_refs",
    } <= set(contract["manifest_requirements"])


def test_extraction_integrity() -> None:
    sys.path.insert(0, str(REPO / "runtime/native_helpers"))
    from bookforge_publication_bundle import source_coverage, visible_ast_text, rendered_text_integrity, MIN_SOURCE_COVERAGE
    source = "研究甲 120例 AUC 0.92 研究乙 200例 AUC 0.85"
    reordered = "研究乙 200例 AUC 0.85\n研究甲 120例 AUC 0.92"
    assert source_coverage(source, reordered) == 1.0
    assert source_coverage(source, "研究甲 120例 AUC 0.92") < MIN_SOURCE_COVERAGE
    assert source_coverage("检查检查检查", "检查") == 1 / 3
    assert source_coverage("Ⅱ期研究", "II期研\n究") == 1.0
    # A complete DOCX XML body can still render with missing Chinese glyphs.
    damaged = rendered_text_integrity("研究对象与临床终点", "人人人中中中", title="章节", author="高峰", date="2026")
    assert damaged["source_coverage"] < MIN_SOURCE_COVERAGE
    assert not damaged["title_byline_date_present"]
    intact = rendered_text_integrity("研究对象与临床终点", "章节 高峰 2026 研究对象与临床终点", title="章节", author="高峰", date="2026")
    assert intact["source_coverage"] == 1.0 and intact["title_byline_date_present"]
    ast = [{"t": "Para", "c": [
        {"t": "Str", "c": "正文"},
        {"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "10.1/(23)"}], ["https://doi.org/10.1/(23)", ""]]},
        {"t": "Image", "c": [["", [], []], [{"t": "Str", "c": "替代文字"}], ["figure.svg", ""]]},
    ]}]
    visible = visible_ast_text(ast)
    assert "正文" in visible and "10.1/(23)" in visible
    assert "https" not in visible and "替代文字" not in visible and "figure.svg" not in visible


def test_caption_and_list_writer_behavior() -> None:
    if not shutil.which("pandoc"):
        raise RuntimeError("publication-bundle writer verification requires pandoc")
    source = """**表1 已给出的标题**

| 任务 | 数据 |
| --- | --- |
| 评估 | 资料 |

**图1 已给出的图题**

![图内替代文字](diagram.svg)

**普通加粗段落**

1. First reference.

2. Second reference.
"""
    command = ["pandoc", "--from=gfm+pipe_tables", "--lua-filter",
               str(REPO / "runtime/native_helpers/bookforge_table_widths.lua")]
    ast = json.loads(subprocess.run(command + ["-t", "json"], input=source,
                                   text=True, capture_output=True, check=True).stdout)
    blocks = ast["blocks"]
    assert [b["t"] for b in blocks] == ["Table", "Figure", "Para", "OrderedList"]
    assert "已给出的标题" in json.dumps(blocks[0]["c"][1], ensure_ascii=False)
    assert "已给出的图题" in json.dumps(blocks[1]["c"][1], ensure_ascii=False)
    assert "普通加粗段落" in json.dumps(blocks[2], ensure_ascii=False)
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "list.docx"
        subprocess.run(command + ["-t", "docx", "-o", str(target)],
                       input="1. First reference.\n\n2. Second reference.\n",
                       text=True, capture_output=True, check=True)
        with ZipFile(target) as archive:
            root = ET.fromstring(archive.read("word/document.xml"))
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs = root.findall("w:body/w:p", ns)
        assert len(paragraphs) == 2
        for paragraph in paragraphs:
            assert paragraph.find("w:pPr/w:numPr", ns) is not None
            assert paragraph.find("w:pPr/w:pStyle", ns).get(f"{{{ns['w']}}}val") == "ListParagraph"


def test_docx_table_rows_keep_content_and_headers() -> None:
    sys.path.insert(0, str(REPO / "runtime/native_helpers"))
    from bookforge_publication_bundle import docx_body_readback, keep_docx_table_rows
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "table.docx"
        subprocess.run(["pandoc", "-f", "gfm", "-t", "docx", "-o", str(target)],
                       input="| 研究 | 结果 |\n| --- | --- |\n| 甲 | 120例 |\n| 乙 | 200例 |\n",
                       text=True, capture_output=True, check=True)
        before = docx_body_readback(target)
        with ZipFile(target) as archive:
            other_parts = {name: archive.read(name) for name in archive.namelist() if name != "word/document.xml"}
        keep_docx_table_rows(target)
        keep_docx_table_rows(target)
        assert docx_body_readback(target) == before
        with ZipFile(target) as archive:
            root = ET.fromstring(archive.read("word/document.xml"))
            assert all(archive.read(name) == data for name, data in other_parts.items())
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        rows = root.findall(".//w:tr", ns)
        assert len(rows) == 3
        assert rows[0].find("w:trPr/w:tblHeader", ns) is not None
        for row in rows:
            settings = row.findall("w:trPr/w:cantSplit", ns)
            assert len(settings) == 1 and settings[0].get(f"{{{ns['w']}}}val") == "1"


def test_default_resources_and_chinese_byline() -> None:
    from_ref = REPO / "runtime/native_helpers/pdf_profiles/bookforge-zh-a4-publication.json"
    profile = json.loads(from_ref.read_text(encoding="utf-8"))
    reference = from_ref.parent / profile["word_reference_doc"]
    assert reference.is_file()
    for header in profile["include_in_header"]:
        assert (from_ref.parent / header).is_file()
    with ZipFile(reference) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        styles = ET.fromstring(archive.read("word/styles.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    size = document.find(".//w:sectPr/w:pgSz", ns)
    assert abs(int(size.get(f"{{{ns['w']}}}w")) - 11906) <= 2
    assert abs(int(size.get(f"{{{ns['w']}}}h")) - 16838) <= 2
    assert any(font.get(f"{{{ns['w']}}}eastAsia") for font in styles.findall(".//w:rFonts", ns))
    command = ["pandoc", "--from=gfm", "--to=latex", "--standalone",
               "--lua-filter", str(REPO / "runtime/native_helpers/bookforge_table_widths.lua")]
    with tempfile.TemporaryDirectory() as tmp:
        metadata = Path(tmp) / "metadata.yaml"
        metadata.write_text('author: "中山大学附属第六医院 高峰"\n', encoding="utf-8")
        output = subprocess.run(command + ["--metadata-file", str(metadata)], input="正文。\n",
                                text=True, capture_output=True, check=True).stdout
        assert "中山大学附属第六医院~高峰" in output
        metadata.write_text('author:\n  - "甲机构 张三"\n  - "乙机构 李四"\n', encoding="utf-8")
        output = subprocess.run(command + ["--metadata-file", str(metadata)], input="正文。\n",
                                text=True, capture_output=True, check=True).stdout
        assert "甲机构~张三" in output and "乙机构~李四" in output


if __name__ == "__main__":
    test_publication_bundle_contract()
    test_extraction_integrity()
    test_caption_and_list_writer_behavior()
    test_docx_table_rows_keep_content_and_headers()
    test_default_resources_and_chinese_byline()
    print('{"status":"passed","test":"publication_bundle_contract"}')
