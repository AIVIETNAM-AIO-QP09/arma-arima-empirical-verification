**DP: dự báo 1 bước trên 360 ngày với tham số cố định và khớp lại định kỳ**

| Phương pháp | RMSE (%) | MAE (%) |
|---|---|---|
| ARIMA(1,1,0) tham số cố định | 1.439 | 1.094 |
| ARIMA(1,1,0) khớp lại mỗi 60 ngày | 1.44 | 1.096 |
| trôi cố định (δ̂ của 1500 ngày đầu) | 1.435 | 1.092 |
| trôi cập nhật mỗi 60 ngày | 1.435 | 1.092 |
| naive | 1.439 | 1.094 |
