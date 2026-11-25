**Độ trôi và tiêu chuẩn thông tin của các mô hình ARIMA đã khớp**

| Mô hình | μ̂_W (hệ số x1) | AIC | BIC | Số quan sát |
|---|---|---|---|---|
| NI: ARIMA(0,1,1), không trôi | 0 | 1269.1 | 1274.3 | 100 |
| DP: ARIMA(0,1,0) + trôi | 6.471e-4 | -11733 | -11722 | 1860 |
| DP: ARIMA(1,1,0) + trôi | 6.52e-4 | -11731 | -11715 | 1860 |

*Ghi chú:* AIC/BIC chỉ so sánh được giữa các mô hình có cùng $d$ và cùng dữ liệu. Với $d=1$, hệ số \texttt{x1} của \texttt{ARIMA(trend='t')} là $\mu_W=\E\nabla Y_t$, không phải $c=\phi(1)\mu_W$.
