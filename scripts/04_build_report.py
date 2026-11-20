"""Biên dịch reports/report/report.tex ra PDF (reports/report/build/report.pdf). Cần latexmk hoặc pdflatex (MiKTeX/TeX Live)."""
import shutil
import subprocess
import sys

from as3179ts.config import ROOT

REPORT_DIR = ROOT / "reports" / "report"


def main() -> None:
    (REPORT_DIR / "build").mkdir(exist_ok=True)
    if shutil.which("latexmk"):
        cmd = [["latexmk", "-pdf", "-interaction=nonstopmode", "-outdir=build", "report.tex"]]
    elif shutil.which("pdflatex"):
        cmd = [["pdflatex", "-interaction=nonstopmode", "-output-directory=build", "report.tex"]] * 2  # 2 lượt cho mục lục
    else:
        sys.exit("Chưa có LaTeX (latexmk/pdflatex). Cài MiKTeX hoặc TeX Live rồi chạy lại.")
    for c in cmd:
        subprocess.run(c, cwd=REPORT_DIR, check=True)
    print("PDF:", REPORT_DIR / "build" / "report.pdf")


if __name__ == "__main__":
    main()
