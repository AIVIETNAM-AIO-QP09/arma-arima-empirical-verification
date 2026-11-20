"""Biên dịch reports/report/main.tex ra PDF (reports/report/build/main.pdf). Cần latexmk hoặc pdflatex (MiKTeX/TeX Live) và gói minted (Python Pygments).

Dùng -shell-escape vì gói minted. Trên Overleaf không cần script này (chọn compiler pdfLaTeX).
"""
import shutil
import subprocess
import sys

from as3179ts.config import ROOT

REPORT_DIR = ROOT / "reports" / "report"


def main() -> None:
    (REPORT_DIR / "build").mkdir(exist_ok=True)
    if shutil.which("latexmk"):
        cmd = [["latexmk", "-pdf", "-shell-escape", "-interaction=nonstopmode", "-outdir=build", "main.tex"]]
    elif shutil.which("pdflatex"):
        cmd = [["pdflatex", "-shell-escape", "-interaction=nonstopmode", "-output-directory=build", "main.tex"]] * 2  # 2 lượt cho mục lục
    else:
        sys.exit("Chưa có LaTeX (latexmk/pdflatex). Cài MiKTeX hoặc TeX Live, hoặc dùng Overleaf (scripts/06_make_overleaf_zip.py).")
    for c in cmd:
        subprocess.run(c, cwd=REPORT_DIR, check=True)
    print("PDF:", REPORT_DIR / "build" / "main.pdf")


if __name__ == "__main__":
    main()
