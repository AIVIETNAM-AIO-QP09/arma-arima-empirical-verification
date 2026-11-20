"""Tái lập từng con số "Kết quả kỳ vọng" của Bài 11–12 (docs/reference_values.md) bằng đúng lệnh Python của Mục 6.

Dung sai = độ chính xác làm tròn mà bài giảng in. KHÔNG sửa giá trị kỳ vọng cho test xanh: số nào lệch thì đánh
xfail trong XFAIL kèm lý do đã điều tra. Bảng so sánh được ghi ra outputs/tables/lecture_reference_check.md.
"""
import warnings
from functools import cache

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from scipy import stats
from statsmodels.regression.linear_model import yule_walker
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import acf, adfuller, coint, kpss

from as3179ts.config import SEED, TABLE_DIR
from as3179ts.data import load_processed, load_raw
from as3179ts import evaluation as E, forecast_tools as F
from as3179ts.reporting import to_markdown

warnings.filterwarnings("ignore")


def _lb(resid, lags, df):
    r = acorr_ljungbox(resid, lags=[lags], model_df=df)
    return float(r["lb_stat"].iloc[0]), float(r["lb_pvalue"].iloc[0])


@cache
def g_hu():
    d = load_processed("HU")
    y, x = d["level_ft"].to_numpy(), d["x_centered"].to_numpy(dtype=float)
    out = {}
    for o, nm in [((1, 0, 0), "ar1"), ((2, 0, 0), "ar2"), ((0, 0, 2), "ma2"), ((1, 0, 1), "arma11")]:
        m = ARIMA(y, exog=x, order=o).fit()
        out[f"aic_{nm}"], out[f"bic_{nm}"] = m.aic, m.bic
    m = ARIMA(y, exog=x, order=(2, 0, 0)).fit(cov_type="oim")
    p, se = dict(zip(m.param_names, m.params)), dict(zip(m.param_names, m.bse))
    out.update(phi1=p["ar.L1"], phi2=p["ar.L2"], slope=p["x1"], slope_se=se["x1"], sigma2=p["sigma2"])
    out["lb10"], out["lb10_p"] = _lb(m.resid, 10, 2)
    ols = sm.OLS(y, sm.add_constant(x)).fit()
    out["ols_slope"], out["ols_slope_se"] = ols.params[1], ols.bse[1]
    return out


@cache
def g_ly():
    y = load_processed("LY")["log10_count"].to_numpy()
    r = acf(y, nlags=2, fft=False)
    phi, sig = yule_walker(y, order=2, method="mle")
    z = np.roots([-phi[1], -phi[0], 1])
    fits = [ARIMA(y, order=(p, 0, 0)).fit() for p in range(1, 15)]
    return {"n": len(y), "gamma0": float(np.var(y)), "rho1": r[1], "rho2": r[2], "phi1": phi[0], "phi2": phi[1],
            "sigma2": sig**2, "root_mod": abs(z).mean(), "period": 2 * np.pi / abs(np.angle(z[0])),
            "aic_p": int(np.argmin([m.aic for m in fits])) + 1, "bic_p": int(np.argmin([m.bic for m in fits])) + 1,
            "lb20_p_ar2": _lb(fits[1].resid, 20, 2)[1], "lb20_p_ar11": _lb(fits[10].resid, 20, 11)[1]}


@cache
def g_sim():
    rng = np.random.default_rng(SEED)
    phi, n, B = 0.6, 100, 2000
    tau = (1 + phi) / (1 - phi)
    naive = fixed = 0
    for _ in range(B):
        e = rng.normal(size=n + 200)
        y = 0 * e
        for t in range(1, n + 200):
            y[t] = phi * y[t - 1] + e[t]
        y = y[200:]
        s = y.std(ddof=1)
        naive += abs(y.mean()) < 1.96 * s / np.sqrt(n)
        fixed += abs(y.mean()) < 1.96 * s * np.sqrt(tau / n)
    return {"cover_naive": naive / B, "cover_corrected": fixed / B}


@cache
def g_dr():
    r = load_processed("DR")["ret_pct"].to_numpy()
    q1, p1 = _lb(r, 10, 0)
    q2, p2 = _lb(r**2, 10, 0)
    return {"n": len(r), "mean": r.mean(), "sd": r.std(ddof=1), "lb_r": q1, "lb_r_p": p1, "lb_r2": q2, "lb_r2_p": p2}


