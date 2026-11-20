"""Tạo submission/: báo cáo .tex + .pdf, mã nguồn (.py/.ipynb), dữ liệu raw + processed, và CHỈ figures.zip cho hình rời.

Các mục 1–4 của đặc tả KHÔNG được nén; chỉ hình ảnh rời mới nằm trong ZIP.
"""
import shutil
import sys
import zipfile

from as3179ts.config import FIG_DIR, ROOT

OUT = ROOT / "submission"
PDF = ROOT / "reports" / "report" / "build" / "report.pdf"


def copy_tree(src, dst, suffixes=None):
    for f in src.rglob("*"):
        if f.is_file() and "__pycache__" not in f.parts and (suffixes is None or f.suffix in suffixes) and f.name != ".gitkeep":
            (dst / f.relative_to(src)).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst / f.relative_to(src))


def main() -> None:
    if not PDF.exists():
        sys.exit(f"Chưa có {PDF}; chạy scripts/04_build_report.py trước.")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for f in (ROOT / "reports" / "report").glob("*.tex"):
        shutil.copy2(f, OUT / f.name)                       # 1. .tex (report.tex + các phần \input)
    shutil.copy2(PDF, OUT / "report.pdf")                   # 2. .pdf
    for name in ("src", "scripts", "notebooks", "tests"):   # 3. .py / .ipynb
        copy_tree(ROOT / name, OUT / "code" / name, {".py", ".ipynb", ".toml"})
    for f in ("run_all.py", "pyproject.toml", "requirements.txt", "requirements-lock.txt", "README.md"):
        shutil.copy2(ROOT / f, OUT / "code" / f)
    copy_tree(ROOT / "data", OUT / "data")                  # 4. dữ liệu gốc + đã làm sạch (+ DATA_SOURCES.md)
    with zipfile.ZipFile(OUT / "figures.zip", "w", zipfile.ZIP_DEFLATED) as z:  # 5. hình rời
        for f in sorted(FIG_DIR.glob("*.png")):
            z.write(f, f.name)
    print("Đã tạo", OUT)


if __name__ == "__main__":
    main()
