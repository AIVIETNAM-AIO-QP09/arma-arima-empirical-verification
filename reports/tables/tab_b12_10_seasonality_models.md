**AP: ba cách mô hình hóa mùa vụ, AIC và RMSE trên tập kiểm định 1959--1960**

| Mô hình | k | n dòng | AIC | RMSE giữ lại |
|---|---|---|---|---|
| airline | 3 | 120 | -389 | 43.18 |
| 11 biến giả + ∇ + MA(1) | 13 | 120 | -424.3 | 85.52 |
| Fourier K = 2 | 6 | 120 | -311.7 | 74.81 |
| Fourier K = 3 | 8 | 120 | -330 | 77.93 |
| Fourier K = 4 | 10 | 120 | -384.6 | 82 |

*Ghi chú:* AIC chỉ so sánh trực tiếp được giữa các mô hình cùng cách sai phân.