@cache
def g_ni():
    d = load_processed("NI")
    y = d["flow"].to_numpy()
    f = ARIMA(y, order=(0, 1, 1), trend="n").fit()
    f_approx = ARIMA(y, order=(0, 1, 1), trend="n").fit(cov_type="approx")
    th, s2 = f.params[0], f.params[1]
    fc = f.get_forecast(10)
    m, s = fc.predicted_mean, np.sqrt(fc.var_pred_mean)
    level = F.ses_recursion(y, 1 + th)[-1]
    eps, eta = F.local_level_variances(th, s2)
    q, p = _lb(F.zero_diffuse_residuals(f.resid, 1), 12, 1)
    return {"n": len(y), "mean": y.mean(), "sd": y.std(ddof=1), "mean_pre1899": y[d.year < 1899].mean(),
            "theta": th, "sigma2": s2, "aic": f.aic, "se_default": f.bse[0], "se_approx": f_approx.bse[0],
            "lb12": q, "lb12_p": p, "fc1": m[0], "lo1": m[0] - 1.96 * s[0], "hi1": m[0] + 1.96 * s[0],
            "lo10": m[9] - 1.96 * s[9], "hi10": m[9] + 1.96 * s[9], "alpha": 1 + th, "ses_minus_arima": level - m[0],
            "sig2_eps": eps, "sig2_eta": eta, "adf_c": adfuller(y, regression="c")[0],
            "adf_ct": adfuller(y, regression="ct")[0], "kpss": kpss(y, nlags="auto")[0]}


def _airline(z):
    return SARIMAX(z, order=(0, 1, 1), trend="n", seasonal_order=(0, 1, 1, 12)).fit(disp=0)


@cache
def g_ap():
    ap = load_processed("AP")["passengers"].to_numpy(dtype=float)
    ly = np.log(ap)
    tr = ly[:120]
    d12 = tr[12:] - tr[:-12]
    dd = np.diff(d12)
    a = acf(dd, nlags=13)
    out = {"sd_tr": tr.std(ddof=1), "sd_d": np.diff(tr).std(ddof=1), "sd_d12": d12.std(ddof=1), "sd_dd12": dd.std(ddof=1),
           "acf1": a[1], "acf11": a[11], "acf12": a[12], "acf13": a[13]}
    f = _airline(tr)
    q, p = _lb(F.zero_diffuse_residuals(f.resid, 13), 24, 2)
    out.update(theta=f.params[0], Theta=f.params[1], sigma2=f.params[2], aic=f.aic, lb24=q)
    g = f.get_forecast(24)
    m, s = g.predicted_mean, np.sqrt(g.var_pred_mean)
    bt = F.back_transform_log(m, s)
    for tag, i in (("jan59", 0), ("dec60", 23)):
        out.update({f"{tag}_median": bt["median"][i], f"{tag}_mean": bt["mean"][i], f"{tag}_lo": bt["lower"][i],
                    f"{tag}_hi": bt["upper"][i]})
    yt, train = ap[120:], ap[:120]
    Q = np.abs(ap[12:120] - ap[:108]).mean()
    fcs = {"airline": bt["median"], "snaive": np.r_[ap[108:120], ap[108:120]],
           "drift": ap[119] + np.arange(1, 25) * (ap[119] - ap[0]) / 119, "naive": np.repeat(ap[119], 24)}
    for k, fc in fcs.items():
        e = yt - fc
        out.update({f"{k}_rmse": np.sqrt((e**2).mean()), f"{k}_mae": np.abs(e).mean(),
                    f"{k}_mape": 100 * np.abs(e / yt).mean(), f"{k}_mase": np.abs(e).mean() / Q})
    ea, es = [], []
    for t in range(120, 144):
        ea.append(ap[t] - np.exp(_airline(ly[:t]).get_forecast(1).predicted_mean[0]))
        es.append(ap[t] - ap[t - 12])
    ea, es = np.array(ea), np.array(es)
    dm, pv = E.diebold_mariano(ea**2 - es**2)
    out.update(ro_rmse_airline=np.sqrt((ea**2).mean()), ro_rmse_snaive=np.sqrt((es**2).mean()), dm=dm, dm_p=pv)
    return out


@cache
def g_dp():
    d = load_processed("DP")
    ly = d["log_close"].to_numpy()
    n_tr = 1500
    tr, te = ly[:n_tr], ly[n_tr:]
    prev = ly[n_tr - 1 : -1]  # giá trị liền trước mỗi điểm kiểm định
    out = {"n": len(d), "last": d["dax_close"].iloc[-1]}
    delta = (tr[-1] - tr[0]) / (n_tr - 1)
    arima = ARIMA(tr, order=(1, 1, 0), trend="n").fit()
    # extend giữ tham số, nạp dữ liệu kiểm định; fittedvalues = dự báo 1 bước cho từng điểm kiểm định
    fc_arima = arima.extend(te).fittedvalues
    for k, fc in (("naive", prev), ("drift", prev + delta), ("arima110", fc_arima)):
        e = 100 * (te - fc)
        out[f"{k}_rmse"], out[f"{k}_mae"] = np.sqrt((e**2).mean()), np.abs(e).mean()
    return out


