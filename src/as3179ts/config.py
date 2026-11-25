"""Hằng số và đường dẫn tập trung. Mọi đường dẫn tính tương đối từ thư mục gốc dự án."""
from pathlib import Path

SEED = 3179  # giống bài giảng; mọi mô phỏng dùng numpy.random.default_rng(SEED)

ROOT = Path(__file__).resolve().parents[2]
# Trong repo, data/ nằm cạnh src/. Trong gói nộp (submission/), mã nằm ở code/ còn dữ liệu ở data/ cạnh code/,
# nên nếu ROOT/data không có thì dùng thư mục data/ ở cấp trên.
DATA_DIR = ROOT / "data" if (ROOT / "data").is_dir() or not (ROOT.parent / "data").is_dir() else ROOT.parent / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"
FIG_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"
LECTURE_DIR = ROOT / "docs" / "lectures"

AP_TRAIN_N = 120      # AirPassengers: 1949-01..1958-12
AP_TEST_N = 24        # 1959-01..1960-12
DP_TRAIN_N = 1500     # DAX: 1500 ngày giao dịch đầu
DP_TEST_N = 360
DAX_START_TIME = 1991 + 129 / 260  # start = c(1991, 130), frequency = 260 (như time() của R)
DAX_FREQ = 260
