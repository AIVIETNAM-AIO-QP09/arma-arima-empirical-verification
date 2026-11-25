"""Tạo các tệp nộp LMS, chỉ nén các hình và tài sản đồ họa."""
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

from as3179ts.config import FIG_DIR, ROOT, TABLE_DIR

REPORT = ROOT / "report"
OUT = ROOT / "submission"
PDF_NAME = "BaoCao_AS3179_Nhom7.pdf"
BOOK = "AS3179_Nhom7.ipynb"


def single_tex():
    """Chèn chương và bảng vào một tệp nguồn; giữ đường dẫn ảnh trong figures.zip."""
    pattern = re.compile(r"(?m)^[ \t]*\\input\{([^}]+)\}[ \t]*$")

    def expand(match):
        name = match.group(1)
        if name.startswith(r"\tabdir/"):
            path = TABLE_DIR / name.split("/", 1)[1]
        else:
            path = (REPORT / name).with_suffix(".tex")
        return pattern.sub(expand, path.read_text(encoding="utf8").rstrip())

    source = pattern.sub(expand, (REPORT / "main.tex").read_text(encoding="utf8"))
    return source.replace("{../outputs/figures}", "{figures}").replace(
        r"\newcommand{\notebookdir}{..}", r"\newcommand{\notebookdir}{.}")


def main():
    # Chuẩn bị đầy đủ ở thư mục tạm trước khi thay bất kỳ tệp đầu ra nào.
    OUT.mkdir(exist_ok=True)
    (REPORT / "build").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "report/build") as tmp:
        stage = Path(tmp)
        (stage / "main.tex").write_text(single_tex(), encoding="utf8")
        for src in (REPORT / PDF_NAME, ROOT / BOOK, *sorted((ROOT / "data/raw").glob("*.csv")),
                    *sorted((ROOT / "data/processed").glob("*.csv"))):
            shutil.copy2(src, stage / src.name)
        with zipfile.ZipFile(stage / "figures.zip", "w", zipfile.ZIP_DEFLATED) as archive:
            for folder, label in ((FIG_DIR, "figures"), (REPORT / "assets", "assets")):
                for src in sorted(folder.glob("*.png")):
                    archive.write(src, f"{label}/{src.name}")
        extra = {p.name for p in OUT.iterdir()} - {p.name for p in stage.iterdir()}
        if extra:
            raise ValueError(f"Tệp ngoài gói LMS hiện tại trong {OUT}: {sorted(extra)}")
        for path in stage.iterdir():
            path.replace(OUT / path.name)
    print(OUT)


if __name__ == "__main__":
    main()
