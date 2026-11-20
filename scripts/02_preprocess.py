"""Sinh 6 file data/processed/*.csv từ data/raw/ theo đúng biến đổi của bài giảng, kèm kiểm tra và bảng tóm tắt."""
import numpy as np
import pandas as pd

from as3179ts.config import (
    AP_TEST_N, AP_TRAIN_N, DAX_FREQ, DAX_START_TIME, DATA_PROCESSED, DATA_RAW, DP_TEST_N, DP_TRAIN_N,
)


def check(df: pd.DataFrame, name: str, n: int, time_col: str) -> None:
    """Kiểm tra số dòng, NA, trùng lặp, đơn điệu thời gian."""
    assert len(df) == n, f"{name}: {len(df)} dòng, kỳ vọng {n}"
    assert not df.isna().any().any(), f"{name}: có NA"
    assert not df.duplicated().any(), f"{name}: có dòng trùng"
    assert df[time_col].is_monotonic_increasing and df[time_col].is_unique, f"{name}: thời gian không đơn điệu"


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    raw = lambda n: pd.read_csv(DATA_RAW / f"{n}.csv")  # noqa: E731

    # HU: không biến đổi; x = năm - 1920
    d = raw("LakeHuron")
    hu = pd.DataFrame({"year": d["time"].astype(int), "level_ft": d["value"]})
    hu["x_centered"] = hu["year"] - 1920
    check(hu, "HU", 98, "year"); assert hu.year.iloc[0] == 1875 and hu.year.iloc[-1] == 1972

    # LY: log10(count)
    d = raw("lynx")
    ly = pd.DataFrame({"year": d["time"].astype(int), "count": d["value"].astype(int)})
    assert (ly["count"] > 0).all(), "LY: count <= 0 trước khi log"
    ly["log10_count"] = np.log10(ly["count"])
    check(ly, "LY", 114, "year"); assert ly.year.iloc[0] == 1821 and ly.year.iloc[-1] == 1934

    # DAX: chỉ chỉ số ngày giao dịch t; time đúng như time() của R (start = c(1991,130), freq 260). KHÔNG có ngày lịch.
    dax = raw("EuStockMarkets")["DAX"].to_numpy()
    assert len(dax) == 1860 and (dax > 0).all()
    t = np.arange(1, len(dax) + 1)
    time = DAX_START_TIME + (t - 1) / DAX_FREQ
    log_p = np.log(dax)

    dr = pd.DataFrame({"t": t[1:], "time": time[1:], "dax_close": dax[1:], "ret_pct": 100 * np.diff(log_p)})
    check(dr, "DR", 1859, "t")

    dp = pd.DataFrame({"t": t, "time": time, "dax_close": dax, "log_close": log_p})
    dp["split"] = np.where(dp["t"] <= DP_TRAIN_N, "train", "test")
    check(dp, "DP", DP_TRAIN_N + DP_TEST_N, "t")

    # NI: post_1899 để thảo luận đổi mức
    d = raw("Nile")
    ni = pd.DataFrame({"year": d["time"].astype(int), "flow": d["value"]})
    ni["post_1899"] = (ni["year"] >= 1899).astype(int)
    check(ni, "NI", 100, "year"); assert ni.year.iloc[0] == 1871 and ni.year.iloc[-1] == 1970

    # AP: log; train 1949-01..1958-12, test 1959-01..1960-12
    d = raw("AirPassengers")
    k = np.rint((d["time"].to_numpy() - 1949) * 12).astype(int)  # time là số thực -> chỉ số tháng
    assert (k == np.arange(len(d))).all(), "AP: chỉ số tháng không liên tục"
    ap = pd.DataFrame({"month": pd.period_range("1949-01", periods=len(d), freq="M").astype(str),
                       "passengers": d["value"].astype(int)})
    assert (ap["passengers"] > 0).all()
    ap["log_passengers"] = np.log(ap["passengers"])
    ap["split"] = np.where(np.arange(len(ap)) < AP_TRAIN_N, "train", "test")
    check(ap, "AP", AP_TRAIN_N + AP_TEST_N, "month")
    assert ap.month.iloc[0] == "1949-01" and ap.month.iloc[-1] == "1960-12"

    files = {"HU_lakehuron": hu, "LY_lynx_log10": ly, "DR_dax_returns": dr,
             "NI_nile": ni, "AP_airpassengers": ap, "DP_dax_logprice": dp}
    for name, df in files.items():
        df.to_csv(DATA_PROCESSED / f"{name}.csv", index=False, encoding="utf-8")

    # Bảng tóm tắt
    spec = [("HU", hu, "level_ft", "year"), ("LY", ly, "log10_count", "year"), ("DR", dr, "ret_pct", "t"),
            ("NI", ni, "flow", "year"), ("AP", ap, "passengers", "month"), ("DP", dp, "log_close", "t")]
    rows = [(c, len(df), f"{df[tc].iloc[0]}..{df[tc].iloc[-1]}", v, df[v].mean(), df[v].std(ddof=1))
            for c, df, v, tc in spec]
    print(pd.DataFrame(rows, columns=["bộ", "n", "thời gian", "biến", "trung bình", "SD"]).to_string(index=False))
    print("\nĐối chiếu với bài giảng:")
    print(f"  HU trung bình {hu.level_ft.mean():.1f} (579.0), SD {hu.level_ft.std():.2f} (1.32)")
    print(f"  DR trung bình {dr.ret_pct.mean():.3f} (0.065), SD {dr.ret_pct.std():.2f} (1.03)")
    print(f"  NI trung bình {ni.flow.mean():.0f} (919), SD {ni.flow.std():.0f} (169), "
          f"trước 1899: {ni.flow[ni.year < 1899].mean():.0f} (1098)")
    print(f"  DAX cuối {dax[-1]:.2f} (5473.72)")


if __name__ == "__main__":
    main()