@cache
def g_ext():
    raw = load_raw("EuStockMarkets")
    x, y = np.log(raw["SMI"].to_numpy()), np.log(raw["DAX"].to_numpy())
    ols = sm.OLS(y, sm.add_constant(x)).fit()
    return {"beta": ols.params[1], "r2": ols.rsquared, "eg_p": coint(y, x)[1]}


GROUPS = {"hu": g_hu, "ly": g_ly, "sim": g_sim, "dr": g_dr, "ni": g_ni, "ap": g_ap, "dp": g_dp, "ext": g_ext}

# (nhóm, khóa, giá trị bài giảng, dung sai tuyệt đối, mô tả)
C = []
def case(group, key, expected, tol, desc=None):  # noqa: E302
    C.append((group, key, expected, tol, desc or f"{group}.{key}"))

for nm, a, b in [("ar1", 218.45, 228.79), ("ar2", 212.40, 225.32), ("ma2", 219.75, 232.68), ("arma11", 212.40, 225.32)]:
    case("hu", f"aic_{nm}", a, 0.005, f"HU AIC {nm}"); case("hu", f"bic_{nm}", b, 0.005, f"HU BIC {nm}")
case("hu", "phi1", 1.0048, 5e-5, "HU AR(2) φ̂₁"); case("hu", "phi2", -0.2913, 5e-5, "HU AR(2) φ̂₂")
case("hu", "slope", -0.0216, 5e-5, "HU AR(2) hệ số dốc"); case("hu", "slope_se", 0.0081, 5e-5, "HU AR(2) SE dốc")
case("hu", "sigma2", 0.4566, 5e-5, "HU AR(2) σ̂²"); case("hu", "lb10", 3.95, 0.005, "HU Q_LB(10) AR(2), model_df=2 (Python)")
case("hu", "lb10_p", 0.86, 0.005, "HU p-value Q_LB(10)")
case("hu", "ols_slope", -0.0242, 5e-5, "HU OLS hệ số dốc"); case("hu", "ols_slope_se", 0.0040, 5e-5, "HU OLS SE dốc")
case("ly", "n", 114, 0, "LY n"); case("ly", "gamma0", 0.309, 5e-4, "LY γ̂(0)")
case("ly", "rho1", 0.785, 5e-4, "LY ρ̂(1)"); case("ly", "rho2", 0.340, 5e-4, "LY ρ̂(2)")
case("ly", "phi1", 1.350, 5e-4, "LY YW φ̂₁"); case("ly", "phi2", -0.720, 5e-4, "LY YW φ̂₂")
case("ly", "sigma2", 0.057, 5e-4, "LY YW σ̂² (Python)"); case("ly", "root_mod", 1.178, 5e-4, "LY môđun nghiệm")
case("ly", "period", 9.66, 5e-3, "LY chu kỳ (năm)"); case("ly", "aic_p", 11, 0, "LY AIC chọn p"); case("ly", "bic_p", 2, 0, "LY BIC chọn p")
case("ly", "lb20_p_ar2", 0.009, 5e-4, "LY p Ljung–Box AR(2), lag 20"); case("ly", "lb20_p_ar11", 0.52, 5e-3, "LY p Ljung–Box AR(11), lag 20")
case("sim", "cover_naive", 0.67, 5e-3, "Mô phỏng ĐL 1: độ phủ ngây thơ (Python)")
case("sim", "cover_corrected", 0.94, 0.01, "Mô phỏng ĐL 1: độ phủ đã hiệu chỉnh √τ (bài giảng in giá trị R)")
case("dr", "n", 1859, 0, "DR n"); case("dr", "mean", 0.065, 5e-4, "DR trung bình"); case("dr", "sd", 1.03, 5e-3, "DR SD")
case("dr", "lb_r", 6.37, 0.005, "DR Q_LB(10) của r"); case("dr", "lb_r_p", 0.78, 0.005, "DR p của r")
case("dr", "lb_r2", 110.7, 0.05, "DR Q_LB(10) của r²"); case("dr", "lb_r2_p", 4e-19, 0.5e-19, "DR p của r² (≈ 4×10⁻¹⁹)")
case("ni", "n", 100, 0, "NI n"); case("ni", "mean", 919, 0.5, "NI trung bình"); case("ni", "sd", 169, 0.5, "NI SD")
case("ni", "mean_pre1899", 1098, 0.5, "NI trung bình trước 1899")
case("ni", "theta", -0.733, 5e-4, "NI θ̂"); case("ni", "sigma2", 20600, 50, "NI σ̂²"); case("ni", "aic", 1269.1, 0.05, "NI AIC")
case("ni", "se_default", 0.074, 5e-4, "NI SE θ̂ mặc định statsmodels"); case("ni", "se_approx", 0.114, 5e-4, "NI SE θ̂ cov_type='approx'")
case("ni", "lb12", 13.7, 0.05, "NI Q_LB(12), df 11"); case("ni", "lb12_p", 0.25, 0.005, "NI p Q_LB(12)")
case("ni", "fc1", 798, 0.6, "NI dự báo"); case("ni", "lo1", 517, 0.6, "NI cận dưới h=1"); case("ni", "hi1", 1080, 0.6, "NI cận trên h=1")
case("ni", "lo10", 438, 0.6, "NI cận dưới h=10"); case("ni", "hi10", 1159, 0.6, "NI cận trên h=10")
case("ni", "alpha", 0.267, 5e-4, "NI α = 1 + θ̂"); case("ni", "ses_minus_arima", 0.0, 1.0, "NI làm trơn mũ − dự báo ARIMA")
# Bài giảng tính từ θ̂ = −0.733, σ̂² = 20 600 đã làm tròn (−θσ² = 15 099.8) nên dung sai theo sai số làm tròn của σ̂² (±50)
case("ni", "sig2_eps", 15099, 40, "NI σ̂_ε² (dẫn xuất từ số làm tròn)"); case("ni", "sig2_eta", 1469, 10, "NI σ̂_η² (dẫn xuất từ số làm tròn)")
case("ni", "adf_c", -4.05, 5e-3, "NI ADF 'c'"); case("ni", "adf_ct", -4.79, 5e-3, "NI ADF 'ct'"); case("ni", "kpss", 0.87, 5e-3, "NI KPSS")
for k, v in [("sd_tr", 0.392), ("sd_d", 0.106), ("sd_d12", 0.066), ("sd_dd12", 0.046)]:
    case("ap", k, v, 5e-4, f"AP {k}")
