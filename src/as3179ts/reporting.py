"""Xuất bảng kết quả: CSV (đủ chữ số), Markdown và LaTeX (booktabs) vào reports/tables/, tên tab_b<bài>_<mục>_<nội dung>.

Chú thích (caption), nhãn cột, định dạng số nằm ở một nơi (captions.py) để mọi bảng trình bày nhất quán.
"""
import re

import numpy as np
import pandas as pd

from .config import TABLE_DIR

# --- Unicode -> LaTeX (pdfLaTeX + T5 không in được chữ Hy Lạp, mũ ^ và chỉ số dưới) ---
GREEK = {"α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta", "ε": r"\varepsilon", "η": r"\eta", "θ": r"\theta", "λ": r"\lambda",
         "μ": r"\mu", "ρ": r"\rho", "σ": r"\sigma", "τ": r"\tau", "φ": r"\phi", "ψ": r"\psi", "ω": r"\omega", "Γ": r"\Gamma", "Θ": r"\Theta",
         "Φ": r"\Phi", "Ψ": r"\Psi", "χ": r"\chi", "κ": r"\kappa", "π": r"\pi", "Σ": r"\Sigma", "ℓ": r"\ell"}
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉ₙ₊₋ₜₖⱼₐₑₒₓₕₘₚₛ", "0123456789n+-tkjaeoxhmps"))
SUP = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-"))
SYM = {"≤": r"\le", "≥": r"\ge", "≈": r"\approx", "∇": r"\nabla", "Δ": r"\Delta", "√": r"\sqrt{}", "∑": r"\sum", "±": r"\pm", "×": r"\times",
       "→": r"\to", "≡": r"\equiv", "⋆": r"\star", "∞": r"\infty", "−": "-", "≠": r"\neq", "∈": r"\in", "·": r"\cdot", "≪": r"\ll"}
HAT = "\u0302"
SPECIAL = {"<": r"$<$", ">": r"$>$", "%": r"\%", "&": r"\&", "#": r"\#", "_": r"\_", "|": r"\textbar{}", "~": r"\textasciitilde{}", "{": r"\{", "}": r"\}"}


def tex(s) -> str:
    """Chuỗi Unicode (có ký hiệu toán) -> LaTeX an toàn cho pdfLaTeX. Đoạn `$...$` có sẵn được giữ nguyên."""
    s = str(s).replace("Q_LB", "$Q_{LB}$").replace("n_eff", r"$n_{\mathrm{eff}}$")
    parts = re.split(r"(\$[^$]*\$)", s)
    out = []
    for p in parts:
        if p.startswith("$") and p.endswith("$") and len(p) > 1:
            out.append(p)
            continue
        buf, i = [], 0
        while i < len(p):
            ch = p[i]
            nxt = p[i + 1] if i + 1 < len(p) else ""
            if ch in GREEK:
                g = GREEK[ch]
                if nxt == HAT:
                    g, i = rf"\hat{{{g}}}", i + 1
                buf.append(f"${g}$")
            elif ch in SUB or ch in SUP:
                table, mark = (SUB, "_") if ch in SUB else (SUP, "^")
                run = ""
                while i < len(p) and p[i] in table:
                    run += table[p[i]]; i += 1
                i -= 1
                buf.append(f"${mark}{{{run}}}$")
            elif ch in SYM and ch not in "−":
                buf.append(f"${SYM[ch]}$")
            elif ch == "−":
                buf.append("$-$" if nxt.isdigit() else "–")
            elif ch == "^" and nxt.isalnum():
                buf.append(f"$^{{{nxt}}}$"); i += 1
            elif ch == HAT:
                pass
            elif ch in SPECIAL:
                buf.append(SPECIAL[ch])
            elif ch == "\\":
                buf.append(r"\textbackslash{}")
            else:
                buf.append(ch)
            i += 1
        out.append("".join(buf))
    return re.sub(r"\$\$", "", "".join(out)).replace("$ $", " ")


# --- Định dạng giá trị ---
def _is_p(col: str) -> bool:
    c = str(col).lower()
    return bool(re.search(r"(^|[\s(])p([\s)\-:=]|$)|p-value|p \(", c))


