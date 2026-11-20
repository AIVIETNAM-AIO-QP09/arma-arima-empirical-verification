# AS3179 – Bài tập lớn: Chuỗi thời gian (Bài 11 + Bài 12)

Dùng Python để thực hiện, minh họa và kiểm chứng các nội dung lý thuyết của **Bài 11** (phụ thuộc và mô hình ARMA) và **Bài 12** (ARIMA và dự báo) trên 6 bộ dữ liệu thật:
HU, LY, DR (Bài 11) và NI, AP, DP (Bài 12). Đặc tả nguyên văn: `docs/spec/dac_ta_bai_tap_lon.md`. Hạn nộp: **12:00 thứ Hai 30/11/2026** (bản in nộp trong 5 phút đầu buổi học).

## Cài đặt (Windows, PowerShell)

Cần Python 3.11 hoặc 3.12.

```powershell
py -3.12 -m venv .venv               # hoặc dùng python3.12.exe có sẵn
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -e .
.\.venv\Scripts\python.exe -m ipykernel install --user --name as3179-ts --display-name "AS3179 time series"
```

Gói nội bộ `as3179ts` (thư mục `src/`) được cài **editable** (`-e .`, cấu hình ở `pyproject.toml`). Phiên bản đã dùng để tái lập: `requirements-lock.txt`.
Nếu PowerShell chặn `Activate.ps1`, gọi trực tiếp `.\.venv\Scripts\python.exe` (không cần đổi ExecutionPolicy).

## Chạy lại toàn bộ

```powershell
.\.venv\Scripts\python.exe run_all.py            # tải dữ liệu -> làm sạch -> test -> thực thi 3 notebook
.\.venv\Scripts\python.exe run_all.py --with-report   # thêm bước biên dịch báo cáo PDF (cần LaTeX)
```

Chỉ `scripts/01_download_data.py` dùng mạng (bỏ qua nếu `data/raw/` đã có; `--force` để tải lại). Bước notebook mất vài phút (mô phỏng và khớp lại mô hình nhiều lần).

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `data/raw/` | 5 CSV gốc từ Rdatasets (không sửa tay; checksum ở `checksums.txt`) |
| `data/processed/` | 6 file đã làm sạch (mỗi bộ một file); `data/DATA_SOURCES.md`: nguồn, codebook, các bước làm sạch |
| `src/as3179ts/` | hàm dùng chung: `acf_tools`, `arma_tools`, `forecast_tools`, `evaluation`, `simulation`, `plotting`, `reporting`, `data`, `config` (`SEED = 3179`) |
| `scripts/` | `01` tải dữ liệu, `02` làm sạch, `03` trích text bài giảng, `04` biên dịch báo cáo, `05` đóng gói nộp bài, `06` zip khung báo cáo để upload Overleaf |
| `notebooks/` | `00_kham_pha_du_lieu`, `bai11_arma` (11.1–11.14), `bai12_arima_du_bao` (12.1–12.14 + ⋆) |
| `tests/` | `test_data`, `test_manual_vs_library` (hàm tay khớp statsmodels), `test_lecture_reference` (tái lập số liệu bài giảng) |
| `reports/figures`, `reports/tables` | 26 hình PNG 300 dpi (`fig_b<bài>_<mục>_<nội dung>`) và 63 bảng (`tab_b<bài>_<mục>_<nội dung>` ở 3 dạng: `.csv` đủ chữ số, `.md`, `.tex` booktabs sẵn caption/nhãn). Chú thích của từng hình/bảng nằm ở `src/as3179ts/captions.py` |
| `reports/report/` | khung báo cáo LaTeX theo template: `main.tex`, `chapters/` (8 chương, tài liệu tham khảo, phụ lục), `assets/` (logo, nền bìa); bố cục: `docs/report_outline.md` |
| `docs/` | đặc tả, 2 PDF bài giảng, text trích từ PDF, `theory_checklist.md`, `reference_values.md` |

