"""Lưu bảng kết quả vào reports/tables/ dưới dạng CSV và Markdown (tên ổn định)."""
import pandas as pd

from .config import TABLE_DIR


def to_markdown(df: pd.DataFrame, floatfmt: str = "{:.4g}") -> str:
    """Bảng Markdown tối giản (không cần tabulate)."""
    d = df.reset_index() if df.index.name or not isinstance(df.index, pd.RangeIndex) else df
    cell = lambda v: floatfmt.format(v) if isinstance(v, float) else str(v)  # noqa: E731
    rows = ["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * len(d.columns)]
    rows += ["| " + " | ".join(cell(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join(rows) + "\n"


def save_table(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Lưu df thành reports/tables/<name>.csv và <name>.md; trả về df để hiển thị trong notebook."""
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLE_DIR / f"{name}.csv", encoding="utf-8")
    (TABLE_DIR / f"{name}.md").write_text(to_markdown(df), encoding="utf-8")
    return df
