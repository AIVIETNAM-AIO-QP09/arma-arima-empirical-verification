"""Trọng số Ψ, phương sai sai số dự báo, chuyển ngược log, làm trơn mũ, mốc chuẩn (Bài 12). Không gọi statsmodels."""
import numpy as np


def psi_from_polys(ar_full, ma_full, n: int) -> np.ndarray:
    """Hệ số Ψ₀..Ψ_{n−1} của Ψ(z) = M(z)/A(z), với A, M là đa thức đầy đủ (hệ số đầu = 1, tăng dần theo bậc z).

    Đệ quy: Ψⱼ = Mⱼ − Σ_{i≥1} Aᵢ Ψ_{j−i}.
    """
    a, m = np.asarray(ar_full, dtype=float), np.asarray(ma_full, dtype=float)
    psi = np.zeros(n)
    for j in range(n):
        psi[j] = (m[j] if j < len(m) else 0.0) - sum(a[i] * psi[j - i] for i in range(1, min(j, len(a) - 1) + 1))
    return psi


def Psi_weights_arima(phi, theta, d: int, n: int) -> np.ndarray:
    """Ψ₀..Ψ_{n−1} của Ψ(z) = θ(z)/{φ(z)(1−z)^d} (Bài 12, Định lý 3(b), Định lý 4)."""
    ar = np.r_[1.0, -np.asarray(phi, dtype=float)]
    for _ in range(d):
        ar = np.polymul(ar, [1.0, -1.0])
    return psi_from_polys(ar, np.r_[1.0, np.asarray(theta, dtype=float)], n)


def sarima_polys(phi=(), theta=(), Phi=(), Theta=(), d: int = 0, D: int = 0, s: int = 12):
    """Đa thức AR, MA đầy đủ của SARIMA(p,d,q)(P,D,Q)ₛ (Bài 12, Định nghĩa 4(b)); AR đã nhân (1−z)^d (1−zˢ)^D.

    Trả về (ar_full, ma_full) để đưa vào psi_from_polys.
    """
    def seasonal(c):  # 1 + c₁zˢ + c₂z²ˢ + …
        out = np.zeros(len(c) * s + 1)
        out[0] = 1.0
        out[s :: s] = np.asarray(c, dtype=float)
        return out

    ar = np.polymul(np.r_[1.0, -np.asarray(phi, dtype=float)], seasonal(-np.asarray(Phi, dtype=float)))
    ma = np.polymul(np.r_[1.0, np.asarray(theta, dtype=float)], seasonal(Theta))
    for _ in range(d):
        ar = np.polymul(ar, [1.0, -1.0])
    for _ in range(D):
        ar = np.polymul(ar, np.r_[1.0, np.zeros(s - 1), -1.0])
    return ar, ma


def forecast_variance_manual(Psi, sigma2: float, H: int) -> np.ndarray:
    """Var eₙ(h) = σ² Σ_{j<h} Ψⱼ², h = 1..H (Bài 12, Định lý 4(a))."""
    return sigma2 * np.cumsum(np.asarray(Psi, dtype=float)[:H] ** 2)


def back_transform_log(m, s, z: float = 1.96) -> dict:
    """Dự báo trên thang log N(m, s²) → thang gốc (Bài 12, Mệnh đề 2).

    median = eᵐ, mean = e^{m+s²/2}, khoảng chuyển đổi chính xác (e^{m−zs}, e^{m+zs}).
    """
    m, s = np.asarray(m, dtype=float), np.asarray(s, dtype=float)
    return {"median": np.exp(m), "mean": np.exp(m + s**2 / 2), "lower": np.exp(m - z * s), "upper": np.exp(m + z * s)}


def ses_recursion(y, alpha: float, init: float | None = None) -> np.ndarray:
    """Đệ quy làm trơn mũ đơn ℓₜ = αyₜ + (1−α)ℓₜ₋₁, ℓ₁ = init (mặc định y₁) (Bài 12, Định lý 3(c)).

    Trả về ℓ₁..ℓₙ; dự báo mọi bước sau là ℓₙ. Với ARIMA(0,1,1): α = 1 + θ.
    """
    y = np.asarray(y, dtype=float)
    level = np.empty(len(y))
    level[0] = y[0] if init is None else init
    for t in range(1, len(y)):
        level[t] = alpha * y[t] + (1 - alpha) * level[t - 1]
    return level


def local_level_variances(theta: float, sigma2: float) -> tuple[float, float]:
    """(σ̂_ε², σ̂_η²) của mô hình mức cục bộ từ ARIMA(0,1,1): σ_ε² = −θσ², σ_η² = (1+θ)²σ² (Bài 12, Ví dụ 2.2)."""
    return -theta * sigma2, (1 + theta) ** 2 * sigma2


def zero_diffuse_residuals(resid, k: int) -> np.ndarray:
    """Đặt k phần dư đầu về 0 (k = d + D·s). statsmodels khởi tạo khuếch tán nên resid[0] ≈ giá trị quan sát (rất lớn);
    cách này giống R, nơi các phần dư khuếch tán gần 0, để ACF/Ljung–Box của phần dư không bị méo."""
    r = np.array(resid, dtype=float)
    r[:k] = 0.0
    return r


# --- Mốc chuẩn (Bài 12, Định nghĩa 5(a)); y là dữ liệu huấn luyện y₁..yₙ, trả về dự báo h = 1..H ---
def forecast_mean(y, H: int) -> np.ndarray:
    return np.full(H, np.mean(y))


def forecast_naive(y, H: int) -> np.ndarray:
    return np.full(H, np.asarray(y, dtype=float)[-1])


def forecast_seasonal_naive(y, H: int, s: int) -> np.ndarray:
    """ŷₙ₊ₕ = yₙ₊ₕ₋ₛ₍ₖ₊₁₎ với k = ⌊(h−1)/s⌋."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    return np.array([y[n + h - s * ((h - 1) // s + 1) - 1] for h in range(1, H + 1)])


def forecast_drift(y, H: int) -> np.ndarray:
    """ŷₙ₊ₕ = yₙ + h(yₙ − y₁)/(n − 1)."""
    y = np.asarray(y, dtype=float)
    return y[-1] + np.arange(1, H + 1) * (y[-1] - y[0]) / (len(y) - 1)
