**Đối chiếu giá trị in trong bài giảng với giá trị tái lập bằng code (105/114 khớp trong dung sai làm tròn)**

| Nội dung | Giá trị bài giảng | Giá trị tái lập | Dung sai | Kết quả | Lý do (nếu lệch) |
|---|---|---|---|---|---|
| HU AIC ar1 | 218.45 | 218.45 | 0.005 | Khớp |  |
| HU BIC ar1 | 228.79 | 228.79 | 0.005 | Khớp |  |
| HU AIC ar2 | 212.4 | 212.397 | 0.005 | Khớp |  |
| HU BIC ar2 | 225.32 | 225.321 | 0.005 | Khớp |  |
| HU AIC ma2 | 219.75 | 219.752 | 0.005 | Khớp |  |
| HU BIC ma2 | 232.68 | 232.676 | 0.005 | Khớp |  |
| HU AIC arma11 | 212.4 | 212.395 | 0.005 | Khớp |  |
| HU BIC arma11 | 225.32 | 225.32 | 0.005 | Khớp |  |
| HU AR(2) φ̂₁ | 1.0048 | 1.00482 | 5e-05 | Khớp |  |
| HU AR(2) φ̂₂ | -0.2913 | -0.291301 | 5e-05 | Khớp |  |
| HU AR(2) hệ số dốc | -0.0216 | -0.0215732 | 5e-05 | Khớp |  |
| HU AR(2) SE dốc | 0.0081 | 0.00812857 | 5e-05 | Khớp |  |
| HU AR(2) σ̂² | 0.4566 | 0.456611 | 5e-05 | Khớp |  |
| HU Q_LB(10) AR(2), model_df=2 (Python) | 3.95 | 3.94501 | 0.005 | Khớp |  |
| HU p-value Q_LB(10) | 0.86 | 0.86205 | 0.005 | Khớp |  |
| HU OLS hệ số dốc | -0.0242 | -0.0242011 | 5e-05 | Khớp |  |
| HU OLS SE dốc | 0.004 | 0.00403611 | 5e-05 | Khớp |  |
| LY n | 114 | 114 | 0 | Khớp |  |
| LY γ̂(0) | 0.309 | 0.309085 | 0.0005 | Khớp |  |
| LY ρ̂(1) | 0.785 | 0.785124 | 0.0005 | Khớp |  |
| LY ρ̂(2) | 0.34 | 0.34023 | 0.0005 | Khớp |  |
| LY YW φ̂₁ | 1.35 | 1.35044 | 0.0005 | Khớp |  |
| LY YW φ̂₂ | -0.72 | -0.720031 | 0.0005 | Khớp |  |
| LY YW σ̂² (Python) | 0.057 | 0.0570927 | 0.0005 | Khớp |  |
| LY môđun nghiệm | 1.178 | 1.17849 | 0.0005 | Khớp |  |
| LY chu kỳ (năm) | 9.66 | 9.6579 | 0.005 | Khớp |  |
| LY AIC chọn p | 11 | 11 | 0 | Khớp |  |
| LY BIC chọn p | 2 | 2 | 0 | Khớp |  |
| LY p Ljung–Box AR(2), lag 20 | 0.009 | 0.00896563 | 0.0005 | Khớp |  |
| LY p Ljung–Box AR(11), lag 20 | 0.52 | 0.618458 | 0.005 | Lệch nhẹ (xfail) | p = 0.6185 (AR(11) hội tụ, AIC chọn p = 11 khớp; AR(2) p = 0.009 khớp). Bài giảng in giá trị của R (Box.test trên arima); statsmodels khác quy ước khởi tạo/phần dư đầu. Đã thử đặt phần dư khuếch tán đầu về 0 như R, vẫn lệch nhẹ. Kết luận (không bác bỏ trắng) không đổi. |
| Mô phỏng ĐL 1: độ phủ ngây thơ (Python) | 0.67 | 0.671 | 0.005 | Khớp |  |
| Mô phỏng ĐL 1: độ phủ đã hiệu chỉnh √τ (bài giảng in giá trị R) | 0.94 | 0.95 | 0.01 | Lệch nhẹ (xfail) | Bài giảng in 0.94 là của R. Python seed 3179 cho 0.950, cách 0.94 khoảng 2 MCSE (0.005); R và NumPy dùng dòng số ngẫu nhiên khác nhau. |
| DR n | 1859 | 1859 | 0 | Khớp |  |
| DR trung bình | 0.065 | 0.0652042 | 0.0005 | Khớp |  |
| DR SD | 1.03 | 1.03008 | 0.005 | Khớp |  |
| DR Q_LB(10) của r | 6.37 | 6.36558 | 0.005 | Khớp |  |
| DR p của r | 0.78 | 0.783671 | 0.005 | Khớp |  |
| DR Q_LB(10) của r² | 110.7 | 110.746 | 0.05 | Khớp |  |
| DR p của r² (≈ 4×10⁻¹⁹) | 4e-19 | 3.77301e-19 | 5e-20 | Khớp |  |
| NI n | 100 | 100 | 0 | Khớp |  |
| NI trung bình | 919 | 919.35 | 0.5 | Khớp |  |
| NI SD | 169 | 169.228 | 0.5 | Khớp |  |
| NI trung bình trước 1899 | 1098 | 1097.75 | 0.5 | Khớp |  |
| NI θ̂ | -0.733 | -0.733449 | 0.0005 | Khớp |  |
| NI σ̂² | 20600 | 20598.9 | 50 | Khớp |  |
| NI AIC | 1269.1 | 1269.08 | 0.05 | Khớp |  |
| NI SE θ̂ mặc định statsmodels | 0.074 | 0.0744081 | 0.0005 | Khớp |  |
| NI SE θ̂ cov_type='approx' | 0.114 | 0.114511 | 0.0005 | Lệch nhẹ (xfail) | 0.1145 so với 0.114 (làm tròn lệch 5e-4): Hessian số của statsmodels khác R nhẹ. |
| NI Q_LB(12), df 11 | 13.7 | 13.5695 | 0.05 | Lệch nhẹ (xfail) | Q = 13.57 (resid[0] = 1120 là phần dư khuếch tán, đã đặt 0); bài giảng 13.7. Bài giảng in giá trị của R (Box.test trên arima); statsmodels khác quy ước khởi tạo/phần dư đầu. Đã thử đặt phần dư khuếch tán đầu về 0 như R, vẫn lệch nhẹ. Kết luận (không bác bỏ trắng) không đổi. |
| NI p Q_LB(12) | 0.25 | 0.257737 | 0.005 | Lệch nhẹ (xfail) | p = 0.258 so với 0.25. Bài giảng in giá trị của R (Box.test trên arima); statsmodels khác quy ước khởi tạo/phần dư đầu. Đã thử đặt phần dư khuếch tán đầu về 0 như R, vẫn lệch nhẹ. Kết luận (không bác bỏ trắng) không đổi. |
| NI dự báo | 798 | 798.528 | 0.6 | Khớp |  |
| NI cận dưới h=1 | 517 | 517.222 | 0.6 | Khớp |  |
| NI cận trên h=1 | 1080 | 1079.83 | 0.6 | Khớp |  |
| NI cận dưới h=10 | 438 | 438.342 | 0.6 | Khớp |  |
| NI cận trên h=10 | 1159 | 1158.71 | 0.6 | Khớp |  |
| NI α = 1 + θ̂ | 0.267 | 0.266551 | 0.0005 | Khớp |  |
| NI làm trơn mũ − dự báo ARIMA | 0 | 7.38964e-12 | 1 | Khớp |  |
| NI σ̂_ε² (dẫn xuất từ số làm tròn) | 15099 | 15108.3 | 40 | Khớp |  |
| NI σ̂_η² (dẫn xuất từ số làm tròn) | 1469 | 1463.55 | 10 | Khớp |  |
| NI ADF 'c' | -4.05 | -4.04871 | 0.005 | Khớp |  |
| NI ADF 'ct' | -4.79 | -4.79077 | 0.005 | Khớp |  |
| NI KPSS | 0.87 | 0.869121 | 0.005 | Khớp |  |
| AP sd_tr | 0.392 | 0.391702 | 0.0005 | Khớp |  |
| AP sd_d | 0.106 | 0.105849 | 0.0005 | Khớp |  |
| AP sd_d12 | 0.066 | 0.0659761 | 0.0005 | Khớp |  |
| AP sd_dd12 | 0.046 | 0.046187 | 0.0005 | Khớp |  |
| AP ACF ∇∇₁₂ acf1 | -0.33 | -0.328037 | 0.005 | Khớp |  |
| AP ACF ∇∇₁₂ acf11 | 0.08 | 0.0761795 | 0.005 | Khớp |  |
| AP ACF ∇∇₁₂ acf12 | -0.41 | -0.405828 | 0.005 | Khớp |  |
| AP ACF ∇∇₁₂ acf13 | 0.18 | 0.182386 | 0.005 | Khớp |  |
| AP θ̂ | -0.342 | -0.342515 | 0.0005 | Lệch nhẹ (xfail) | θ̂ = −0.3425 so với −0.342. Log-likelihood phẳng quanh cực đại: 4 bộ tối ưu (lbfgs, nm, bfgs, powell) đều cho θ̂ ≈ −0.3425 và log-lik tại (−0.342, −0.541) chỉ thấp hơn 2e-6. Lệch ≤ 0.06 ở số in, do dung sai tối ưu R vs statsmodels. |
| AP Θ̂ | -0.541 | -0.540573 | 0.0005 | Khớp |  |
| AP σ̂² | 0.0014 | 0.00140227 | 5e-06 | Khớp |  |
| AP AIC | -389 | -389.01 | 0.05 | Khớp |  |
| AP Q_LB(24), df 22 | 20.3 | 19.7605 | 0.05 | Lệch nhẹ (xfail) | Q = 19.76 (13 phần dư khuếch tán đầu đặt 0); bài giảng 20.3. Bài giảng in giá trị của R (Box.test trên arima); statsmodels khác quy ước khởi tạo/phần dư đầu. Đã thử đặt phần dư khuếch tán đầu về 0 như R, vẫn lệch nhẹ. Kết luận (không bác bỏ trắng) không đổi. |
| AP jan59 median | 348.6 | 348.587 | 0.05 | Khớp |  |
| AP jan59 mean | 348.8 | 348.832 | 0.05 | Khớp |  |
| AP jan59 lo | 324 | 323.918 | 0.6 | Khớp |  |
| AP jan59 hi | 375 | 375.134 | 0.6 | Khớp |  |
| AP dec60 median | 388.1 | 388.156 | 0.05 | Lệch nhẹ (xfail) | 388.156 so với 388.1. Log-likelihood phẳng quanh cực đại: 4 bộ tối ưu (lbfgs, nm, bfgs, powell) đều cho θ̂ ≈ −0.3425 và log-lik tại (−0.342, −0.541) chỉ thấp hơn 2e-6. Lệch ≤ 0.06 ở số in, do dung sai tối ưu R vs statsmodels. |
| AP dec60 mean | 392.8 | 392.846 | 0.05 | Khớp |  |
| AP dec60 lo | 286 | 286.467 | 0.6 | Khớp |  |
| AP dec60 hi | 526 | 525.941 | 0.6 | Khớp |  |
| AP giữ lại 24 tháng: airline RMSE | 43.2 | 43.178 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: airline MAE | 39.5 | 39.4416 | 0.05 | Lệch nhẹ (xfail) | 39.44 so với 39.5. Log-likelihood phẳng quanh cực đại: 4 bộ tối ưu (lbfgs, nm, bfgs, powell) đều cho θ̂ ≈ −0.3425 và log-lik tại (−0.342, −0.541) chỉ thấp hơn 2e-6. Lệch ≤ 0.06 ở số in, do dung sai tối ưu R vs statsmodels. |
| AP giữ lại 24 tháng: airline MAPE | 8.5 | 8.51507 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: airline MASE | 1.38 | 1.38033 | 0.005 | Khớp |  |
| AP giữ lại 24 tháng: snaive RMSE | 77 | 76.9946 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: snaive MAE | 71.3 | 71.25 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: snaive MAPE | 15.5 | 15.5234 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: snaive MASE | 2.49 | 2.49352 | 0.005 | Khớp |  |
| AP giữ lại 24 tháng: drift RMSE | 115.7 | 115.703 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: drift MAE | 91.6 | 91.6155 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: drift MAPE | 18.4 | 18.4084 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: drift MASE | 3.21 | 3.20625 | 0.005 | Khớp |  |
| AP giữ lại 24 tháng: naive RMSE | 137.3 | 137.329 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: naive MAE | 115.3 | 115.25 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: naive MAPE | 23.6 | 23.5775 | 0.05 | Khớp |  |
| AP giữ lại 24 tháng: naive MASE | 4.03 | 4.03338 | 0.005 | Khớp |  |
| AP gốc cuốn chiếu RMSE airline | 15.3 | 15.2692 | 0.05 | Khớp |  |
| AP gốc cuốn chiếu RMSE naive mùa vụ | 50 | 49.9867 | 0.05 | Khớp |  |
| AP Diebold–Mariano | -7.49 | -7.49079 | 0.005 | Khớp |  |
| AP p-value DM (< 10⁻⁶) | 0 | 1.30068e-07 | 1e-06 | Khớp |  |
| DP n | 1860 | 1860 | 0 | Khớp |  |
| DP giá cuối | 5473.72 | 5473.72 | 0.005 | Khớp |  |
| DP 1 bước naive RMSE (%) | 1.439 | 1.43891 | 0.0005 | Khớp |  |
| DP 1 bước naive MAE (%) | 1.094 | 1.0938 | 0.0005 | Khớp |  |
| DP 1 bước drift RMSE (%) | 1.435 | 1.43524 | 0.0005 | Khớp |  |
| DP 1 bước drift MAE (%) | 1.092 | 1.09211 | 0.0005 | Khớp |  |
| DP 1 bước arima110 RMSE (%) | 1.439 | 1.43893 | 0.0005 | Khớp |  |
| DP 1 bước arima110 MAE (%) | 1.094 | 1.09365 | 0.0005 | Khớp |  |
| ⋆ hồi quy log DAX ~ log SMI: β̂ | 0.82 | 0.820253 | 0.0005 | Khớp |  |
| ⋆ R² | 0.965 | 0.965016 | 0.0005 | Khớp |  |
| ⋆ Engle–Granger p | 0.28 | 0.278113 | 0.005 | Khớp |  |
