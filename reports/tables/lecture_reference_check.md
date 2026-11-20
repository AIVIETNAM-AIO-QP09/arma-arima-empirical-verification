# Đối chiếu giá trị bài giảng và giá trị tái lập

Tổng 114 giá trị; khớp 105.

| nội dung | bài giảng | tái lập | dung sai | khớp? |
|---|---|---|---|---|
| HU AIC ar1 | 218.45 | 218.45 | 0.005 | khớp |
| HU BIC ar1 | 228.79 | 228.79 | 0.005 | khớp |
| HU AIC ar2 | 212.4 | 212.397 | 0.005 | khớp |
| HU BIC ar2 | 225.32 | 225.321 | 0.005 | khớp |
| HU AIC ma2 | 219.75 | 219.752 | 0.005 | khớp |
| HU BIC ma2 | 232.68 | 232.676 | 0.005 | khớp |
| HU AIC arma11 | 212.4 | 212.395 | 0.005 | khớp |
| HU BIC arma11 | 225.32 | 225.32 | 0.005 | khớp |
| HU AR(2) φ̂₁ | 1.0048 | 1.00482 | 5e-05 | khớp |
| HU AR(2) φ̂₂ | -0.2913 | -0.291301 | 5e-05 | khớp |
| HU AR(2) hệ số dốc | -0.0216 | -0.0215732 | 5e-05 | khớp |
| HU AR(2) SE dốc | 0.0081 | 0.00812857 | 5e-05 | khớp |
| HU AR(2) σ̂² | 0.4566 | 0.456611 | 5e-05 | khớp |
| HU Q_LB(10) AR(2), model_df=2 (Python) | 3.95 | 3.94501 | 0.005 | khớp |
| HU p-value Q_LB(10) | 0.86 | 0.86205 | 0.005 | khớp |
| HU OLS hệ số dốc | -0.0242 | -0.0242011 | 5e-05 | khớp |
| HU OLS SE dốc | 0.004 | 0.00403611 | 5e-05 | khớp |
| LY n | 114 | 114 | 0 | khớp |
| LY γ̂(0) | 0.309 | 0.309085 | 0.0005 | khớp |
| LY ρ̂(1) | 0.785 | 0.785124 | 0.0005 | khớp |
| LY ρ̂(2) | 0.34 | 0.34023 | 0.0005 | khớp |
| LY YW φ̂₁ | 1.35 | 1.35044 | 0.0005 | khớp |
| LY YW φ̂₂ | -0.72 | -0.720031 | 0.0005 | khớp |
| LY YW σ̂² (Python) | 0.057 | 0.0570927 | 0.0005 | khớp |
| LY môđun nghiệm | 1.178 | 1.17849 | 0.0005 | khớp |
| LY chu kỳ (năm) | 9.66 | 9.6579 | 0.005 | khớp |
| LY AIC chọn p | 11 | 11 | 0 | khớp |
| LY BIC chọn p | 2 | 2 | 0 | khớp |
| LY p Ljung–Box AR(2), lag 20 | 0.009 | 0.00896563 | 0.0005 | khớp |
| LY p Ljung–Box AR(11), lag 20 | 0.52 | 0.618458 | 0.005 | lệch (xfail) |
| Mô phỏng ĐL 1: độ phủ ngây thơ (Python) | 0.67 | 0.671 | 0.005 | khớp |
| Mô phỏng ĐL 1: độ phủ đã hiệu chỉnh √τ (bài giảng in giá trị R) | 0.94 | 0.95 | 0.01 | lệch (xfail) |
| DR n | 1859 | 1859 | 0 | khớp |
| DR trung bình | 0.065 | 0.0652042 | 0.0005 | khớp |
| DR SD | 1.03 | 1.03008 | 0.005 | khớp |
| DR Q_LB(10) của r | 6.37 | 6.36558 | 0.005 | khớp |
| DR p của r | 0.78 | 0.783671 | 0.005 | khớp |
| DR Q_LB(10) của r² | 110.7 | 110.746 | 0.05 | khớp |
| DR p của r² (≈ 4×10⁻¹⁹) | 4e-19 | 3.77301e-19 | 5e-20 | khớp |
| NI n | 100 | 100 | 0 | khớp |
| NI trung bình | 919 | 919.35 | 0.5 | khớp |
| NI SD | 169 | 169.228 | 0.5 | khớp |
| NI trung bình trước 1899 | 1098 | 1097.75 | 0.5 | khớp |
| NI θ̂ | -0.733 | -0.733449 | 0.0005 | khớp |
| NI σ̂² | 20600 | 20598.9 | 50 | khớp |
| NI AIC | 1269.1 | 1269.08 | 0.05 | khớp |
| NI SE θ̂ mặc định statsmodels | 0.074 | 0.0744081 | 0.0005 | khớp |
| NI SE θ̂ cov_type='approx' | 0.114 | 0.114511 | 0.0005 | lệch (xfail) |
| NI Q_LB(12), df 11 | 13.7 | 13.5695 | 0.05 | lệch (xfail) |
| NI p Q_LB(12) | 0.25 | 0.257737 | 0.005 | lệch (xfail) |
| NI dự báo | 798 | 798.528 | 0.6 | khớp |
| NI cận dưới h=1 | 517 | 517.222 | 0.6 | khớp |
| NI cận trên h=1 | 1080 | 1079.83 | 0.6 | khớp |
| NI cận dưới h=10 | 438 | 438.342 | 0.6 | khớp |
| NI cận trên h=10 | 1159 | 1158.71 | 0.6 | khớp |
| NI α = 1 + θ̂ | 0.267 | 0.266551 | 0.0005 | khớp |
| NI làm trơn mũ − dự báo ARIMA | 0 | 7.38964e-12 | 1 | khớp |
| NI σ̂_ε² (dẫn xuất từ số làm tròn) | 15099 | 15108.3 | 40 | khớp |
| NI σ̂_η² (dẫn xuất từ số làm tròn) | 1469 | 1463.55 | 10 | khớp |
| NI ADF 'c' | -4.05 | -4.04871 | 0.005 | khớp |
| NI ADF 'ct' | -4.79 | -4.79077 | 0.005 | khớp |
| NI KPSS | 0.87 | 0.869121 | 0.005 | khớp |
| AP sd_tr | 0.392 | 0.391702 | 0.0005 | khớp |
| AP sd_d | 0.106 | 0.105849 | 0.0005 | khớp |
| AP sd_d12 | 0.066 | 0.0659761 | 0.0005 | khớp |
| AP sd_dd12 | 0.046 | 0.046187 | 0.0005 | khớp |
| AP ACF ∇∇₁₂ acf1 | -0.33 | -0.328037 | 0.005 | khớp |
| AP ACF ∇∇₁₂ acf11 | 0.08 | 0.0761795 | 0.005 | khớp |
| AP ACF ∇∇₁₂ acf12 | -0.41 | -0.405828 | 0.005 | khớp |
| AP ACF ∇∇₁₂ acf13 | 0.18 | 0.182386 | 0.005 | khớp |
| AP θ̂ | -0.342 | -0.342515 | 0.0005 | lệch (xfail) |
| AP Θ̂ | -0.541 | -0.540573 | 0.0005 | khớp |
| AP σ̂² | 0.0014 | 0.00140227 | 5e-06 | khớp |
| AP AIC | -389 | -389.01 | 0.05 | khớp |
| AP Q_LB(24), df 22 | 20.3 | 19.7605 | 0.05 | lệch (xfail) |
| AP jan59 median | 348.6 | 348.587 | 0.05 | khớp |
| AP jan59 mean | 348.8 | 348.832 | 0.05 | khớp |
| AP jan59 lo | 324 | 323.918 | 0.6 | khớp |
| AP jan59 hi | 375 | 375.134 | 0.6 | khớp |
| AP dec60 median | 388.1 | 388.156 | 0.05 | lệch (xfail) |
| AP dec60 mean | 392.8 | 392.846 | 0.05 | khớp |
| AP dec60 lo | 286 | 286.467 | 0.6 | khớp |
| AP dec60 hi | 526 | 525.941 | 0.6 | khớp |
| AP giữ lại 24 tháng: airline RMSE | 43.2 | 43.178 | 0.05 | khớp |
| AP giữ lại 24 tháng: airline MAE | 39.5 | 39.4416 | 0.05 | lệch (xfail) |
| AP giữ lại 24 tháng: airline MAPE | 8.5 | 8.51507 | 0.05 | khớp |
| AP giữ lại 24 tháng: airline MASE | 1.38 | 1.38033 | 0.005 | khớp |
| AP giữ lại 24 tháng: snaive RMSE | 77 | 76.9946 | 0.05 | khớp |
| AP giữ lại 24 tháng: snaive MAE | 71.3 | 71.25 | 0.05 | khớp |
| AP giữ lại 24 tháng: snaive MAPE | 15.5 | 15.5234 | 0.05 | khớp |
| AP giữ lại 24 tháng: snaive MASE | 2.49 | 2.49352 | 0.005 | khớp |
| AP giữ lại 24 tháng: drift RMSE | 115.7 | 115.703 | 0.05 | khớp |
| AP giữ lại 24 tháng: drift MAE | 91.6 | 91.6155 | 0.05 | khớp |
| AP giữ lại 24 tháng: drift MAPE | 18.4 | 18.4084 | 0.05 | khớp |
| AP giữ lại 24 tháng: drift MASE | 3.21 | 3.20625 | 0.005 | khớp |
| AP giữ lại 24 tháng: naive RMSE | 137.3 | 137.329 | 0.05 | khớp |
| AP giữ lại 24 tháng: naive MAE | 115.3 | 115.25 | 0.05 | khớp |
| AP giữ lại 24 tháng: naive MAPE | 23.6 | 23.5775 | 0.05 | khớp |
| AP giữ lại 24 tháng: naive MASE | 4.03 | 4.03338 | 0.005 | khớp |
| AP gốc cuốn chiếu RMSE airline | 15.3 | 15.2692 | 0.05 | khớp |
| AP gốc cuốn chiếu RMSE naive mùa vụ | 50 | 49.9867 | 0.05 | khớp |
| AP Diebold–Mariano | -7.49 | -7.49079 | 0.005 | khớp |
| AP p-value DM (< 10⁻⁶) | 0 | 1.30068e-07 | 1e-06 | khớp |
| DP n | 1860 | 1860 | 0 | khớp |
| DP giá cuối | 5473.72 | 5473.72 | 0.005 | khớp |
| DP 1 bước naive RMSE (%) | 1.439 | 1.43891 | 0.0005 | khớp |
| DP 1 bước naive MAE (%) | 1.094 | 1.0938 | 0.0005 | khớp |
| DP 1 bước drift RMSE (%) | 1.435 | 1.43524 | 0.0005 | khớp |
| DP 1 bước drift MAE (%) | 1.092 | 1.09211 | 0.0005 | khớp |
| DP 1 bước arima110 RMSE (%) | 1.439 | 1.43893 | 0.0005 | khớp |
| DP 1 bước arima110 MAE (%) | 1.094 | 1.09365 | 0.0005 | khớp |
| ⋆ hồi quy log DAX ~ log SMI: β̂ | 0.82 | 0.820253 | 0.0005 | khớp |
| ⋆ R² | 0.965 | 0.965016 | 0.0005 | khớp |
| ⋆ Engle–Granger p | 0.28 | 0.278113 | 0.005 | khớp |
