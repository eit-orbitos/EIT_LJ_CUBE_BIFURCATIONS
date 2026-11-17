"""Numerical check of the local A2u branch inside the T_d shape family (scale eliminated).

f(u) = log Phi along rho_+ = e^(-u/2), rho_- = e^(u/2):  f(u) = p log U_q(u) - q log U_p(u), even in u.
Near the curve, nonzero critical points satisfy u^2 ~ -6 f''(0) / f''''(0). This module locates them directly,
with the analytic u-derivative of U_r and a bracketing root finder.
"""
import mpmath as mp


def _D(uu):
    return mp.mpf(3) / 2 * mp.cosh(uu) - mp.mpf(1) / 2


def U_sym(rr, uu):
    rr, uu = mp.mpf(rr), mp.mpf(uu)
    return (12 * mp.power(2, -rr / 2) * mp.cosh(rr * uu / 2) + 12 * mp.power(_D(uu), -rr / 2)
            + 4 * mp.power(3, -rr / 2) * mp.power(mp.cosh(uu / 2), -rr))


def dU_sym(rr, uu):
    rr, uu = mp.mpf(rr), mp.mpf(uu)
    return (6 * rr * mp.power(2, -rr / 2) * mp.sinh(rr * uu / 2) - 9 * rr * mp.power(_D(uu), -rr / 2 - 1) * mp.sinh(uu)
            - 2 * rr * mp.power(3, -rr / 2) * mp.power(mp.cosh(uu / 2), -rr - 1) * mp.sinh(uu / 2))


def f(uu, pp, qq):
    return pp * mp.log(U_sym(qq, uu)) - qq * mp.log(U_sym(pp, uu))


def df(uu, pp, qq):
    return pp * dU_sym(qq, uu) / U_sym(qq, uu) - qq * dU_sym(pp, uu) / U_sym(pp, uu)


def taylor_f(pp, qq):
    """f''(0), f''''(0) by numerical differentiation of f (independent of the closed forms k, m)."""
    with mp.workdps(mp.mp.dps + 30):
        return (mp.diff(lambda t: f(t, pp, qq), 0, 2), mp.diff(lambda t: f(t, pp, qq), 0, 4))


def branch_point(pp, qq):
    """Predicted and found u > 0 with f'(u) = 0 (None when -6 f''/f'''' <= 0)."""
    f2, f4 = taylor_f(pp, qq)
    pred2 = -6 * f2 / f4
    if pred2 <= 0:
        return {"f2": f2, "f4": f4, "u_pred": None, "u_found": None}
    up = mp.sqrt(pred2)
    g = lambda t: df(t, pp, qq) / t
    found = mp.findroot(g, (up / 2, 3 * up / 2), solver="anderson")
    return {"f2": f2, "f4": f4, "u_pred": up, "u_found": found}


def no_small_branch(pp, qq, umax, n=200):
    """True if f'(u) keeps one sign on (0, umax] (sampled), i.e. no small nonzero critical point."""
    vals = [df(umax * mp.mpf(k) / n, pp, qq) for k in range(1, n + 1)]
    return all(v < 0 for v in vals) or all(v > 0 for v in vals)
