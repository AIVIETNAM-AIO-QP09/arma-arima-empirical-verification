"""Đóng gói báo cáo để upload lên Overleaf (compiler pdfLaTeX, main document main.tex): dist/AS3179_Nhom7_Overleaf.zip.

Cấu trúc trong zip: main.tex ở gốc, front/, chapters/, back/, assets/, figures/ (PNG), tables/ (chỉ .tex). Đường dẫn
../outputs/figures và ../outputs/tables trong main.tex được đổi thành figures và tables cho khớp Overleaf. Chỉ đưa vào zip những hình
và bảng mà báo cáo thực sự gọi, nên gói gọn nhẹ. Đây là gói biên dịch, không phải gói nộp bài (xem 05_package_submission.py).
"""
import re
import sys
import zipfile

from as3179ts.config import FIG_DIR, ROOT, TABLE_DIR

REPORT = ROOT / "report"
OUT = ROOT / "dist" / "AS3179_Nhom7_Overleaf.zip"
TEX_DIRS = ("front", "chapters", "back")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.parent.mkdir(exist_ok=True)
    texts = {"main.tex": (REPORT / "main.tex").read_text(encoding="utf-8")}
    for d in TEX_DIRS:
        for f in sorted((REPORT / d).glob("*.tex")):
            texts[f"{d}/{f.name}"] = f.read_text(encoding="utf-8")
    body = "\n".join(texts.values())
    used_figs = set(re.findall(r"\\figx\{([^}]+)\}", body))
    used_tabs = set(re.findall(r"\\tabdir/([A-Za-z0-9_]+)\.tex", body))
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT / "AS3179_Nhom7.ipynb", "AS3179_Nhom7.ipynb")
        for name, text in texts.items():
            z.writestr(name, text.replace(r"\newcommand{\notebookdir}{..}", r"\newcommand{\notebookdir}{.}").replace("{../outputs/figures}", "{figures}").replace("{../outputs/tables}", "{tables}"))
        for f in sorted((REPORT / "assets").glob("*")):
            z.write(f, f"assets/{f.name}")
        for n in sorted(used_tabs):
            z.write(TABLE_DIR / f"{n}.tex", f"tables/{n}.tex")
        for n in sorted(used_figs):
            z.write(FIG_DIR / f"{n}.png", f"figures/{n}.png")
    print(f"{OUT} ({OUT.stat().st_size / 1e6:.1f} MB): {len(used_figs)} hình, {len(used_tabs)} bảng, "
          f"{sum(k.startswith('chapters/') for k in texts)} chương")


if __name__ == "__main__":
    main()
