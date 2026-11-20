import numpy as np
import pytest

from as3179ts.data import load_processed

# (mã, số dòng, mốc đầu, mốc cuối)
SPEC = [("HU", 98, 1875, 1972), ("LY", 114, 1821, 1934), ("DR", 1859, 2, 1860),
        ("NI", 100, 1871, 1970), ("AP", 144, "1949-01", "1960-12"), ("DP", 1860, 1, 1860)]


@pytest.mark.parametrize("code,n,first,last", SPEC)
def test_shape_and_time(code, n, first, last):
    df = load_processed(code)
    assert len(df) == n
    assert not df.isna().any().any() and not df.duplicated().any()
    assert df.iloc[0, 0] == first and df.iloc[-1, 0] == last
    assert df.iloc[:, 0].is_monotonic_increasing


def test_positive_before_log():
    assert (load_processed("LY")["count"] > 0).all()
    assert (load_processed("AP")["passengers"] > 0).all()
    assert (load_processed("DP")["dax_close"] > 0).all()


def test_splits():
    ap, dp = load_processed("AP"), load_processed("DP")
    assert (ap.split == "train").sum() == 120 and (ap.split == "test").sum() == 24
    assert (dp.split == "train").sum() == 1500 and (dp.split == "test").sum() == 360


def test_lecture_numbers():
    hu, dr, ni, dp = (load_processed(c) for c in ("HU", "DR", "NI", "DP"))
    assert round(hu.level_ft.mean(), 1) == 579.0 and round(hu.level_ft.std(), 2) == 1.32
    assert round(dr.ret_pct.mean(), 3) == 0.065 and round(dr.ret_pct.std(), 2) == 1.03
    assert round(ni.flow.mean()) == 919 and round(ni.flow.std()) == 169
    assert round(ni.flow[ni.year < 1899].mean()) == 1098
    assert dp.dax_close.iloc[-1] == 5473.72
    # DAX: time đúng như time() của R, không có ngày lịch
    assert np.isclose(dp.time.iloc[0], 1991 + 129 / 260)
    assert "date" not in dp.columns
