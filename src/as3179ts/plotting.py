"""Style hình thống nhất và lưu hình vào reports/figures/ (PNG 300 dpi, tên ổn định, ví dụ bai11_LY_acf)."""
import matplotlib

matplotlib.use("Agg")  # chạy không cần màn hình (nbconvert, run_all)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .config import FIG_DIR  # noqa: E402

plt.rcParams.update({"figure.figsize": (7, 3.5), "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 10})


def save_figure(fig, name: str) -> str:
    """Lưu fig thành reports/figures/<name>.png (300 dpi); trả về đường dẫn."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    return str(path)


def show_figure(path: str):
    """Hiển thị hình đã lưu trong notebook (backend Agg không tự vẽ inline)."""
    from IPython.display import Image, display

    display(Image(filename=path, width=720))


def acf_bars(ax, values, n: int, title: str = "", band: float | None = None, start: int = 1) -> None:
    """Vẽ ACF/PACF dạng cột từ độ trễ `start`, kèm dải ±band (mặc định iid ±1.96/√n)."""
    band = 1.96 / np.sqrt(n) if band is None else band
    lags = np.arange(start, len(values))
    ax.vlines(lags, 0, np.asarray(values)[start:], color="C0")
    ax.axhline(0, color="k", lw=0.8)
    ax.axhline(band, color="C3", ls="--", lw=0.8)
    ax.axhline(-band, color="C3", ls="--", lw=0.8)
    ax.set(title=title, xlabel="độ trễ h")
