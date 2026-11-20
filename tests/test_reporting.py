"""Bộ xuất bảng/hình: ký hiệu toán -> LaTeX, định dạng số, và mọi hình/bảng trong captions.py có đủ thông tin."""
import numpy as np
import pandas as pd

from as3179ts.captions import ARTIFACTS
from as3179ts.reporting import fmt_value, to_latex, to_markdown, tex


def test_unicode_math_to_latex():
    assert tex("σ̂²") == r"$\hat{\sigma}^{2}$"
    assert tex("φ̂₁₂") == r"$\hat{\phi}_{12}$"
    assert tex("10⁻⁴") == "10$^{-4}$"
    assert tex("|ρ̂|") == r"\textbar{}$\hat{\rho}$\textbar{}"
    assert tex("$x_1$ và 5%") == r"$x_1$ và 5\%"


def test_value_format():
    assert fmt_value(float("nan")) == "–" and fmt_value(True) == "Có" and fmt_value(False) == "Không"
    assert fmt_value(3e-20, "p-value") == "<0.0001" and fmt_value(0.0123456, "p-value") == "0.0123"
    assert fmt_value(-11730.4) == "-11730" and fmt_value(1.0) == "1"
    assert fmt_value(6.471e-4) == "6.471e-4"


def test_table_outputs_are_safe():
    df = pd.DataFrame({"n": [98], "τ̂ (AR(1))": [10.9], "p-value": [1e-9], "nhân quả": [True], "ghi chú": [np.nan]}, index=pd.Index(["HU"], name="Bộ"))
    md, tx = to_markdown(df, "cap"), to_latex(df, "tab_x", "cap")
    assert "| n |" in md and "| N |" not in md          # không viết hoa ký hiệu n
    assert "nan" not in md and "True" not in md and "Có" in md
    assert r"\hat{\tau}" in tx and r"\toprule" in tx and r"\label{tab:tab_x}" in tx
    assert all(ord(c) < 128 or c.isalpha() or c == "–" for c in tx)   # chỉ chữ Latin/Việt và gạch ngang (ô trống)


def test_every_artifact_has_caption_and_sorted_names():
    for name, meta in ARTIFACTS.items():
        assert name.startswith(("fig_", "tab_")) and meta["caption"].strip()
