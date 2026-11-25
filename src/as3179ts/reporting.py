"""Xuất bảng kết quả: CSV (đủ chữ số), Markdown và LaTeX (booktabs) vào outputs/tables/, tên tab_b<bài>_<mục>_<nội dung>.

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


def _plain(s: str) -> str:
    """Thoát ký tự đặc biệt cho văn bản thường (dùng trong \\texttt{})."""
    return "".join(SPECIAL.get(c, r"\textbackslash{}" if c == "\\" else c) for c in s)


def _math_inner(s: str) -> str:
    """Nội dung toán của một đoạn Unicode ngắn (dùng bên trong \\sqrt{} hoặc chỉ số dưới): tex() rồi bỏ các dấu $."""
    return tex(s).replace("$", "")


def _closing(p: str, i: int, open_ch: str, close_ch: str) -> int:
    """Vị trí ngoặc đóng khớp với ngoặc mở tại p[i] (−1 nếu không có)."""
    depth = 0
    for j in range(i, len(p)):
        depth += (p[j] == open_ch) - (p[j] == close_ch)
        if depth == 0:
            return j
    return -1


def tex(s) -> str:
    """Chuỗi Unicode (có ký hiệu toán) -> LaTeX an toàn cho pdfLaTeX. Đoạn `$...$` có sẵn được giữ nguyên.

    Ngoài ra: `mã` -> \\texttt{mã}; "trích dẫn" -> ``trích dẫn''; √(…) và √x -> \\sqrt{…}; x_t, σ²_ε, t_{m−1} -> chỉ số dưới
    (chỉ khi trước dấu _ là một ký hiệu đơn, nên tên biến như level_ft vẫn in nguyên).
    """
    s = str(s).replace("Q_LB", "$Q_{LB}$").replace("n_eff", r"$n_{\mathrm{eff}}$")
    s = re.sub(r"(?<!`)`([^`]+)`(?!`)", lambda m: "\x00" + m.group(1) + "\x01", s)   # đánh dấu đoạn mã (không đụng ``…'')
    s = re.sub(r'"([^"$]*)"', r"``\1''", s)
    parts = re.split(r"(\$[^$]*\$|\x00[^\x01]*\x01)", s)
    out = []
    for p in parts:
        if p.startswith("$") and p.endswith("$") and len(p) > 1:
            out.append(p)
            continue
        if p.startswith("\x00"):
            out.append(r"\texttt{" + _plain(p[1:-1]) + "}")
            continue
        buf, i = [], 0
        while i < len(p):
            ch = p[i]
            nxt = p[i + 1] if i + 1 < len(p) else ""
            prev = p[i - 1] if i > 0 else ""
            prev2 = p[i - 2] if i > 1 else " "
            if ch == "√" and nxt == "(" and _closing(p, i + 1, "(", ")") > 0:
                j = _closing(p, i + 1, "(", ")")
                buf.append(r"$\sqrt{" + _math_inner(p[i + 2:j]) + "}$"); i = j + 1
                continue
            if ch == "√" and nxt and (nxt.isalnum() or nxt in GREEK):
                j = i + 1
                while j < len(p) and (p[j].isalnum() or p[j] in GREEK or p[j] == HAT):
                    j += 1
                buf.append(r"$\sqrt{" + _math_inner(p[i + 1:j]) + "}$"); i = j
                continue
            single = prev in GREEK or prev in SUP or prev == HAT or (prev.isalpha() and not prev2.isalpha())
            if ch == "_" and single and nxt == "{" and _closing(p, i + 1, "{", "}") > 0:
                j = _closing(p, i + 1, "{", "}")
                buf.append("$_{" + _math_inner(p[i + 2:j]) + "}$"); i = j + 1
                continue
            if ch == "_" and single and nxt and (nxt.isalnum() or nxt in GREEK):
                j = i + 2
                while nxt.isdigit() and j < len(p) and p[j].isdigit():   # Ψ_100: lấy cả dãy chữ số
                    j += 1
                buf.append("$_{" + _math_inner(p[i + 1:j]) + "}$"); i = j
                continue
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


_SUP_DIGITS = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sci(v: float, digits: int = 3) -> str:
    """Số dạng 2.06×10⁴ thay cho 2.06e+04 (dùng khi ghép số vào chuỗi trong bảng); số vừa phải giữ dạng thường."""
    v = float(v)
    if v == 0 or 1e-3 <= abs(v) < 1e4:
        s = f"{v:.{digits}g}"
        if "e" in s:                      # ví dụ 2859.9 với 2 chữ số có nghĩa: "2.9e+03" -> "2900"
            s = f"{round(v, digits - 1 - int(np.floor(np.log10(abs(v))))):.0f}"
        return s
    m, e = f"{v:.{digits - 1}e}".split("e")
    m = m.rstrip("0").rstrip(".")
    return f"{m}×10{str(int(e)).translate(_SUP_DIGITS)}"


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


def _has_index_column(df: pd.DataFrame) -> bool:
    """Chỉ số có mang thông tin (cần in thành cột) hay chỉ là RangeIndex mặc định 0, 1, 2, ... không tên.

    Chỉ số kiểu range(1, 7) (độ trễ h = 1..6) cũng là RangeIndex nhưng có nghĩa, nên vẫn được in thành cột.
    """
    idx = df.index
    if isinstance(idx, pd.MultiIndex) or not isinstance(idx, pd.RangeIndex):
        return True
    return idx.name is not None or idx.start != 0 or idx.step != 1


def _prepare(df: pd.DataFrame, index_label: str | None) -> pd.DataFrame:
    d = df.copy()
    if isinstance(d.index, pd.MultiIndex):
        d.index = d.index.set_names([n or f"Chỉ tiêu {i + 1}" for i, n in enumerate(d.index.names)])
        d = d.reset_index()
    elif _has_index_column(d):
        d.index.name = index_label or d.index.name or "Chỉ tiêu"
        d = d.reset_index()
    d.columns = [cap(c) for c in d.columns]
    return d


# Từ đứng đầu tiêu đề cột nhưng là ký hiệu hoặc hàm toán, giữ nguyên chữ thường
_KEEP_LOWER = {"n", "k", "h", "p", "q", "s", "t", "x", "y", "r", "e", "d", "sd", "exp", "log", "log10", "max", "min", "var", "ln"}


def cap(s) -> str:
    """Viết hoa chữ cái đầu của tiêu đề (cả từ tiếng Việt ngắn như "bộ", "từ"), trừ khi từ đầu là ký hiệu toán (n, k, h, p, max, exp…)."""
    s = str(s)
    m = re.match(r"[A-Za-zÀ-ỹ0-9]+", s)
    if not m or not s[:1].isalpha() or "Ͱ" <= s[:1] <= "Ͽ" or not s[:1].islower() or m.group(0) in _KEEP_LOWER or s[:1] in "`$":
        return s
    return s[:1].upper() + s[1:]


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
    labels = [cap(", ".join(str(x) for x in row[:n_idx])) for row in cells]
    names = list(d.columns[n_idx:])
    header = " & ".join(tex(c) for c in ["Đại lượng"] + labels) + r" \\"
    body = "\n".join(" & ".join(tex(x) for x in [names[k]] + [row[n_idx + k] for row in cells]) + r" \\" for k in range(len(names)))
    spec = "|" + "|".join("l" + "r" * len(cells)) + "|"
    notes = rf"\par\vspace{{2pt}}{{\footnotesize\textit{{Ghi chú:}} {tex(note)}}}" if note else ""
    return (f"\\begin{{table}}[H]\n\\centering\\footnotesize\n\\caption{{{tex(caption)}}}\\label{{tab:{name}}}\n"
            f"\\begin{{adjustbox}}{{max width=\\linewidth}}\n\\begin{{tabular}}{{{spec}}}\n\\toprule\n{header}\n\\midrule\n{body}\n\\bottomrule\n"
            f"\\end{{tabular}}\n\\end{{adjustbox}}{notes}\n\\end{{table}}\n")


def to_latex(df: pd.DataFrame, name: str, caption: str, fmt: dict | None = None, index_label: str | None = None,
             note: str | None = None) -> str:
    """Bảng booktabs, tự co về vừa bề rộng trang; cột chữ dài dùng p{}; có caption, nhãn `tab:<name>` và ghi chú."""
    d = _prepare(df, index_label)
    fmt = fmt or {}
    cells = [[fmt_value(v, c, fmt.get(c), latex=True) for v, c in zip(r, d.columns)] for r in d.itertuples(index=False)]
    ncol = len(d.columns)
    n_idx = df.index.nlevels if _has_index_column(df) else 0
    if ncol >= 9 and len(cells) <= 4 and n_idx >= 1:
        return _to_latex_tall(d, cells, n_idx, name, caption, note)
    plain = lambda s: re.sub(r"\$.*?\$", "x", str(s))  # noqa: E731  (độ dài hiển thị, bỏ phần toán)
    maxlen = [max(len(plain(c)), *(len(plain(row[j])) for row in cells)) for j, c in enumerate(d.columns)]
    numeric = [pd.api.types.is_numeric_dtype(d.iloc[:, j]) and not pd.api.types.is_bool_dtype(d.iloc[:, j]) for j in range(ncol)]
    long_text = [j for j in range(ncol) if not numeric[j] and maxlen[j] > 28]
    share = {j: min(maxlen[j], 60) for j in long_text}
    frac = 0.97 if len(long_text) == ncol else 0.72
    cols = []
    for j in range(ncol):
        if j in long_text:
            w = frac * share[j] / sum(share.values())
            if len(long_text) < ncol:      # cột chữ cạnh các cột số: không rộng hơn mức chữ cần (≈ 0.0105 bề rộng mỗi ký tự)
                w = min(w, 0.0105 * share[j])
            cols.append(r">{\raggedright\arraybackslash}p{\dimexpr " + f"{w:.3f}" + r"\linewidth-2\tabcolsep\relax}")
        else:
            cols.append("r" if numeric[j] else ("c" if pd.api.types.is_bool_dtype(d.iloc[:, j]) else "l"))
    spec = "|" + "|".join(cols) + "|"   # có đường kẻ dọc giữa các cột
    header = " & ".join(tex(c) for c in d.columns) + r" \\"
    end = r" \\[3pt]" if long_text else r" \\"   # bảng có cột chữ dài: thêm chút khoảng cách giữa các hàng
    body = "\n".join(" & ".join(tex(x) for x in row) + end for row in cells)
    size = r"\scriptsize" if ncol >= 9 else r"\footnotesize"
    notes = rf"\par\vspace{{2pt}}{{\footnotesize\textit{{Ghi chú:}} {tex(note)}}}" if note else ""
    return (f"\\begin{{table}}[H]\n\\centering{size}\n\\caption{{{tex(caption)}}}\\label{{tab:{name}}}\n"
            f"\\begin{{adjustbox}}{{max width=\\linewidth}}\n\\begin{{tabular}}{{{spec}}}\n\\toprule\n{header}\n\\midrule\n{body}\n\\bottomrule\n"
            f"\\end{{tabular}}\n\\end{{adjustbox}}{notes}\n\\end{{table}}\n")


def save_table(df: pd.DataFrame, name: str, caption: str | None = None, fmt: dict | None = None, index_label: str | None = None,
               note: str | None = None) -> pd.DataFrame:
    """Lưu df thành outputs/tables/<name>.csv / .md / .tex; caption, nhãn chỉ số, ghi chú lấy từ captions.ARTIFACTS nếu không truyền.

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
    out = df.reset_index() if _has_index_column(df) else df
    if index_label and out.columns[0] != index_label and not isinstance(df.index, pd.MultiIndex) and df.index.name is None:
        out = out.rename(columns={out.columns[0]: index_label})
    out.to_csv(TABLE_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")
    (TABLE_DIR / f"{name}.md").write_text(to_markdown(df, caption, fmt, index_label, note), encoding="utf-8")
    (TABLE_DIR / f"{name}.tex").write_text(to_latex(df, name, caption, fmt, index_label, note), encoding="utf-8")
    return df