for k, v in [("acf1", -0.33), ("acf11", 0.08), ("acf12", -0.41), ("acf13", 0.18)]:
    case("ap", k, v, 5e-3, f"AP ACF ∇∇₁₂ {k}")
case("ap", "theta", -0.342, 5e-4, "AP θ̂"); case("ap", "Theta", -0.541, 5e-4, "AP Θ̂"); case("ap", "sigma2", 0.00140, 5e-6, "AP σ̂²")
case("ap", "aic", -389.0, 0.05, "AP AIC"); case("ap", "lb24", 20.3, 0.05, "AP Q_LB(24), df 22")
for tag, vals in (("jan59", (348.6, 348.8, 324, 375)), ("dec60", (388.1, 392.8, 286, 526))):
    for k, v, tol in zip(("median", "mean", "lo", "hi"), vals, (0.05, 0.05, 0.6, 0.6)):
        case("ap", f"{tag}_{k}", v, tol, f"AP {tag} {k}")
for k, vals in {"airline": (43.2, 39.5, 8.5, 1.38), "snaive": (77.0, 71.3, 15.5, 2.49),
                "drift": (115.7, 91.6, 18.4, 3.21), "naive": (137.3, 115.3, 23.6, 4.03)}.items():
    for m_, v, tol in zip(("rmse", "mae", "mape", "mase"), vals, (0.05, 0.05, 0.05, 0.005)):
        case("ap", f"{k}_{m_}", v, tol, f"AP giữ lại 24 tháng: {k} {m_.upper()}")
case("ap", "ro_rmse_airline", 15.3, 0.05, "AP gốc cuốn chiếu RMSE airline"); case("ap", "ro_rmse_snaive", 50.0, 0.05, "AP gốc cuốn chiếu RMSE naive mùa vụ")
case("ap", "dm", -7.49, 0.005, "AP Diebold–Mariano"); case("ap", "dm_p", 0.0, 1e-6, "AP p-value DM (< 10⁻⁶)")
case("dp", "n", 1860, 0, "DP n"); case("dp", "last", 5473.72, 0.005, "DP giá cuối")
for k, (r_, m_) in {"naive": (1.439, 1.094), "drift": (1.435, 1.092), "arima110": (1.439, 1.094)}.items():
    case("dp", f"{k}_rmse", r_, 5e-4, f"DP 1 bước {k} RMSE (%)"); case("dp", f"{k}_mae", m_, 5e-4, f"DP 1 bước {k} MAE (%)")
