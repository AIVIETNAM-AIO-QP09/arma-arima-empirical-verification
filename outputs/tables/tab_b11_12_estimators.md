**Ước lượng AR(2) bằng Yule–Walker, OLS và cực đại hợp lý**

| Bộ | Phương pháp | φ̂₁ | SE(φ̂₁) | φ̂₂ | SE(φ̂₂) |
|---|---|---|---|---|---|
| LY | Yule–Walker | 1.35 | 0.065 | -0.72 | 0.065 |
| LY | OLS (AutoReg) | 1.384 | 0.063 | -0.7478 | 0.0631 |
| LY | ML (ARIMA) | 1.378 | 0.0616 | -0.7399 | 0.0615 |
| HU | Yule–Walker | 0.9714 | 0.0971 | -0.2754 | 0.0971 |
| HU | OLS (AutoReg) | 1.002 | 0.0957 | -0.2838 | 0.0974 |
| HU | ML (ARIMA) | 1.005 | 0.0964 | -0.2913 | 0.0989 |
| DR | Yule–Walker | -4.462e-4 | 0.0232 | -0.0267 | 0.0232 |
| DR | OLS (AutoReg) | -6.855e-4 | 0.0232 | -0.0268 | 0.0232 |
| DR | ML (ARIMA) | -4.299e-4 | 0.0232 | -0.0268 | 0.0232 |

*Ghi chú:* SE của Yule–Walker là SE tiệm cận $\sqrt{\operatorname{diag}(\hat\sigma^2\hat\Gamma_2^{-1}/n)}$.
