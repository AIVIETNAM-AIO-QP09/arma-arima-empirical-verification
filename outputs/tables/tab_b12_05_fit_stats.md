**Độ trôi và tiêu chuẩn thông tin của các mô hình ARIMA đã khớp**

| Mô hình | μ̂_W = ĉ/φ̂(1) | AIC | BIC | số quan sát |
|---|---|---|---|---|
| NI: ARIMA(0,1,1), không trôi | 0 | 1269.1 | 1274.3 | 100 |
| DP: ARIMA(0,1,0) + trôi | 6.471e-4 | -11733 | -11722 | 1860 |
| DP: ARIMA(1,1,0) + trôi | 6.517e-4 | -11731 | -11715 | 1860 |

*Ghi chú:* AIC/BIC chỉ so sánh được giữa các mô hình có cùng $d$ và cùng dữ liệu.