## Ánh xạ ID lý thuyết → notebook → mục báo cáo

- **11.1–11.14** → `notebooks/bai11_arma.ipynb`, section `## 11.x` → báo cáo **Chương 4** (kiểm chứng mục 2.1).
- **12.1–12.14 (+ ⋆)** → `notebooks/bai12_arima_du_bao.ipynb`, section `## 12.x` → báo cáo **Chương 5** (chuỗi không dừng, ARIMA) và **Chương 6** (dự báo).
- EDA → `notebooks/00_kham_pha_du_lieu.ipynb` → mục **3.2** của báo cáo; bảng tổng hợp cuối mỗi notebook → **Chương 7** (Bảng 7.1).
- Danh sách và trạng thái: `docs/theory_checklist.md`. Mỗi section có đủ 6 tiểu mục theo đặc tả; hai tiểu mục *Phân tích và diễn giải* và *Nhận xét* là `TODO(nhóm)`.

## Quy ước

- **Seed:** `SEED = 3179` khai báo duy nhất ở `src/as3179ts/config.py`. Mỗi mục mô phỏng dùng `simulation.child_rng(bài, mục, …)` = `default_rng([3179, …])`, nên kết quả không phụ thuộc thứ tự chạy ô.
- **DAX không có ngày lịch.** Chỉ có chỉ số ngày giao dịch `t = 1..1860` (`time = 1991 + 129/260 + (t−1)/260`, như `time()` của R).
- Hàm cài tay (`acf_tools`, `arma_tools`, `forecast_tools`, `evaluation`) không gọi statsmodels; statsmodels chỉ dùng để đối chiếu.
- File văn bản UTF-8; tên file không dấu, không khoảng trắng.

## Khác biệt đã biết so với bài giảng

`reports/tables/lecture_reference_check.md` so từng số của bài giảng với giá trị tái lập (xfail kèm lý do trong `tests/test_lecture_reference.py`): phần lớn khác biệt do bài giảng in giá trị R (Ljung–Box của phần dư, SE số), do tối ưu số, hoặc do dòng số ngẫu nhiên khác.
Riêng hàng *"iid + dịch mức"* trong bảng công suất ADF (0.08) chưa tái lập được (xem ô 12.4).

## Biên dịch báo cáo

**Trong VS Code (khuyến nghị):** cài MiKTeX (`winget install MiKTeX.MiKTeX --scope user`) và extension *LaTeX Workshop* (đã gợi ý trong `.vscode/extensions.json`). Mở `reports/report/main.tex` hoặc bất kỳ file trong `reports/report/chapters/`, lưu file (Ctrl+S) là tự biên dịch (pdfLaTeX hai lượt, thư mục `reports/report/build/`); xem PDF bằng nút *View LaTeX PDF* hoặc Ctrl+Alt+V. Lần biên dịch đầu mất vài phút vì MiKTeX tự tải gói (bật bằng `initexmf --set-config-value="[MPM]AutoInstall=1"`).
**Dòng lệnh:** `python scripts\04_build_report.py`. **Overleaf:** `python scripts\06_make_overleaf_zip.py`, upload zip, compiler pdfLaTeX, main document `main.tex`.
Lưu ý: ảnh trong `assets/` luôn gọi bằng đường dẫn `assets/…` (tên trần như `background.png` có thể trùng một tệp có sẵn trong thư viện TeX).

## Nộp bài

```powershell
.\.venv\Scripts\python.exe scripts\04_build_report.py        # cần pdflatex (MiKTeX)
.\.venv\Scripts\python.exe scripts\05_package_submission.py  # tạo submission/
```

`submission/` gồm `.tex`, `.pdf`, mã nguồn (`.py`, `.ipynb`), dữ liệu gốc và đã làm sạch (không nén), và **chỉ** `figures.zip` cho hình rời.
