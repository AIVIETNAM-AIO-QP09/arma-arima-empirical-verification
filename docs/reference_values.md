# Phụ lục B — Giá trị tham chiếu từ bài giảng (dùng cho `tests/test_lecture_reference.py`)

Trích từ "Kết quả kỳ vọng" ở Mục 6 và các ví dụ mẫu của Bài 11, 12. Làm tròn như bài giảng in.

## Bài 11

**HU — Hồ Huron, hồi quy theo `x = năm − 1920` với sai số ARMA**
- Mã: `ARIMA(y, exog=x, order=o).fit()` với `o ∈ {(1,0,0), (2,0,0), (0,0,2), (1,0,1)}`.
- AIC = 218.45, 212.40, 219.75, 212.40.
- BIC = 228.79, 225.32, 232.68, 225.32.
- AR(2) (dùng `cov_type="oim"`): φ̂ = (1.0048, −0.2913), hệ số dốc −0.0216 (SE 0.0081), σ̂² = 0.4566.
- Q_LB(10) của phần dư AR(2), `model_df=2`: 3.95 (Python; R ra 3.93), p = 0.86.
- OLS `y ~ x`: hệ số dốc −0.0242 (SE 0.0040).
- statsmodels có thể in cảnh báo hội tụ; cảnh báo này không ảnh hưởng các số trên.

**LY — log10(lynx)**
- n = 114, γ̂(0) = 0.309, ρ̂(1) = 0.785, ρ̂(2) = 0.340.
- `yule_walker(y, order=2, method="mle")`: φ̂ = (1.350, −0.720), σ̂² = 0.057 (Python; R `ar.yw` ra 0.0586 vì hiệu chỉnh n/(n−p−1)).
- Nghiệm có môđun 1.178; chu kỳ 9.66 năm.
- Với `ARIMA(y, order=(p,0,0))`, p = 1..14: AIC chọn p = 11, BIC chọn p = 2.
- Giá trị p của Ljung–Box (lag 20, `model_df = p`): 0.009 cho AR(2) và 0.52 cho AR(11).

**Mô phỏng Định lý 1 (AR(1))**
- φ = 0.6, n = 100, B = 2000, seed 3179, burn-in 200.
- Độ phủ của KTC ngây thơ: 0.67 (Python; R ra 0.65). Độ phủ đã hiệu chỉnh bằng √τ: 0.94 (R).

**DR — suất sinh lợi DAX**
- n = 1859, trung bình 0.065, SD 1.03.
- Q_LB(10) của r_t = 6.37 (p = 0.78).
- Q_LB(10) của r_t² = 110.7 (p ≈ 4×10⁻¹⁹).

## Bài 12

**NI — Nile**
- n = 100, trung bình 919, SD 169; trung bình trước 1899 là 1098.
- `ARIMA(y, order=(0,1,1), trend="n")`: θ̂ = −0.733, σ̂² = 20 600, AIC = 1269.1.
- SE của θ̂: R ra 0.114; statsmodels mặc định ra 0.074 (vì dùng tích ngoài gradient); `cov_type="approx"` tái tạo 0.114.
- Q_LB(12) = 13.7 với 11 bậc tự do (p = 0.25).
- Dự báo 798; khoảng 95% là (517, 1080) tại h = 1 và (438, 1159) tại h = 10.
- α = 1 + θ̂ = 0.267; đệ quy làm trơn mũ tái tạo được dự báo; σ̂_ε² = 15 099, σ̂_η² = 1 469.
- ADF: −4.05 (`regression="c"`), −4.79 (`"ct"`). KPSS (`nlags="auto"`) = 0.87.

