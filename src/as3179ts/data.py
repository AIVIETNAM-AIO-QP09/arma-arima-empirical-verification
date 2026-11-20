"""Đọc dữ liệu: bản gốc (data/raw) và bản đã làm sạch (data/processed)."""
import pandas as pd

from .config import DATA_PROCESSED, DATA_RAW

PROCESSED_FILES = {
    "HU": "HU_lakehuron.csv",
    "LY": "LY_lynx_log10.csv",
    "DR": "DR_dax_returns.csv",
    "NI": "NI_nile.csv",
    "AP": "AP_airpassengers.csv",
    "DP": "DP_dax_logprice.csv",
}


def load_raw(name: str) -> pd.DataFrame:
    """Đọc CSV gốc, ví dụ load_raw('LakeHuron')."""
    return pd.read_csv(DATA_RAW / f"{name}.csv")


def load_processed(code: str) -> pd.DataFrame:
    """Đọc bộ đã làm sạch theo mã ∈ {HU, LY, DR, NI, AP, DP}."""
    return pd.read_csv(DATA_PROCESSED / PROCESSED_FILES[code])
