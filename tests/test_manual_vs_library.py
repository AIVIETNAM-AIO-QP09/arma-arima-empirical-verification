"""Hàm cài đặt tay (as3179ts) phải khớp statsmodels trên dữ liệu thật."""
import warnings

import numpy as np
import pytest
from statsmodels.regression.linear_model import yule_walker
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma2ma, arma_acf
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.stattools import acf, acovf, pacf

from as3179ts import acf_tools as A, arma_tools as R, evaluation as E, forecast_tools as F
from as3179ts.data import load_processed

warnings.filterwarnings("ignore")

SERIES = {
    "HU": lambda: load_processed("HU")["level_ft"].to_numpy(),
    "LY": lambda: load_processed("LY")["log10_count"].to_numpy(),
    "DR": lambda: load_processed("DR")["ret_pct"].to_numpy(),
    "NI": lambda: load_processed("NI")["flow"].to_numpy(),
    "AP": lambda: load_processed("AP")["log_passengers"].to_numpy(),
    "DP": lambda: load_processed("DP")["log_close"].to_numpy(),
}


@pytest.fixture(params=list(SERIES))
def y(request):
    return SERIES[request.param]()


def test_autocov_and_acf(y):
    np.testing.assert_allclose(A.sample_autocov(y, 20), acovf(y, adjusted=False, nlag=20), atol=1e-10)
    np.testing.assert_allclose(A.sample_acf(y, 20), acf(y, nlags=20, fft=False), atol=1e-10)
    np.testing.assert_allclose(A.sample_autocov(y, 20, "n-h"), acovf(y, adjusted=True, nlag=20), atol=1e-10)


def test_gamma_matrix_psd_with_n_denominator(y):
    assert np.linalg.eigvalsh(A.gamma_matrix(y, 30)).min() > -1e-9


def test_pacf_durbin_levinson(y):
    ours = A.pacf_durbin_levinson(A.sample_acf(y, 15), 15)
    np.testing.assert_allclose(ours, pacf(y, nlags=15, method="ldb"), atol=1e-8)


@pytest.mark.parametrize("model_df", [0, 2])
def test_ljung_box(y, model_df):
    q, p = A.ljung_box_manual(y, 10, model_df)
    ref = acorr_ljungbox(y, lags=[10], model_df=model_df)
    assert q == pytest.approx(ref["lb_stat"].iloc[0], abs=1e-8)
    assert p == pytest.approx(ref["lb_pvalue"].iloc[0], abs=1e-10)


@pytest.mark.parametrize("p", [1, 2, 5])
def test_yule_walker(y, p):
    phi, s2 = R.yule_walker_manual(y, p)
    ref_phi, ref_sigma = yule_walker(y, order=p, method="mle")
    np.testing.assert_allclose(phi, ref_phi, atol=1e-8)
    assert s2 == pytest.approx(ref_sigma**2, abs=1e-8)


def test_psi_and_theoretical_acf():
    phi, theta = [1.0, -0.29], [0.4, -0.2]
    np.testing.assert_allclose(R.psi_weights(phi, theta, 30), arma2ma(np.r_[1, -np.array(phi)], np.r_[1, theta], 30), atol=1e-10)
    np.testing.assert_allclose(R.theoretical_acf(phi, theta, 15), arma_acf(np.r_[1, -np.array(phi)], np.r_[1, theta], 16), atol=1e-8)


def test_roots_and_ar2():
    assert R.ar2_in_triangle(1.35, -0.72) and not R.ar2_in_triangle(1.2, 0.5)
    np.testing.assert_allclose(sorted(R.ar_roots_modulus([1.35, -0.72])), [np.sqrt(1 / 0.72)] * 2)
    assert R.causal_invertible_check([0.5], [0.4])["causal"]
    assert not R.causal_invertible_check([], [-1.25])["invertible"]


