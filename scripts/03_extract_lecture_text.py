"""Trích text UTF-8 từ 2 PDF bài giảng vào docs/lectures_text/ (để tra cứu, grep)."""
from pypdf import PdfReader

from as3179ts.config import LECTURE_DIR, ROOT

OUT = ROOT / "docs" / "lectures_text"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(LECTURE_DIR.glob("*.pdf")):
        pages = PdfReader(pdf).pages
        text = "\n".join(f"\n===== Trang {i} =====\n{p.extract_text() or ''}" for i, p in enumerate(pages, 1))
        (OUT / (pdf.stem + ".txt")).write_text(text, encoding="utf-8")
        print(f"{pdf.name}: {len(pages)} trang, {len(text)} ký tự")


if __name__ == "__main__":
    main()
