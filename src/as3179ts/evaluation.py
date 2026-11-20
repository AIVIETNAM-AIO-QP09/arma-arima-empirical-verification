"""Thước đo độ chính xác, gốc cuốn chiếu và kiểm định Diebold–Mariano (Bài 12, Định nghĩa 5, Định lý 6)."""
from typing import Callable

import numpy as np
from scipy import stats


def _err(actual, forecast) -> np.ndarray:
    return np.asarray(actual, dtype=float) - np.asarray(forecast, dtype=float)


def mae(actual, forecast) -> float:
    return float(np.mean(np.abs(_err(actual, forecast))))


def rmse(actual, forecast) -> float:
    return float(np.sqrt(np.mean(_err(actual, forecast) ** 2)))


def mape(actual, forecast) -> float:
    """MAPE theo %; không xác định khi có giá trị thực bằng 0 (Định lý 6(c))."""
    return float(100 * np.mean(np.abs(_err(actual, forecast) / np.asarray(actual, dtype=float))))


def mase(actual, forecast, y_train, s: int = 1) -> float:
    """MASE = MAE/Q, Q = (1/(n−s)) Σ_{t>s} |yₜ − yₜ₋ₛ| trên dữ liệu huấn luyện (s = 1 nếu không mùa vụ)."""
    y = np.asarray(y_train, dtype=float)
    return mae(actual, forecast) / float(np.mean(np.abs(y[s:] - y[:-s])))


def rolling_origin_forecast(y, fit_forecast: Callable, t0: int, h: int = 1):
    """Đánh giá gốc cuốn chiếu (Bài 12, Định nghĩa 5(c)).

    Với mỗi gốc t = t0..n−h: khớp lại trên y[:t] bằng `fit_forecast(y_train, h)` (trả về mảng h dự báo),
    lấy dự báo bước h cho y[t+h−1]. Trả về (actual, forecast), mỗi mảng có n − h − t0 + 1 phần tử.
    """
    y = np.asarray(y, dtype=float)
    origins = range(t0, len(y) - h + 1)
    forecast = np.array([np.asarray(fit_forecast(y[:t], h))[h - 1] for t in origins])
    return y[[t + h - 1 for t in origins]], forecast


def rolling_origin_horizons(y, fit_forecast: Callable, t0: int, H: int) -> dict:
    """Như rolling_origin_forecast nhưng cho mọi chân trời h = 1..H, mỗi gốc chỉ khớp một lần.

    Trả về {h: (actual, forecast)}; số gốc giảm dần theo h vì cuối mẫu không đủ dữ liệu.
    """
    y = np.asarray(y, dtype=float)
    out = {h: ([], []) for h in range(1, H + 1)}
    for t in range(t0, len(y)):
        hmax = min(H, len(y) - t)
        f = np.asarray(fit_forecast(y[:t], hmax))
        for h in range(1, hmax + 1):
            out[h][0].append(y[t + h - 1])
            out[h][1].append(f[h - 1])
    return {h: (np.array(a), np.array(f)) for h, (a, f) in out.items()}


def diebold_mariano(d, h: int = 1) -> tuple[float, float]:
    """DM = d̄ / √(v̂/m), v̂ ≈ Σ_{|k|<h} γ̂_d(k) (Bài 12, Định lý 6(d)); p-value dùng phân phối t với m − 1 bậc tự do
    (như mã Mục 6 của bài giảng). d_t = L(e₁ₜ) − L(e₂ₜ).

    shortcut: h > 1 dùng trọng số đều (không Bartlett) nên v̂ có thể âm, chỉ nên dùng với h nhỏ; nâng cấp thành HAC Bartlett khi cần.
    """
    d = np.asarray(d, dtype=float)
    m = len(d)
    c = d - d.mean()
    v = c @ c / (m - 1)  # h = 1: đúng var(ddof=1) của bài giảng
    for k in range(1, h):
        v += 2 * (c[k:] @ c[:-k]) / (m - 1)
    dm = d.mean() / np.sqrt(v / m)
    return float(dm), float(2 * stats.t.sf(abs(dm), m - 1))