def fmt_value(v, col: str = "", spec: str | None = None, latex: bool = False) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "–"
    if isinstance(v, (bool, np.bool_)):
        return "Có" if v else "Không"
    if isinstance(v, (int, np.integer)):
        return f"{v:,}".replace(",", " ") if abs(v) >= 10000 else str(v)
    if isinstance(v, (float, np.floating)):
        v = float(v)
        if spec:
            return spec.format(v)
        if _is_p(col):
            if v < 1e-4:
                return "<0.0001" if not latex else r"$<10^{-4}$"
            return f"{v:.4f}"
        if v == 0:
            return "0"
        a = abs(v)
        if a < 1e-3 or a >= 1e7:
            m, e = f"{v:.3e}".split("e")
            m = m.rstrip("0").rstrip(".")
            return rf"${m}\times10^{{{int(e)}}}$" if latex else f"{m}e{int(e)}"
        if a >= 1e4:
            return f"{v:.0f}"
        if a >= 1e3:
            return f"{v:.1f}"
        return f"{v:.4g}" if a >= 0.1 or a == 0 else f"{v:.4f}".rstrip("0")
    return str(v)


def _prepare(df: pd.DataFrame, index_label: str | None) -> pd.DataFrame:
    d = df.copy()
    if isinstance(d.index, pd.MultiIndex):
        d.index = d.index.set_names([n or f"Chỉ tiêu {i + 1}" for i, n in enumerate(d.index.names)])
        d = d.reset_index()
    elif not isinstance(d.index, pd.RangeIndex):
        d.index.name = index_label or d.index.name or "Chỉ tiêu"
        d = d.reset_index()
    def cap(s):  # chỉ viết hoa khi từ đầu là chữ thường dài ≥ 3 (giữ nguyên ký hiệu như n, τ̂, n_eff, K)
        m = re.match(r"[A-Za-zÀ-ỹ]+", str(s))
        return str(s)[:1].upper() + str(s)[1:] if m and len(m.group(0)) >= 3 else str(s)

    d.columns = [cap(c) for c in d.columns]
    return d


def to_markdown(df: pd.DataFrame, caption: str | None = None, fmt: dict | None = None, index_label: str | None = None,
                note: str | None = None) -> str:
    d = _prepare(df, index_label)
    fmt = fmt or {}
    esc = lambda s: str(s).replace("|", "\\|")  # noqa: E731
    rows = ["| " + " | ".join(esc(c) for c in d.columns) + " |", "|" + "---|" * len(d.columns)]
    for r in d.itertuples(index=False):
        rows.append("| " + " | ".join(esc(fmt_value(v, c, fmt.get(c))) for v, c in zip(r, d.columns)) + " |")
    head = f"**{caption}**\n\n" if caption else ""
    tail = f"\n*Ghi chú:* {note}\n" if note else ""
    return head + "\n".join(rows) + "\n" + tail


def _to_latex_tall(d: pd.DataFrame, cells: list, n_idx: int, name: str, caption: str, note: str | None) -> str:
    """Bảng rộng mà ít dòng (nhiều đại lượng, vài bộ dữ liệu) được xoay: mỗi hàng một đại lượng, mỗi cột một bộ/mô hình."""
    labels = [", ".join(str(x) for x in row[:n_idx]) for row in cells]
    names = list(d.columns[n_idx:])
    header = " & ".join(tex(c) for c in ["Đại lượng"] + labels) + r" \\"
    body = "\n".join(" & ".join(tex(x) for x in [names[k]] + [row[n_idx + k] for row in cells]) + r" \\" for k in range(len(names)))
    spec = "l" + "r" * len(cells)
    notes = rf"\par\vspace{{2pt}}{{\footnotesize\textit{{Ghi chú:}} {tex(note)}}}" if note else ""
    return (f"\\begin{{table}}[H]\n\\centering\\small\n\\caption{{{tex(caption)}}}\\label{{tab:{name}}}\n"
            f"\\begin{{adjustbox}}{{max width=\\linewidth}}\n\\begin{{tabular}}{{{spec}}}\n\\toprule\n{header}\n\\midrule\n{body}\n\\bottomrule\n"
            f"\\end{{tabular}}\n\\end{{adjustbox}}{notes}\n\\end{{table}}\n")


