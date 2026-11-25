**Nhiễu iid $N(0,1)$, $n=200$, $B=2000$: tần suất vượt dải và phân phối của $Q_{LB}(10)$**

| Đại lượng | Mô phỏng | Lý thuyết (tiệm cận) | Xấp xỉ mẫu hữu hạn | MCSE |
|---|---|---|---|---|
| Tỷ lệ \|ρ̂(h)\| vượt ±1.96/√n (h = 1..20) | 0.0435 | 0.05 | 0.0436 | 0.0011 |
| Tỷ lệ Q_LB(10) > phân vị 95% của χ²₁₀ | 0.0615 | 0.05 | – | 0.0049 |
| Trung bình của Q_LB | 10.08 | 10 | – | 0.1058 |
| Phương sai của Q_LB | 22.41 | 20 | – | – |
| p-value kiểm định KS so với χ²₁₀ | 0.4655 | – | – | – |

*Ghi chú:* Xấp xỉ mẫu hữu hạn dùng $\E\hat\rho(h)\approx-1/n$ và $\Var\hat\rho(h)\approx(n-h)/\{n(n+2)\}$, lấy trung bình theo $h=1,\dots,20$. MCSE của tỷ lệ vượt dải coi $20B$ chỉ báo là độc lập.
