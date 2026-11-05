"""Static validation for the six shared project notebooks.

No Olist data is required; verifies file JSON, Python-cell syntax, and no
fabricated execution outputs committed into source control.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "01_TAN_LEN_chuong_1_6.ipynb",
    "02_NGOC_LAN_chuong_2.ipynb",
    "03_LAM_LINH_chuong_3.ipynb",
    "04_TRUC_CHI_chuong_4.ipynb",
    "05_VINH_CHI_chuong_5.ipynb",
    "06_FINAL_tong_hop_do_an.ipynb",
]


def test_exactly_six_notebooks():
    existing = sorted(path.name for path in (ROOT / "notebooks").glob("*.ipynb"))
    assert existing == EXPECTED, f"Expected shared notebooks only: {existing}"


def test_all_python_cells_are_syntactically_valid_and_unexecuted():
    for filename in EXPECTED:
        path = ROOT / "notebooks" / filename
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        cells = notebook["cells"]
        assert cells and any(c["cell_type"] == "markdown" for c in cells)
        assert any(c["cell_type"] == "code" for c in cells)
        for index, cell in enumerate(cells):
            assert isinstance(cell["source"], (str, list))
            source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
            if cell["cell_type"] == "code":
                ast.parse(source, filename=f"{filename}:cell-{index}")
                assert cell["execution_count"] is None
                assert cell["outputs"] == []


def test_theory_markdown_matches_owners():
    expected_theory = [
        "01_tan_len_ch1_ch6.md",
        "02_ngoc_lan_ch2.md",
        "03_lam_linh_ch3.md",
        "04_truc_chi_ch4.md",
        "05_vinh_chi_ch5.md",
        "06_final_integration.md",
    ]
    actual = sorted(p.name for p in (ROOT / "docs" / "theory").glob("*.md"))
    assert actual == expected_theory
