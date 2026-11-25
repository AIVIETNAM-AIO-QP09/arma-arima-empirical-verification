**Kiểm định nghiệm đơn vị ADF (H$_0$: có nghiệm đơn vị) và KPSS (H$_0$: dừng)**

| Bộ | Chuỗi | Kiểm định | Hồi quy | Thống kê | p-value | Tới hạn 5% | Bác bỏ H₀ (5%) | Độ trễ |
|---|---|---|---|---|---|---|---|---|
| NI | y | ADF | hằng số | -4.049 | 0.0012 | -2.892 | Có | 1 |
| NI | y | ADF | hằng số + xu thế | -4.791 | 0.0005 | -3.456 | Có | 1 |
| NI | y | KPSS | hằng số | 0.8691 | ≤ 0.01 | 0.463 | Có | 5 |
| NI | y | KPSS | hằng số + xu thế | 0.2376 | ≤ 0.01 | 0.146 | Có | 4 |
| NI | ∇y | ADF | hằng số | -4.68 | <0.0001 | -2.895 | Có | 9 |
| NI | ∇y | KPSS | hằng số | 0.1171 | ≥ 0.10 | 0.463 | Không | 23 |
| AP | y | ADF | hằng số | -1.925 | 0.3206 | -2.889 | Không | 13 |
| AP | y | ADF | hằng số + xu thế | -1.575 | 0.8022 | -3.453 | Không | 13 |
| AP | y | KPSS | hằng số | 1.744 | ≤ 0.01 | 0.463 | Có | 6 |
| AP | y | KPSS | hằng số + xu thế | 0.0606 | ≥ 0.10 | 0.146 | Không | 4 |
| AP | ∇y | ADF | hằng số | -2.343 | 0.1584 | -2.889 | Không | 12 |
| AP | ∇y | KPSS | hằng số | 0.0296 | ≥ 0.10 | 0.463 | Không | 1 |
| DP | y | ADF | hằng số | 1.184 | 0.9959 | -2.863 | Không | 0 |
| DP | y | ADF | hằng số + xu thế | -1.361 | 0.8719 | -3.413 | Không | 0 |
| DP | y | KPSS | hằng số | 5.754 | ≤ 0.01 | 0.463 | Có | 27 |
| DP | y | KPSS | hằng số + xu thế | 1.139 | ≤ 0.01 | 0.146 | Có | 27 |
| DP | ∇y | ADF | hằng số | -43.06 | <0.0001 | -2.863 | Có | 0 |
| DP | ∇y | KPSS | hằng số | 0.4372 | 0.061 | 0.463 | Không | 9 |

*Ghi chú:* p-value của KPSS được nội suy từ bảng nên bị chặn trong $[0.01,0.10]$; ``$\le0.01$'' và ``$\ge0.10$'' nghĩa là ngoài khoảng bảng. Cột độ trễ: số hạng $\nabla Y_{t-i}$ của ADF (chọn theo AIC) hoặc độ trễ Newey--West của KPSS (`nlags='auto'`).
