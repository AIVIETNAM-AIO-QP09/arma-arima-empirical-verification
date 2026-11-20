"""Đóng gói khung báo cáo để upload lên Overleaf (pdfLaTeX): reports/report_overleaf.zip.

Cấu trúc trong zip: report.tex + các phần \\input ở gốc, thư mục figures/ (PNG) và tables/ (chỉ .tex). Đường dẫn ../figures, ../tables
được đổi thành figures, tables cho khớp Overleaf. Đây là gói xem thử, không phải gói nộp bài (xem 05_package_submission.py).
"""
import zipfile

from as3179ts.config import FIG_DIR, ROOT, TABLE_DIR

REPORT = ROOT / "reports" / "report"
OUT = ROOT / "reports" / "report_overleaf.zip"


def main() -> None:
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(REPORT.glob("*.tex")):
            text = f.read_text(encoding="utf-8").replace("{../figures}", "{figures}").replace("{../tables}", "{tables}")
            z.writestr(f.name, text)
        for f in sorted(TABLE_DIR.glob("tab_*.tex")):
            z.write(f, f"tables/{f.name}")
        for f in sorted(FIG_DIR.glob("*.png")):
            z.write(f, f"figures/{f.name}")
    with zipfile.ZipFile(OUT) as z:
        names = z.namelist()
    print(f"{OUT} ({OUT.stat().st_size / 1e6:.1f} MB): {sum(n.startswith('figures/') for n in names)} hình, "
          f"{sum(n.startswith('tables/') for n in names)} bảng, {sum('/' not in n for n in names)} file .tex")


if __name__ == "__main__":
    main()
