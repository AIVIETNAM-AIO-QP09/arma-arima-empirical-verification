"""Chạy tuần tự: tải dữ liệu -> làm sạch -> trích text bài giảng -> test -> thực thi notebook -> (tùy chọn) báo cáo.

Dùng: python run_all.py [--with-report]
Chỉ bước tải dữ liệu cần mạng (bỏ qua nếu data/raw đã có). Chạy bằng Python của venv của dự án.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
NOTEBOOKS = ["00_kham_pha_du_lieu", "bai11_arma", "bai12_arima_du_bao"]


def run(*args):
    print("\n>>", " ".join(map(str, args)), flush=True)
    subprocess.run([PY, *map(str, args)], cwd=ROOT, check=True)


def main() -> None:
    run("scripts/01_download_data.py")
    run("scripts/02_preprocess.py")
    run("scripts/03_extract_lecture_text.py")
    run("-m", "pytest", "-q", "-p", "no:warnings")
    for nb in NOTEBOOKS:
        run("-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", "--ExecutePreprocessor.timeout=-1",
            f"notebooks/{nb}.ipynb")
    if "--with-report" in sys.argv:
        run("scripts/04_build_report.py")


if __name__ == "__main__":
    main()
