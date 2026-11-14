"""Static validation for the six shared project notebooks.

Olist data is not needed in CI. Saved execution results are permitted so team
members can review real tables and figures, but code syntax and output structure
must remain valid. The CI does not independently reproduce Olist results.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "01_TAN_LEN_chuong_1_6.ipynb",
    "02_NGOC_LAN_chuong_2.ipynb",
    "03_LAM_LINH_chuong_3.ipynb",
    "04_TRUC_CHI_chuong_4.ipynb",
    "05_VINH_CHI_chuong_5.ipynb",
    "06_FINAL_tong_hop_do_an.ipynb",
]
ALLOWED_OUTPUT_TYPES = {
    "stream", "display_data", "execute_result", "update_display_data"
}


def validate_code_cell(cell: dict, filename: str, index: int) -> None:
    """Allow genuine saved outputs; reject invalid counts and traceback outputs."""
    assert isinstance(cell["source"], (str, list))
    source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
    ast.parse(source, filename=f"{filename}:cell-{index}")

    count = cell.get("execution_count")
    assert count is None or (type(count) is int and count >= 1), (
        f"{filename}:cell-{index}: invalid execution_count"
    )
    outputs = cell.get("outputs")
    assert isinstance(outputs, list), f"{filename}:cell-{index}: outputs must be a list"
    assert count is not None or not outputs, (
        f"{filename}:cell-{index}: unexecuted cell cannot contain outputs"
    )
    for output in outputs:
        assert isinstance(output, dict)
        kind = output.get("output_type")
        assert kind in ALLOWED_OUTPUT_TYPES, (
            f"{filename}:cell-{index}: invalid or error output_type {kind!r}"
        )
        if kind == "stream":
            assert output.get("name") in {"stdout", "stderr"}
            assert isinstance(output.get("text"), (str, list))
        else:
            assert isinstance(output.get("data"), dict)
        if kind == "execute_result":
            result_count = output.get("execution_count")
            assert result_count is None or (
                type(result_count) is int and result_count >= 1
            )


def test_exactly_six_notebooks():
    existing = sorted(path.name for path in (ROOT / "notebooks").glob("*.ipynb"))
    assert existing == EXPECTED, f"Expected shared notebooks only: {existing}"


def test_all_python_cells_are_syntactically_valid_and_outputs_well_formed():
    for filename in EXPECTED:
        path = ROOT / "notebooks" / filename
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        cells = notebook["cells"]
        assert cells and any(c["cell_type"] == "markdown" for c in cells)
        assert any(c["cell_type"] == "code" for c in cells)
        for index, cell in enumerate(cells):
            assert isinstance(cell["source"], (str, list))
            if cell["cell_type"] == "code":
                validate_code_cell(cell, filename, index)


def test_saved_execution_output_is_allowed():
    cell = {
        "source": ["print('OK')\n"],
        "execution_count": 1,
        "outputs": [{"output_type": "stream", "name": "stdout", "text": ["OK\n"]}],
    }
    validate_code_cell(cell, "example.ipynb", 0)


def test_clean_unexecuted_cell_is_still_allowed():
    cell = {"source": "x = 1", "execution_count": None, "outputs": []}
    validate_code_cell(cell, "example.ipynb", 0)


def test_error_output_is_not_accepted():
    cell = {
        "source": "1 / 0",
        "execution_count": 1,
        "outputs": [{
            "output_type": "error",
            "ename": "ZeroDivisionError",
            "evalue": "division by zero",
            "traceback": ["Traceback ..."],
        }],
    }
    with pytest.raises(AssertionError, match="error output_type"):
        validate_code_cell(cell, "example.ipynb", 0)


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
