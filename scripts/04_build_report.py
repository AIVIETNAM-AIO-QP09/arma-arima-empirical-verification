"""Biên dịch report/main.tex ra PDF bằng pdfLaTeX hai lượt (mục lục, tham chiếu chéo).

Kết quả: report/build/main.pdf, đồng thời sao chép thành report/BaoCao_AS3179_Nhom7.pdf (bản PDF để nộp và xem nhanh).
Cần MiKTeX hoặc TeX Live (pdflatex trên PATH). Trong VS Code dùng extension LaTeX Workshop (cấu hình ở .vscode/settings.json);
script này dành cho dòng lệnh.
"""
import shutil
import subprocess
import sys

from as3179ts.config import ROOT

REPORT_DIR = ROOT / "report"
PDF_NAME = "BaoCao_AS3179_Nhom7.pdf"


def main() -> None:
    if not shutil.which("pdflatex"):
        sys.exit("Chưa có pdflatex. Cài MiKTeX (winget install MiKTeX.MiKTeX) hoặc dùng Overleaf (scripts/06_make_overleaf_zip.py).")
    (REPORT_DIR / "build").mkdir(exist_ok=True)
    subprocess.run([sys.executable, ROOT / "scripts/07_make_notebook.py"], check=True)
    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-output-directory=build", "main.tex"]
    for _ in range(2):
        subprocess.run(cmd, cwd=REPORT_DIR, check=True)
    shutil.copy2(REPORT_DIR / "build" / "main.pdf", REPORT_DIR / PDF_NAME)
    print("PDF:", REPORT_DIR / PDF_NAME)


if __name__ == "__main__":
    main()
