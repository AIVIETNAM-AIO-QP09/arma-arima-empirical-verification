"""Tạo notebook nộp LMS từ các ô phân tích và các hàm Python của nhóm."""
from hashlib import sha256
from pathlib import Path
import re

import nbformat as nb

ROOT = Path(__file__).resolve().parents[1]
NAME = "AS3179_Nhom7.ipynb"
MODULES = ("config", "data", "acf_tools", "arma_tools", "evaluation", "forecast_tools",
           "simulation", "captions", "reporting", "plotting")
ANALYSES = ("00_kham_pha_du_lieu", "bai11_arma", "bai12_arima_du_bao")

INTRO = """# AS3179 · Nhóm 7 · Kiểm chứng ARMA và ARIMA

Đặt notebook cạnh năm CSV gốc (hoặc cạnh thư mục `data/raw/` của bài nộp).
Chọn kernel Python 3.12 rồi **Restart Kernel and Run All Cells**. Nếu tạo môi trường mới,
cài các phiên bản ở Phụ lục B bằng pip trước khi chạy. Dữ liệu xử lý, bảng và hình
sẽ được tạo lại trong thư mục đang chạy. Không cần tải dữ liệu hay cài gói mã của nhóm.

Đọc theo thứ tự **hàm và dữ liệu → khám phá → Bài 11 (§11.1–11.14) → Bài 12 (§12.1–12.14)**.
Mỗi phép kiểm chứng có mã, kết quả và diễn giải. Hạt giống mô phỏng là 3179."""

REGISTER = '''from types import ModuleType
from pathlib import Path
import sys
from IPython.core.magic import register_cell_magic

# Mỗi ô %%hocphan chứa nguyên mã của một mô-đun. Các import nội bộ bên dưới
# trỏ tới các ô này trong bộ nhớ của kernel, kể cả trên máy chưa cài dự án.
package = ModuleType("as3179ts")
package.__path__ = []
sys.modules[package.__name__] = package

@register_cell_magic
def hocphan(name, source):
    fullname = f"as3179ts.{name}"
    module = ModuleType(fullname)
    module.__package__ = package.__name__
    sys.modules[fullname] = module
    setattr(package, name, module)
    exec(compile(source, f"<notebook: {name}>", "exec"), module.__dict__)'''

PATHS = '''ROOT = Path.cwd()
DATA_DIR = ROOT / "data"
DATA_RAW = DATA_DIR / "raw" if (DATA_DIR / "raw" / "Nile.csv").is_file() else ROOT
DATA_PROCESSED = DATA_DIR / "processed"
'''


def main():
    cells = [nb.v4.new_markdown_cell(INTRO), nb.v4.new_code_cell(REGISTER)]
    for module in MODULES:
        source = (ROOT / "src" / "as3179ts" / f"{module}.py").read_text(encoding="utf8")
        if module == "config":
            source = re.sub(r"(?ms)^ROOT = .*?(?=^FIG_DIR = )", lambda _: PATHS, source)
        cells.append(nb.v4.new_code_cell(f"%%hocphan {module}\n{source.rstrip()}"))

    cells.append(nb.v4.new_markdown_cell("## Dữ liệu đầu vào và tiền xử lý\n\nKiểm tra SHA-256 của năm CSV trước khi tạo sáu chuỗi HU, LY, DR, NI, AP và DP."))
    checksum_list = (ROOT / "data/raw/checksums.txt").read_text().splitlines()
    hashes = {line.split()[1]: line.split()[0] for line in checksum_list if line and not line.startswith("#")}
    checksum_code = ("from as3179ts.config import DATA_RAW\nfrom hashlib import sha256\n\n"
                     + "raw_sha256 = " + repr(hashes) + "\n"
                     + 'for filename, expected in raw_sha256.items():\n'
                     + '    path = DATA_RAW / filename\n'
                     + '    if sha256(path.read_bytes()).hexdigest() != expected:\n'
                     + '        raise ValueError(f"CSV khác bản gốc: {path}")')
    cells.append(nb.v4.new_code_cell(checksum_code))
    preprocess = (ROOT / "scripts/02_preprocess.py").read_text(encoding="utf8")
    cells.append(nb.v4.new_code_cell(preprocess.split('if __name__ == "__main__":')[0].rstrip() + "\n\nmain()"))
    for name in ANALYSES:
        book = nb.read(ROOT / "notebooks" / f"{name}.ipynb", as_version=4)
        for cell in book.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
            cell.metadata = {}
            cells.append(cell)
    for i, cell in enumerate(cells):
        cell.id = sha256(f"{i}:{cell.source}".encode()).hexdigest()[:12]
    book = nb.v4.new_notebook(cells=cells, metadata={"kernelspec": {
        "name": "python3", "language": "python", "display_name": "Python 3 (ipykernel)"}})
    nb.validate(book)
    (ROOT / NAME).write_text(nb.writes(book) + "\n", encoding="utf8", newline="\n")


if __name__ == "__main__":
    main()