case("ext", "beta", 0.820, 5e-4, "⋆ hồi quy log DAX ~ log SMI: β̂"); case("ext", "r2", 0.965, 5e-4, "⋆ R²")
case("ext", "eg_p", 0.28, 5e-3, "⋆ Engle–Granger p")

# Số lệch đã điều tra: {khóa "nhóm.khóa": lý do}. Điền sau lần chạy đầu tiên, không sửa giá trị kỳ vọng.
_R_RESID = ("Bài giảng in giá trị của R (Box.test trên arima); statsmodels khác quy ước khởi tạo/phần dư đầu. "
            "Đã thử đặt phần dư khuếch tán đầu về 0 như R, vẫn lệch nhẹ. Kết luận (không bác bỏ trắng) không đổi.")
_FLAT = ("Log-likelihood phẳng quanh cực đại: 4 bộ tối ưu (lbfgs, nm, bfgs, powell) đều cho θ̂ ≈ −0.3425 và log-lik tại "
         "(−0.342, −0.541) chỉ thấp hơn 2e-6. Lệch ≤ 0.06 ở số in, do dung sai tối ưu R vs statsmodels.")
XFAIL: dict[str, str] = {
    "ly.lb20_p_ar11": f"p = 0.6185 (AR(11) hội tụ, AIC chọn p = 11 khớp; AR(2) p = 0.009 khớp). {_R_RESID}",
    "sim.cover_corrected": "Bài giảng in 0.94 là của R. Python seed 3179 cho 0.950, cách 0.94 khoảng 2 MCSE (0.005); "
                           "R và NumPy dùng dòng số ngẫu nhiên khác nhau.",
    "ni.se_approx": "0.1145 so với 0.114 (làm tròn lệch 5e-4): Hessian số của statsmodels khác R nhẹ.",
    "ni.lb12": f"Q = 13.57 (resid[0] = 1120 là phần dư khuếch tán, đã đặt 0); bài giảng 13.7. {_R_RESID}",
    "ni.lb12_p": f"p = 0.258 so với 0.25. {_R_RESID}",
    "ap.lb24": f"Q = 19.76 (13 phần dư khuếch tán đầu đặt 0); bài giảng 20.3. {_R_RESID}",
    "ap.theta": f"θ̂ = −0.3425 so với −0.342. {_FLAT}",
    "ap.dec60_median": f"388.156 so với 388.1. {_FLAT}",
    "ap.airline_mae": f"39.44 so với 39.5. {_FLAT}",
}


def _param(c):
    g, k, exp, tol, desc = c
    marks = [pytest.mark.xfail(reason=XFAIL[f"{g}.{k}"], strict=False)] if f"{g}.{k}" in XFAIL else []
    return pytest.param(g, k, exp, tol, id=f"{g}.{k}", marks=marks)


@pytest.mark.parametrize("group,key,expected,tol", [_param(c) for c in C])
def test_lecture_value(group, key, expected, tol):
    got = GROUPS[group]()[key]
    assert abs(got - expected) <= tol, f"bài giảng {expected}, tái lập {got}"


def test_zz_write_table():
    rows = []
    for g, k, exp, tol, desc in C:
        got = float(GROUPS[g]()[k])
        ok = abs(got - exp) <= tol
        status = "Khớp" if ok else ("Lệch nhẹ (xfail)" if f"{g}.{k}" in XFAIL else "LỆCH")
        rows.append({"nội dung": desc, "giá trị bài giảng": exp, "giá trị tái lập": got, "dung sai": tol, "kết quả": status,
                     "lý do (nếu lệch)": XFAIL.get(f"{g}.{k}", "")})
    df = pd.DataFrame(rows)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    n_ok = int((df["kết quả"] == "Khớp").sum())
    fmt = {"Giá trị bài giảng": "{:.6g}", "Giá trị tái lập": "{:.6g}", "Dung sai": "{:.3g}"}
    caption = f"Đối chiếu giá trị in trong bài giảng với giá trị tái lập bằng code ({n_ok}/{len(df)} khớp trong dung sai làm tròn)"
    (TABLE_DIR / "lecture_reference_check.md").write_text(to_markdown(df, caption, fmt), encoding="utf-8")
    df.to_csv(TABLE_DIR / "lecture_reference_check.csv", index=False, encoding="utf-8-sig")
