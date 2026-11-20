"""Style hình thống nhất và lưu hình vào outputs/figures/ (PNG 300 dpi, tên fig_b<bài>_<mục>_<nội dung>)."""
import matplotlib

matplotlib.use("Agg")  # chạy không cần màn hình (nbconvert, run_all)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from cycler import cycler  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

from .config import FIG_DIR  # noqa: E402

# Bảng màu Okabe–Ito: phân biệt được khi in đen trắng và với người mù màu
BLUE, ORANGE, GREEN, RED, PURPLE, SKY, GREY = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#6b6b6b"

plt.rcParams.update({
    "figure.figsize": (7.5, 3.8), "figure.facecolor": "white", "savefig.facecolor": "white",
    "axes.prop_cycle": cycler(color=[BLUE, ORANGE, GREEN, RED, PURPLE, SKY]),
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 8.5, "legend.frameon": True, "legend.framealpha": 0.9, "legend.edgecolor": "#cccccc",
    "lines.linewidth": 1.3, "font.size": 10, "axes.unicode_minus": True,
})


def save_figure(fig, name: str) -> str:
    """Lưu fig thành outputs/figures/<name>.png (300 dpi, nền trắng); trả về đường dẫn."""
    from .captions import caption_of

    caption_of(name)  # mọi hình phải có chú thích trong captions.py
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def show_figure(path: str):
    """Hiển thị hình đã lưu trong notebook (backend Agg không tự vẽ inline)."""
    import io

    from IPython.display import Image, display
    from PIL import Image as PILImage

    # nhúng bản thu nhỏ (rộng ≤ 1600 px) để notebook nhẹ; file PNG 300 dpi gốc vẫn nằm ở outputs/figures
    img = PILImage.open(path)
    img.thumbnail((1600, 1600))
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    display(Image(data=buf.getvalue(), width=760))


def panel_label(ax, text: str) -> None:
    """Nhãn panel đậm (a), (b), … ở góc trên trái, ngoài khung."""
    ax.text(-0.02, 1.12, text, transform=ax.transAxes, fontsize=12, fontweight="bold", va="bottom", ha="right")


def acf_bars(ax, values, n: int, title: str = "", band: float | None = None, start: int = 1, ylabel: str = "ACF",
             band_label: str | None = None, highlight: bool = True) -> None:
    """Biểu đồ ACF/PACF dạng que-chấm từ độ trễ `start`, kèm dải ±band (mặc định iid ±1.96/√n).

    Độ trễ vượt dải được tô màu cam đỏ; trục độ trễ chỉ có tick nguyên.
    """
    values = np.asarray(values, dtype=float)
    band = 1.96 / np.sqrt(n) if band is None else band
    lags = np.arange(start, len(values))
    v = values[start:]
    out = np.abs(v) > band if highlight else np.zeros(len(v), bool)
    ax.vlines(lags, 0, v, color=np.where(out, RED, BLUE), lw=2.0, zorder=3)
    ax.plot(lags, v, "o", ms=3, color=BLUE, zorder=4, mfc=BLUE)
    if out.any():
        ax.plot(lags[out], v[out], "o", ms=3, color=RED, zorder=5)
    ax.axhline(0, color="k", lw=0.8)
    ax.axhline(band, color=GREY, ls="--", lw=1)
    ax.axhline(-band, color=GREY, ls="--", lw=1)
    top = max(np.abs(v).max(), band) * 1.12
    ax.set_ylim(-top, top)
    last = len(values) - 1
    step = 1 if last <= 12 else (2 if last <= 24 else 5)
    ax.set_xticks(list(range(step, last + 1, step)) if step > 1 else list(range(start, last + 1)))
    ax.set_xlim(start - 0.8, last + 0.8)
    # thông tin dải đặt ở nhãn trục x (không dùng legend để không đè lên cột)
    ax.set(title=title, xlabel=f"độ trễ h    (- - - : {band_label or f'dải 95% ±{band:.3f}'})", ylabel=ylabel)


def overlay_theory(ax, lags, values, label: str):
    """Chồng đường lý thuyết lên biểu đồ ACF mẫu."""
    ax.plot(lags, values, "-o", color=ORANGE, ms=3.5, lw=1.4, label=label, zorder=6)
    ax.legend(loc="best")
