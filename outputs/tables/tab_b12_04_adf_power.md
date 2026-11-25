**Tỷ lệ bác bỏ nghiệm đơn vị ở mức 5% (có hệ số chặn): DF không độ trễ và ADF chọn độ trễ theo AIC, $B=1000$**

| Mô hình đúng | n | DF (không độ trễ) | ADF (độ trễ theo AIC) |
|---|---|---|---|
| AR(1), φ = 0.95 | 100 | 0.138 | 0.167 |
| AR(1), φ = 0.95 | 200 | 0.327 | 0.343 |
| AR(1), φ = 0.9 | 100 | 0.331 | 0.36 |
| AR(1), φ = 0.9 | 200 | 0.886 | 0.86 |
| AR(1), φ = 0.8 | 100 | 0.896 | 0.828 |
| AR(1), φ = 0.8 | 200 | 1 | 0.983 |
| iid N(0,1) + dịch mức 2 ở nửa sau | 100 | 1 | 0.08 |

*Ghi chú:* Hai cột dùng cùng các chuỗi mô phỏng. Cột ADF dùng mặc định của adfuller (độ trễ chọn theo AIC), như mã mẫu của Bài 12.
