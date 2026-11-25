**AP: ba cách mô hình hóa mùa vụ, có và không có độ trôi, AIC và RMSE trên tập kiểm định 1959--1960**

| Mô hình | k | n dòng | AIC | RMSE giữ lại |
|---|---|---|---|---|
| airline | 3 | 107 | -389.0 | 43.2 |
| 11 biến giả + ∇ + MA(1) | 13 | 119 | -424.3 | 85.5 |
| 11 biến giả + ∇ + MA(1) + trôi | 14 | 119 | -434.0 | 33.1 |
| Fourier K = 2 | 6 | 119 | -311.7 | 74.8 |
| Fourier K = 2 + trôi | 7 | 119 | -330.5 | 23.6 |
| Fourier K = 3 | 8 | 119 | -330.0 | 77.9 |
| Fourier K = 3 + trôi | 9 | 119 | -347.5 | 21.9 |
| Fourier K = 4 | 10 | 119 | -384.6 | 82.0 |
| Fourier K = 4 + trôi | 11 | 119 | -398.0 | 27.6 |

*Ghi chú:* n dòng: số quan sát còn lại sau sai phân, như Ví dụ 4.2 của Bài 12. AIC chỉ so sánh trực tiếp được giữa các mô hình cùng cách sai phân. Dòng ``+ trôi'' thêm hằng số vào phương trình của $\nabla y$, tức một độ trôi; Ví dụ 4.2 dùng bản không có độ trôi.
