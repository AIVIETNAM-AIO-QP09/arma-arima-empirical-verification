**Sai số chuẩn của trung bình mẫu: giả định iid và có xét phụ thuộc**

| Bộ dữ liệu | n | K | SE iid | τ̂ (Bartlett) | SE hiệu chỉnh | τ̂ (AR(1)) | SE theo công thức đầy đủ, h ≤ n/4 | n_eff = n/τ̂ (Bartlett) |
|---|---|---|---|---|---|---|---|---|
| HU | 98 | 3 | 0.1332 | 3.087 | 0.2328 | 10.9 | 0.4064 | 31.75 |
| LY | 114 | 4 | 0.0523 | 2.361 | 0.08 | 8.308 | – | 48.28 |
| DR | 1859 | 7 | 0.0239 | 0.9163 | 0.0229 | 0.9991 | 0.0247 | 2028.8 |

*Ghi chú:* $\hat\tau$ Bartlett cắt cụt ở $K=\lfloor4(n/100)^{2/9}\rfloor$; $\hat\tau$ Bartlett luôn không âm nên dùng được cho cả ba bộ. Cột ``SE theo công thức đầy đủ'' dùng công thức đầy đủ của $\Var\bar Y$ thay $\hat\gamma$, chỉ dùng độ trễ $h\le n/4$; cắt cụt trọng số $(1-h/n)$ làm mất tính xác định dương, nên với ACF dao động (LY) tổng này âm và được ghi dấu –.
