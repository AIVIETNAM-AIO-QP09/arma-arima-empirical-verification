"""ACF, PACF, Ljung–Box cài đặt tay theo Bài 11 (chỉ dùng numpy/scipy, không gọi statsmodels)."""
import numpy as np
from scipy import stats
from scipy.linalg import toeplitz


def sample_autocov(y, nlags: int, denom: str = "n") -> np.ndarray:
    """γ̂(h), h = 0..nlags (Bài 11, Định nghĩa 3).

    denom="n": mẫu số n (mặc định, đảm bảo Γ̂ₙ xác định không âm);
    denom="n-h": mẫu số n − h (có thể mất tính xác định dương, Bài tập 4(1)).
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    d = y - y.mean()
    s = np.array([d[h:] @ d[: n - h] for h in range(nlags + 1)])
    return s / n if denom == "n" else s / (n - np.arange(nlags + 1))


def sample_acf(y, nlags: int, denom: str = "n") -> np.ndarray:
    """ρ̂(h) = γ̂(h)/γ̂(0), h = 0..nlags (Bài 11, Định nghĩa 3)."""
    g = sample_autocov(y, nlags, denom)
    return g / g[0]


def gamma_matrix(y, size: int, denom: str = "n") -> np.ndarray:
    """Ma trận Toeplitz Γ̂ = [γ̂(i − j)] cỡ size × size (Bài 11, Mệnh đề 1(c))."""
    return toeplitz(sample_autocov(y, size - 1, denom))


def bartlett_band(n: int, rho=None, q: int = 0, z: float = 1.96) -> float:
    """Nửa độ rộng dải 95% của ρ̂(h), h > q.

    q = 0: dải iid ±z/√n (Định lý 2(a)).
    q ≥ 1: Bartlett cho MA(q), ±z·√{(1 + 2Σ_{k≤q} ρ(k)²)/n} (Định lý 2(c)); rho[k] = ρ(k), rho[0] = 1.
    """
    if q == 0:
        return z / np.sqrt(n)
    return z * np.sqrt((1 + 2 * np.sum(np.asarray(rho)[1 : q + 1] ** 2)) / n)


def pacf_durbin_levinson(rho, nlags: int) -> np.ndarray:
    """PACF α(h) = φ_hh từ ACF, h = 0..nlags, bằng đệ quy Durbin–Levinson (Bài 11, Mệnh đề 5).

    φ_hh = {ρ(h) − Σ_{j<h} φ_{h−1,j} ρ(h−j)} / {1 − Σ_{j<h} φ_{h−1,j} ρ(j)};  φ_hj = φ_{h−1,j} − φ_hh φ_{h−1,h−j}.
    rho phải chứa ρ(0) = 1 ở vị trí 0 và ít nhất nlags + 1 phần tử.
    """
    rho = np.asarray(rho, dtype=float)
    out = np.ones(nlags + 1)
    phi = np.array([])
    for h in range(1, nlags + 1):
        num = rho[h] - phi @ rho[h - 1 : 0 : -1] if h > 1 else rho[1]
        den = 1 - phi @ rho[1:h] if h > 1 else 1.0
        phi_hh = num / den
        phi = np.append(phi - phi_hh * phi[::-1], phi_hh)
        out[h] = phi_hh
    return out


def ljung_box_manual(y, H: int, model_df: int = 0) -> tuple[float, float]:
    """Q_LB(H) = n(n+2) Σ_{h=1..H} ρ̂(h)²/(n−h) ~ χ²_{H−model_df} (Bài 11, Định lý 2(b)).

    model_df = p + q cho phần dư ARMA(p, q) (Bài 11, Mục 5). Trả về (Q, p-value).
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    r = sample_acf(y, H)[1:]
    q = n * (n + 2) * np.sum(r**2 / (n - np.arange(1, H + 1)))
    return float(q), float(stats.chi2.sf(q, H - model_df))
