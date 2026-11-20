**Phương sai sai số dự báo: công thức tay (Ψ và công thức đóng) so với statsmodels**

| Bộ dữ liệu | h tối đa | SE tay (h=1) | SE tay (h=tối đa) | SE statsmodels (h=tối đa) | Max \|tay/statsmodels − 1\| | Max \|công thức đóng/Ψ − 1\| |
|---|---|---|---|---|---|---|
| NI ARIMA(0,1,1) | 10 | 143.5 | 183.8 | 183.8 | 2.909e-14 | 2.22e-16 |
| DP bước ngẫu nhiên + trôi | 250 | 0.0103 | 0.1628 | 0.1628 | 2.887e-15 | 0 |
| AP airline (log) | 24 | 0.0374 | 0.155 | 0.155 | 1.008e-5 | – |