def to_latex(df: pd.DataFrame, name: str, caption: str, fmt: dict | None = None, index_label: str | None = None,
             note: str | None = None) -> str:
    """Bảng booktabs, tự co về vừa bề rộng trang; cột chữ dài dùng p{}; có caption, nhãn `tab:<name>` và ghi chú."""
    d = _prepare(df, index_label)
    fmt = fmt or {}
    cells = [[fmt_value(v, c, fmt.get(c), latex=True) for v, c in zip(r, d.columns)] for r in d.itertuples(index=False)]
    ncol = len(d.columns)
    n_idx = df.index.nlevels if (isinstance(df.index, pd.MultiIndex) or not isinstance(df.index, pd.RangeIndex)) else 0
    if ncol >= 9 and len(cells) <= 4 and n_idx >= 1:
        return _to_latex_tall(d, cells, n_idx, name, caption, note)
    plain = lambda s: re.sub(r"\$.*?\$", "x", str(s))  # noqa: E731  (độ dài hiển thị, bỏ phần toán)
    maxlen = [max(len(plain(c)), *(len(plain(row[j])) for row in cells)) for j, c in enumerate(d.columns)]
    numeric = [pd.api.types.is_numeric_dtype(d.iloc[:, j]) and not pd.api.types.is_bool_dtype(d.iloc[:, j]) for j in range(ncol)]
    long_text = [j for j in range(ncol) if not numeric[j] and maxlen[j] > 28]
    share = {j: min(maxlen[j], 60) for j in long_text}
    frac = 0.97 if len(long_text) == ncol else 0.72
    spec = ""
    for j in range(ncol):
        if j in long_text:
            w = frac * share[j] / sum(share.values())
            spec += r">{\raggedright\arraybackslash}p{\dimexpr " + f"{w:.3f}" + r"\linewidth-2\tabcolsep\relax}"
        else:
            spec += "r" if numeric[j] else ("c" if pd.api.types.is_bool_dtype(d.iloc[:, j]) else "l")
    header = " & ".join(tex(c) for c in d.columns) + r" \\"
    end = r" \\[12pt]" if long_text else r" \\"   # bảng có cột chữ dài: thêm khoảng cách giữa các hàng
    body = "\n".join(" & ".join(tex(x) for x in row) + end for row in cells)
    size = r"\scriptsize" if ncol >= 9 else r"\small"
    notes = rf"\par\vspace{{2pt}}{{\footnotesize\textit{{Ghi chú:}} {tex(note)}}}" if note else ""
    return (f"\\begin{{table}}[H]\n\\centering{size}\n\\caption{{{tex(caption)}}}\\label{{tab:{name}}}\n"
            f"\\begin{{adjustbox}}{{max width=\\linewidth}}\n\\begin{{tabular}}{{{spec}}}\n\\toprule\n{header}\n\\midrule\n{body}\n\\bottomrule\n"
            f"\\end{{tabular}}\n\\end{{adjustbox}}{notes}\n\\end{{table}}\n")


def save_table(df: pd.DataFrame, name: str, caption: str | None = None, fmt: dict | None = None, index_label: str | None = None,
               note: str | None = None) -> pd.DataFrame:
    """Lưu df thành reports/tables/<name>.csv / .md / .tex; caption, nhãn chỉ số, ghi chú lấy từ captions.ARTIFACTS nếu không truyền.

    Trả về df để hiển thị trong notebook.
    """
    from .captions import ARTIFACTS

    meta = ARTIFACTS.get(name, {})
    caption = caption or meta.get("caption")
    if caption is None:
        raise KeyError(f"Bảng '{name}' chưa có caption trong as3179ts/captions.py")
    index_label = index_label or meta.get("index")
    note = note or meta.get("note")
    fmt = {**meta.get("fmt", {}), **(fmt or {})}
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    out = df.reset_index() if (isinstance(df.index, pd.MultiIndex) or not isinstance(df.index, pd.RangeIndex)) else df
    if index_label and out.columns[0] != index_label and not isinstance(df.index, pd.MultiIndex) and df.index.name is None:
        out = out.rename(columns={out.columns[0]: index_label})
    out.to_csv(TABLE_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")
    (TABLE_DIR / f"{name}.md").write_text(to_markdown(df, caption, fmt, index_label, note), encoding="utf-8")
    (TABLE_DIR / f"{name}.tex").write_text(to_latex(df, name, caption, fmt, index_label, note), encoding="utf-8")
    return df
