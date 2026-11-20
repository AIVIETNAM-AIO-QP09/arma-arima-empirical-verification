"""Tải 5 CSV từ Rdatasets vào data/raw/ và ghi SHA-256. Đây là script duy nhất được truy cập mạng.

Dùng: python scripts/01_download_data.py [--force]
"""
import hashlib
import sys
import urllib.request
from datetime import date

from as3179ts.config import DATA_RAW

NAMES = ["LakeHuron", "lynx", "EuStockMarkets", "Nile", "AirPassengers"]
URL = "https://vincentarelbundock.github.io/Rdatasets/csv/datasets/{}.csv"


def main() -> None:
    force = "--force" in sys.argv
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    lines = []
    for name in NAMES:
        path = DATA_RAW / f"{name}.csv"
        if force or not path.exists():
            try:
                with urllib.request.urlopen(URL.format(name), timeout=60) as resp:
                    path.write_bytes(resp.read())
            except OSError as exc:
                sys.exit(f"Không tải được {name} (kiểm tra kết nối mạng): {exc}")
            print(f"đã tải {path.name}")
        else:
            print(f"đã có {path.name} (dùng --force để tải lại)")
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    with open(DATA_RAW / "checksums.txt", "w", encoding="utf-8", newline="\n") as fh:  # newline cố định để git không báo thay đổi giả
        fh.write(f"# SHA-256, ghi ngày {date.today().isoformat()}\n" + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
