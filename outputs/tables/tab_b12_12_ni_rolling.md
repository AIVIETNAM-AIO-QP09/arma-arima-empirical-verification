**NI: RMSE gốc cuốn chiếu theo chân trời, gồm cả bước chọn mô hình lồng trong mỗi gốc**

| Phương pháp | RMSE h=1 | RMSE h=2 | RMSE h=3 | RMSE h=5 | số gốc h=1 |
|---|---|---|---|---|---|
| naive | 153.1 | 163.7 | 151.5 | 175.4 | 20 |
| trung bình mở rộng | 131.9 | 128.8 | 125.5 | 127.5 | 20 |
| ARIMA(0,1,1) cố định | 126.9 | 133.5 | 137.2 | 140.6 | 20 |
| ARIMA chọn theo AIC trong mỗi gốc | 126.2 | 131.7 | 134.3 | 137.3 | 20 |