**AP — AirPassengers (log; train = 120 tháng đầu)**
- SD của tr, ∇tr, ∇₁₂tr, ∇∇₁₂tr: 0.392, 0.106, 0.066, 0.046.
- ACF của ∇∇₁₂ tại độ trễ 1, 11, 12, 13 ≈ −0.33, 0.08, −0.41, 0.18.
- `SARIMAX(tr, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n")`: θ̂ = −0.342, Θ̂ = −0.541, σ̂² = 0.00140, AIC = −389.0.
- Q_LB(24) = 20.3 với 22 bậc tự do.
- Dự báo tháng 1/1959: trung vị 348.6, trung bình 348.8, khoảng (324, 375).
- Dự báo tháng 12/1960: trung vị 388.1, trung bình 392.8, khoảng (286, 526).
- Tập giữ lại 24 tháng, (RMSE, MAE, MAPE, MASE), với MASE chia cho Q = MAE của naive mùa vụ trong mẫu train trên thang gốc:
  - airline: 43.2, 39.5, 8.5%, 1.38
  - naive mùa vụ: 77.0, 71.3, 15.5%, 2.49
  - trôi: 115.7, 91.6, 18.4%, 3.21
  - naive: 137.3, 115.3, 23.6%, 4.03
- Gốc cuốn chiếu, dự báo 1 bước, t = 120..143: RMSE 15.3 (airline) so với 50.0 (naive mùa vụ). Diebold–Mariano với hiệu mất mát bình phương, phân phối t với n−1 bậc tự do: DM = −7.49, p < 10⁻⁶.

**DP — log giá DAX**
- n = 1860, giá cuối 5473.72.
- Huấn luyện 1500 ngày đầu, dự báo 1 bước 360 ngày còn lại; độ chính xác 1 bước (RMSE, MAE):
  - naive: 1.439%, 1.094%
  - trôi: 1.435%, 1.092%
  - ARIMA(1,1,0): 1.439%, 1.094%
- Ví dụ mẫu: bước ngẫu nhiên có trôi, ước lượng δ và σ từ 1859 suất sinh lợi log, dự báo 1, 20 và 250 ngày giao dịch sau giá cuối 5473.72 (khoảng bất đối xứng sau khi lấy mũ). Bài giảng không in sẵn số, nên ghi giá trị tính được vào bảng.
- ⋆ Mở rộng: hồi quy log DAX theo log SMI cho β̂ = 0.820, R² = 0.965; Engle–Granger p = 0.28.

## Ghi chú bổ sung (từ việc đọc bài giảng, không có trong prompt gốc)

- Bài 11 trang 53 (bảng Huron) còn in AR(3): AIC 214.01, BIC 229.52; MA(1): 237.17, 247.51; Q_LB(10) từng mô hình: AR(1) 12.06, AR(2) 3.93, AR(3) 3.37, MA(1) 32.6, MA(2) 10.91, ARMA(1,1) 3.79.
- Bài 11 Ví dụ mẫu Huron ARMA(1,1): φ̂ = 0.653, θ̂ = 0.357, σ̂² = 0.457, ℓ̂ = −101.20.
- Bài 12 trang 44: sd trong năm của mức tăng từ 13.7 đến 77.7; trên thang log từ 0.108 đến 0.157; dải ACF ±0.171 (n = 131).
- Bài 12 Ví dụ 3.2: độ phủ khoảng 95% ARIMA(0,1,1), θ = −0.5, n = 100, 2000 lần: h = 1, 5, 10 cho 0.952, 0.936, 0.939.
- Bài 12 Ví dụ 1.2: tỷ lệ bác bỏ ADF (4000 lần lặp): AR(1) φ = 0.95: 0.14 (n=100), 0.32 (n=200); φ = 0.90: 0.35, 0.84; φ = 0.80: 0.84, 0.99; iid + dịch mức: 0.08.
- Bài 12 Định lý 1 mô phỏng: bước ngẫu nhiên n = 200, 2000 lần: trung bình ρ̂(h) = 0.96, 0.93, …, 0.68 (h = 1..10), 0.43 (h = 20).
- Bài 12 Ví dụ 4.2: airline k = 3, n = 107, AIC −389.0, RMSE 43.2; 11 biến giả k = 13, n = 119, AIC −424.3, RMSE 85.5; Fourier K = 2/3/4: AIC −311.7/−330.0/−384.6, RMSE 74.8/77.9/82.0.
- Số trang PDF thực tế: Bài 11 = 76 trang, Bài 12 = 80 trang (khác 68/71 ghi ở prompt; số 68/71 là số trang đánh theo footer của slide).
