"""Biên dịch reports/report/main.tex ra PDF (reports/report/build/main.pdf) bằng pdfLaTeX hai lượt (mục lục, tham chiếu chéo).

Cần MiKTeX hoặc TeX Live (pdflatex trên PATH). Trong VS Code dùng extension LaTeX Workshop (cấu hình ở .vscode/settings.json), script này dành cho dòng lệnh.
"""
import shutil
import subprocess
import sys

from as3179ts.config import ROOT

REPORT_DIR = ROOT / "reports" / "report"


def main() -> None:
    if not shutil.which("pdflatex"):
        sys.exit("Chưa có pdflatex. Cài MiKTeX (winget install MiKTeX.MiKTeX) hoặc dùng Overleaf (scripts/06_make_overleaf_zip.py).")
    (REPORT_DIR / "build").mkdir(exist_ok=True)
    cmd = ["pdflatex", "-interaction=nonstopmode", "-file-line-error", "-output-directory=build", "main.tex"]
    for _ in range(2):
        subprocess.run(cmd, cwd=REPORT_DIR, check=True)
    print("PDF:", REPORT_DIR / "build" / "main.pdf")


if __name__ == "__main__":
    main()