def test_Psi_weights_and_forecast_variance_vs_statsmodels():
    ni = SERIES["NI"]()
    fit = ARIMA(ni, order=(0, 1, 1), trend="n").fit()
    theta = fit.params[0]
    Psi = F.Psi_weights_arima([], [theta], 1, 10)
    np.testing.assert_allclose(Psi, [1] + [1 + theta] * 9, atol=1e-12)  # Bài 12, Định lý 4(b)
    var_manual = F.forecast_variance_manual(Psi, fit.params[1], 10)
    var_sm = fit.get_forecast(10).var_pred_mean
    np.testing.assert_allclose(var_manual, var_sm, rtol=2e-3)


def test_sarima_polys_psi_matches_arma2ma():
    ar, ma = F.sarima_polys(theta=[-0.34], Theta=[-0.54], d=1, D=1, s=12)
    assert len(ar) == 1 + 1 + 12 + 0 + 0 and ar[0] == 1  # (1−z)(1−z¹²) có bậc 13
    np.testing.assert_allclose(F.psi_from_polys(ar, ma, 40), arma2ma(ar, ma, 40), atol=1e-10)


def test_back_transform_and_ses():
    out = F.back_transform_log(5.0, 0.3)
    assert out["mean"] / out["median"] == pytest.approx(np.exp(0.045))
    ni = SERIES["NI"]()
    lvl = F.ses_recursion(ni, 0.267)
    ses = SimpleExpSmoothing(ni, initialization_method="known", initial_level=ni[0]).fit(smoothing_level=0.267, optimized=False)
    assert lvl[-1] == pytest.approx(ses.forecast(1)[0], abs=1e-8)


def test_benchmarks():
    y = np.arange(1.0, 25.0)
    assert F.forecast_naive(y, 3).tolist() == [24, 24, 24]
    assert F.forecast_seasonal_naive(y, 14, 12).tolist() == list(range(13, 25)) + [13, 14]
    assert F.forecast_drift(y, 2).tolist() == [25.0, 26.0]


def test_accuracy_measures_lecture12_example_5_1():
    actual = np.array([100, 120, 90, 110.0])
    a, b = np.array([95, 115, 100, 105.0]), np.array([100, 110, 95, 120.0])
    assert E.mae(actual, a) == 6.25 and E.rmse(actual, a) == pytest.approx(np.sqrt(43.75))
    assert E.mape(actual, b) == pytest.approx(100 * np.mean([0, 10 / 120, 5 / 90, 10 / 110]))
    train = np.cumsum(np.arange(1.0, 30.0))  # MASE bất biến theo thang đo (Định lý 6(b))
    assert E.mase(actual, a, train, 1) == pytest.approx(E.mase(actual * 7, a * 7, train * 7, 1))


def test_rolling_origin_and_dm():
    y = np.arange(20.0)
    actual, fc = E.rolling_origin_forecast(y, lambda tr, h: np.full(h, tr[-1]), t0=10, h=2)
    assert len(actual) == 9 and np.all(actual - fc == 2)
    rng = np.random.default_rng(0)
    dm, p = E.diebold_mariano(rng.normal(size=500))
    assert abs(dm) < 4 and 0 <= p <= 1
    assert E.diebold_mariano(np.full(30, -1.0) + rng.normal(0, 0.1, 30))[1] < 1e-6


def test_rolling_origin_horizons_matches_single_horizon():
    y = np.arange(30.0) ** 1.3
    fc = lambda tr, h: np.full(h, tr[-1])  # noqa: E731
    both = E.rolling_origin_horizons(y, fc, t0=20, H=3)
    for h in (1, 2, 3):
        a, f = E.rolling_origin_forecast(y, fc, 20, h)
        np.testing.assert_allclose(both[h][0], a)
        np.testing.assert_allclose(both[h][1], f)


def test_child_rng_is_order_independent():
    from as3179ts.simulation import child_rng
    assert child_rng(11, 3).normal() == child_rng(11, 3).normal() != child_rng(11, 4).normal()
