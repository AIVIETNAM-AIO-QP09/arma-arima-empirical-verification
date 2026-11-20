"""Công cụ AR/MA/ARMA theo Bài 11 (chỉ dùng numpy/scipy, không gọi statsmodels).

Quy ước: phi = [φ₁..φ_p], theta = [θ₁..θ_q] (không chứa hệ số 1 đứng đầu).
"""
import numpy as np
from scipy.linalg import solve, toeplitz

from .acf_tools import sample_autocov


def yule_walker_manual(y, p: int) -> tuple[np.ndarray, float]:
    """Yule–Walker: φ̂ = Γ̂ₚ⁻¹ γ̂ₚ, σ̂² = γ̂(0) − φ̂ᵀγ̂ₚ (Bài 11, Định lý 6(a)); γ̂ dùng mẫu số n.

    Trả về (phi_hat, sigma2_hat). Không hiệu chỉnh n/(n−p−1) như ar.yw của R.
    """
    g = sample_autocov(y, p)
    phi = solve(toeplitz(g[:p]), g[1 : p + 1])
    return phi, float(g[0] - phi @ g[1 : p + 1])


def ar_roots(phi) -> np.ndarray:
    """Nghiệm của φ(z) = 1 − φ₁z − … − φ_p z^p (Bài 11, Định lý 4(a))."""
    return np.roots(np.r_[-np.asarray(phi, dtype=float)[::-1], 1.0])


def ma_roots(theta) -> np.ndarray:
    """Nghiệm của θ(z) = 1 + θ₁z + … + θ_q z^q (khả nghịch ⇔ mọi |z| > 1, Định lý 5(b))."""
    return np.roots(np.r_[np.asarray(theta, dtype=float)[::-1], 1.0])


def ar_roots_modulus(phi) -> np.ndarray:
    """Môđun các nghiệm của φ(z); nhân quả ⇔ tất cả > 1."""
    return np.abs(ar_roots(phi))


def ar2_in_triangle(phi1: float, phi2: float) -> bool:
    """Tam giác nhân quả AR(2): φ₁+φ₂ < 1, φ₂−φ₁ < 1, |φ₂| < 1 (Bài 11, Mệnh đề 3)."""
    return phi1 + phi2 < 1 and phi2 - phi1 < 1 and abs(phi2) < 1


def ar2_period(phi1: float, phi2: float) -> float:
    """Chu kỳ 2π/ω của AR(2) có nghiệm phức (φ₁² + 4φ₂ < 0), cos ω = φ₁/(2r), r = √(−φ₂); NaN nếu nghiệm thực."""
    if phi1**2 + 4 * phi2 >= 0:
        return float("nan")
    return float(2 * np.pi / np.arccos(phi1 / (2 * np.sqrt(-phi2))))


def psi_weights(phi, theta, n: int) -> np.ndarray:
    """ψ₀..ψ_{n−1}, hệ số của ψ(z) = θ(z)/φ(z): ψⱼ = θⱼ + Σ_{i≤min(j,p)} φᵢψ_{j−i}, ψ₀ = 1 (Bài 11, Định lý 5(a))."""
    phi, theta = np.asarray(phi, dtype=float), np.asarray(theta, dtype=float)
    psi = np.zeros(n)
    psi[0] = 1.0
    for j in range(1, n):
        psi[j] = (theta[j - 1] if j <= len(theta) else 0.0) + sum(
            phi[i - 1] * psi[j - i] for i in range(1, min(j, len(phi)) + 1)
        )
    return psi


def theoretical_acvf(phi, theta, nlags: int, sigma2: float = 1.0, terms: int = 2000) -> np.ndarray:
    """γ(h) = σ² Σⱼ ψⱼψⱼ₊ₕ, h = 0..nlags (Bài 11, Mệnh đề 2); cắt chuỗi ở `terms` số hạng (đủ khi mô hình nhân quả)."""
    psi = psi_weights(phi, theta, terms + nlags)
    return sigma2 * np.array([psi[: terms] @ psi[h : h + terms] for h in range(nlags + 1)])


def theoretical_acf(phi, theta, nlags: int, terms: int = 2000) -> np.ndarray:
    """ρ(h) = γ(h)/γ(0), h = 0..nlags của ARMA nhân quả."""
    g = theoretical_acvf(phi, theta, nlags, 1.0, terms)
    return g / g[0]


def causal_invertible_check(phi, theta) -> dict:
    """Kiểm tra nhân quả (nghiệm φ ngoài vòng đơn vị) và khả nghịch (nghiệm θ ngoài vòng đơn vị).

    Trả về môđun nhỏ nhất của mỗi bên và khoảng cách nhỏ nhất giữa nghiệm AR và nghiệm MA
    (gần 0 ⇒ gần triệt tiêu nghiệm chung, Bài 11, Định lý 5 và Ví dụ 4.2).
    """
    ar, ma = ar_roots(phi), ma_roots(theta)
    gap = float(np.min(np.abs(ar[:, None] - ma[None, :]))) if len(ar) and len(ma) else float("nan")
    return {
        "causal": bool(len(ar) == 0 or np.all(np.abs(ar) > 1)),
        "invertible": bool(len(ma) == 0 or np.all(np.abs(ma) > 1)),
        "min_ar_modulus": float(np.abs(ar).min()) if len(ar) else float("nan"),
        "min_ma_modulus": float(np.abs(ma).min()) if len(ma) else float("nan"),
        "min_ar_ma_root_gap": gap,
    }


def ma1_ratio(theta: float) -> float:
    """ρ(1) = θ/(1 + θ²) của MA(1) (Bài 11, Mệnh đề 4(b)); |ρ(1)| ≤ 1/2."""
    return theta / (1 + theta**2)
