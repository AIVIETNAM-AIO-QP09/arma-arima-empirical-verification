"""Tạo submission/: báo cáo .tex + .pdf, mã nguồn (.py/.ipynb), dữ liệu raw + processed, và CHỈ figures.zip cho hình rời.

Các mục 1–4 của đặc tả KHÔNG được nén; chỉ hình ảnh rời mới nằm trong ZIP. Các bảng của báo cáo (tables/*.tex) là mã LaTeX nên để rời,
còn hình PNG nằm trong figures.zip (giải nén vào thư mục figures/ cạnh main.tex để biên dịch lại).
"""
import shutil
import sys
import zipfile

from as3179ts.config import FIG_DIR, ROOT, TABLE_DIR

OUT = ROOT / "submission"
REPORT = ROOT / "report"
PDF = REPORT / "build" / "main.pdf"
TEX_DIRS = ("front", "chapters", "back")


def copy_tree(src, dst, suffixes=None):
    for f in src.rglob("*"):
        if f.is_file() and "__pycache__" not in f.parts and (suffixes is None or f.suffix in suffixes) and f.name != ".gitkeep":
            (dst / f.relative_to(src)).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst / f.relative_to(src))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not PDF.exists():
        sys.exit(f"Chưa có {PDF}; chạy scripts/04_build_report.py (hoặc biên dịch trên Overleaf rồi đặt PDF vào đó) trước.")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    # 1. .tex: main.tex + front/ chapters/ back/ (đường dẫn hình/bảng đổi về cùng thư mục) + assets/ (logo, nền bìa)
    files = [REPORT / "main.tex"] + [f for d in TEX_DIRS for f in sorted((REPORT / d).glob("*.tex"))]
    for f in files:
        dst = OUT / f.relative_to(REPORT)
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = f.read_text(encoding="utf-8").replace("{../outputs/figures}", "{figures}").replace("{../outputs/tables}", "{tables}")
        dst.write_text(text, encoding="utf-8")
    copy_tree(REPORT / "assets", OUT / "assets")
    (OUT / "tables").mkdir()
    for f in TABLE_DIR.glob("tab_*.tex"):
        shutil.copy2(f, OUT / "tables" / f.name)
    shutil.copy2(PDF, OUT / "report.pdf")                   # 2. .pdf
    for name in ("src", "scripts", "notebooks", "tests"):   # 3. .py / .ipynb
        copy_tree(ROOT / name, OUT / "code" / name, {".py", ".ipynb"})
    for f in ("run_all.py", "pyproject.toml", "requirements.txt", "requirements-lock.txt", "README.md"):
        shutil.copy2(ROOT / f, OUT / "code" / f)
    copy_tree(ROOT / "data", OUT / "data")                  # 4. dữ liệu gốc + đã làm sạch (+ DATA_SOURCES.md)
    with zipfile.ZipFile(OUT / "figures.zip", "w", zipfile.ZIP_DEFLATED) as z:  # 5. hình rời
        for f in sorted(FIG_DIR.glob("*.png")):
            z.write(f, f"figures/{f.name}")
    print("Đã tạo", OUT)


if __name__ == "__main__":
    main()
