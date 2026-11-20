# Nguồn dữ liệu

Cả 6 bộ là dữ liệu thật, thuộc gói R `datasets`, tải từ Rdatasets (Vincent Arel-Bundock):
`https://vincentarelbundock.github.io/Rdatasets/csv/datasets/<Tên>.csv`. Ngày tải: **2026-11-20** (script `scripts/01_download_data.py`).
Tương đương trong Python: `statsmodels.datasets.get_rdataset("<Tên>")`.

Chỉ 5 file CSV gốc (`LakeHuron`, `lynx`, `EuStockMarkets`, `Nile`, `AirPassengers`) vì DAX được dùng cho hai bộ (DR, DP). Các file gốc **không được sửa tay**; checksum SHA-256 ở `data/raw/checksums.txt`.
Các cột SMI, CAC, FTSE của `EuStockMarkets` chỉ giữ trong file gốc (SMI chỉ dùng cho phần mở rộng ⋆ đồng tích hợp, nếu làm).

Trích dẫn nguồn khoa học theo tài liệu R (`?LakeHuron`, `?lynx`, `?EuStockMarkets`, `?Nile`, `?AirPassengers`); nhóm cần đối chiếu lại nguyên văn trích dẫn trong tài liệu R trước khi đưa vào Mục 4.9.

| Mã | Bài / ví dụ | Bộ (R) | Quan sát | Biến đáp ứng, đơn vị | n | Khoảng thời gian | File đã làm sạch |
|---|---|---|---|---|---|---|---|
| HU | 11 (i) | `LakeHuron` | hằng năm | mực nước hồ Huron, ft so với mực nước biển | 98 | 1875–1972 | `HU_lakehuron.csv` |
| LY | 11 (ii) | `lynx` | hằng năm | số linh miêu bị bẫy, sông Mackenzie (Canada); mô hình hóa `log10` | 114 | 1821–1934 | `LY_lynx_log10.csv` |
| DR | 11 (iii) | `EuStockMarkets` cột `DAX` | ngày giao dịch | suất sinh lợi log `100·log(P_t/P_{t−1})`, đơn vị % | 1859 | t = 2..1860 | `DR_dax_returns.csv` |
| NI | 12 (i) | `Nile` | hằng năm | lưu lượng sông Nile tại Aswan, 10⁸ m³ | 100 | 1871–1970 | `NI_nile.csv` |
| AP | 12 (ii) | `AirPassengers` | hằng tháng | hành khách hàng không quốc tế, nghìn người; mô hình hóa `log` | 144 | 01/1949–12/1960 | `AP_airpassengers.csv` |
| DP | 12 (iii) | `EuStockMarkets` cột `DAX` | ngày giao dịch | log giá đóng cửa DAX | 1860 | t = 1..1860 | `DP_dax_logprice.csv` |

## Các bước làm sạch / biến đổi (`scripts/02_preprocess.py`)

Kiểm tra cho mọi bộ: đúng số dòng, không NA, không dòng trùng, thời gian đơn điệu, giá trị > 0 trước khi lấy log.

- **HU**: không biến đổi. Thêm `x_centered = year − 1920` (biến giải thích xu thế).
- **LY**: `log10_count = log10(count)`.
- **DAX (DR, DP)**: bộ gốc **không có ngày lịch**. Chuỗi R gốc có `start = c(1991, 130)`, `frequency = 260` ("thời gian giao dịch", đã bỏ cuối tuần và ngày lễ). Chỉ dùng chỉ số ngày giao dịch `t = 1..1860` và `time = 1991 + 129/260 + (t−1)/260` (như `time()` của R). **Không gán ngày lịch.**
  - DR: `ret_pct = 100·Δlog P_t`, 1859 dòng (t = 2..1860).
  - DP: `log_close = log P_t`; `split = train` cho t ≤ 1500 và `test` cho t > 1500 (1500 + 360).
- **NI**: không biến đổi. Thêm `post_1899 = 1` nếu `year ≥ 1899` (để thảo luận đổi mức; "trước 1899" là `year < 1899`, trung bình 1098).
- **AP**: cột `time` của CSV là số thực (1949, 1949.0833…), chuyển thành chuỗi tháng `YYYY-MM` qua chỉ số tháng; `log_passengers = log(passengers)`; `split = train` cho 1949-01..1958-12 (120), `test` cho 1959-01..1960-12 (24).

## Đối chiếu với bài giảng (đã kiểm tra tự động trong `tests/test_data.py`)

HU trung bình 579.0, SD 1.32; DR trung bình 0.065, SD 1.03; NI trung bình 919, SD 169, trước 1899 là 1098; DAX cuối 5473.72.

## Codebook các file đã làm sạch

| File | Cột |
|---|---|
| `HU_lakehuron.csv` | `year`, `level_ft`, `x_centered` |
| `LY_lynx_log10.csv` | `year`, `count`, `log10_count` |
| `DR_dax_returns.csv` | `t`, `time`, `dax_close`, `ret_pct` |
| `NI_nile.csv` | `year`, `flow`, `post_1899` |
| `AP_airpassengers.csv` | `month`, `passengers`, `log_passengers`, `split` |
| `DP_dax_logprice.csv` | `t`, `time`, `dax_close`, `log_close`, `split` |
