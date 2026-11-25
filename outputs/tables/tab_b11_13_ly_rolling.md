**LY: sai số dự báo 1 bước trên gốc cuốn chiếu, 1915--1934 (khớp lại mỗi năm)**

| Mô hình | Số gốc | RMSE 1 bước | MAE 1 bước |
|---|---|---|---|
| AR(2) | 20 | 0.2339 | 0.1885 |
| AR(11) | 20 | 0.2033 | 0.1517 |
| AR(p) chọn theo AIC trong mỗi gốc | 20 | 0.2088 | 0.1645 |
| trung bình quá khứ | 20 | 0.5436 | 0.4629 |

*Ghi chú:* Dòng ``AR($p$) chọn theo AIC trong mỗi gốc'' chọn $p\in\{1,\dots,14\}$ tại từng gốc chỉ bằng dữ liệu trước gốc đó.
