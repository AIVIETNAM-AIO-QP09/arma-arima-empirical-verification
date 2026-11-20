"""Mô phỏng (luôn nhận rng: numpy.random.Generator, sinh từ SEED = 3179)."""
from typing import Callable

import numpy as np
from scipy.signal import lfilter

from .config import SEED


def child_rng(*key: int) -> np.random.Generator:
    """Generator con sinh từ SEED = 3179 và khóa của mục (ví dụ child_rng(11, 3)): kết quả không phụ thuộc thứ tự chạy ô."""
    return np.random.default_rng([SEED, *key])


def simulate_arma(phi, theta, n: int, rng: np.random.Generator, sigma: float = 1.0, burn: int = 200) -> np.ndarray:
    """Chuỗi ARMA(p,q) có nhiễu N(0, σ²), bỏ `burn` giá trị đầu (như burn-in 200 của bài giảng)."""
    eps = sigma * rng.normal(size=n + burn)
    y = lfilter(np.r_[1.0, np.asarray(theta, dtype=float)], np.r_[1.0, -np.asarray(phi, dtype=float)], eps)
    return y[burn:]


def simulate_ar1(phi: float, n: int, rng: np.random.Generator, sigma: float = 1.0, burn: int = 200) -> np.ndarray:
    return simulate_arma([phi], [], n, rng, sigma, burn)


def simulate_random_walk(n: int, rng: np.random.Generator, delta: float = 0.0, sigma: float = 1.0,
                         y0: float = 0.0) -> np.ndarray:
    """Yₜ = Y₀ + δt + Σ_{j≤t} εⱼ, t = 1..n (Bài 12, Định lý 1), εⱼ ~ N(0, σ²)."""
    return y0 + np.cumsum(delta + sigma * rng.normal(size=n))


def coverage_study(simulate: Callable, interval: Callable, truth: float, B: int, rng: np.random.Generator) -> dict:
    """Độ phủ của khoảng tin cậy qua B lần lặp.

    simulate(rng) → một chuỗi; interval(y) → (lo, hi). Trả về độ phủ và MCSE = √{p(1−p)/B}.
    """
    hits = 0
    for _ in range(B):
        lo, hi = interval(simulate(rng))
        hits += lo <= truth <= hi
    p = hits / B
    return {"coverage": p, "mcse": float(np.sqrt(p * (1 - p) / B)), "B": B}
