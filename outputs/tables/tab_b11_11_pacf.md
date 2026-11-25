**PACF mẫu: Durbin–Levinson tự cài đặt so với statsmodels, độ trễ vượt dải và bậc AR gợi ý**

| Bộ dữ liệu | α̂(1) − ρ̂(1) | α̂(2) − (ρ̂₂−ρ̂₁²)/(1−ρ̂₁²) | max\|PACF tay − pacf()\| | Dải ± | Độ trễ vượt dải (h≤20) | Bậc AR gợi ý (số độ trễ vượt dải liên tiếp từ h = 1) |
|---|---|---|---|---|---|---|
| HU (khử xu thế) | 0 | 0 | 1.665e-16 | 0.198 | [1, 2, 10] | 2 |
| LY | 0 | 0 | 2.706e-15 | 0.1836 | [1, 2, 4, 7, 10, 11] | 2 |
| DR | 0 | 0 | 6.939e-18 | 0.0455 | [11, 17] | 0 |
