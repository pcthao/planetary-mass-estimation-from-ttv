
import numpy as np
import emcee
import corner
import pandas as pd
from uncertainties.umath import *
from ttv2fast2furious import MultiplanetSystemLinearModelAmplitudes
from ttv2fast2furious import MultiplanetSystemBasisFunctionMatrices
from tqdm import tqdm
from scipy.optimize import minimize
from scipy.spatial import cKDTree

############################################################################
def calculate_twopl_ttvs(mass1, mass2, ecc1, ecc2, omega1, omega2,
                         P, P1, T0, T10, Ntransits, Ntransits1):
    M, M1 = MultiplanetSystemBasisFunctionMatrices(2, [P, P1], [T0, T10], [Ntransits, Ntransits1])
    X, X1 = MultiplanetSystemLinearModelAmplitudes(2, [P, P1], [T0, T10], [mass1, mass2], [ecc1, ecc2], [omega1, omega2])

    TransitTimes = M @ X
    TTV = M[:, 2:] @ X[2:]
    TransitTimes1 = M1 @ X1
    TTV1 = M1[:, 2:] @ X1[2:]

    return TransitTimes, TTV, TransitTimes1, TTV1

def find_closest_calc_time_fast(observed_times, calculated_times):
    tree = cKDTree(calculated_times[:, None])
    _, idx = tree.query(observed_times[:, None])
    return calculated_times[idx]

def log_prior(params, use_mass_prior=True):
    ecc1, ecc2, omega1, omega2, mass1, mass2 = params

    if (mass1 < 2.4022e-5) or (mass1 > 9.0082e-5) or (mass2 < 0) or        (ecc1 < 0) or (ecc1 > 1.) or (ecc2 < 0.) or (ecc2 > 1.) or        (omega1 < 0) or (omega1 > 2*np.pi) or (omega2 < 0) or (omega2 > 2*np.pi):
        return -np.inf

    secosomegab = np.sqrt(ecc1) * np.cos(omega1)
    sesinomegab = np.sqrt(ecc1) * np.sin(omega1)
    secosomegac = np.sqrt(ecc2) * np.cos(omega2)
    sesinomegac = np.sqrt(ecc2) * np.sin(omega2)

    if use_mass_prior:
        values = [mass1, secosomegab, sesinomegab, secosomegac, sesinomegac]
        prior_mu = np.array([4.5041e-5, -0.072, -0.060, -0.008, -0.018])
        prior_sigma2 = np.array([1.5014e-5, 0.35261, 0.088855, 0.383276, 0.11768])**2
    else:
        values = [secosomegab, sesinomegab, secosomegac, sesinomegac]
        prior_mu = np.array([-0.072, -0.060, -0.008, -0.018])
        prior_sigma2 = np.array([0.35261, 0.088855, 0.383276, 0.11768])**2

    log_p = np.sum(-((values - prior_mu) ** 2) / (2 * prior_sigma2) - 0.5 * np.log(2 * np.pi * prior_sigma2))
    return log_p

def log_likelihood(params, observed_times1, observed_times2,
                   err_up1, err_down1, err_up2, err_down2,
                   P, P1, T0, T10, Ntransits, Ntransits1):
    ecc1, ecc2, omega1, omega2, mass1, mass2 = params

    try:
        TransitTimes, _, TransitTimes1, _ = calculate_twopl_ttvs(
            mass1, mass2, ecc1, ecc2, omega1, omega2,
            P, P1, T0, T10, Ntransits, Ntransits1
        )

        model_time1 = find_closest_calc_time_fast(observed_times1, TransitTimes)
        model_time2 = find_closest_calc_time_fast(observed_times2, TransitTimes1)

        residuals1 = observed_times1 - model_time1
        residuals2 = observed_times2 - model_time2

        err1 = np.where(residuals1 >= 0, err_down1, err_up1)
        err2 = np.where(residuals2 >= 0, err_down2, err_up2)

        chi2_1 = np.sum((residuals1 / err1) ** 2)
        chi2_2 = np.sum((residuals2 / err2) ** 2)

        return -0.5 * (chi2_1 + chi2_2)
    except Exception:
        return -np.inf

def log_posterior(params, observed_times1, observed_times2,
                  err_up1, err_down1, err_up2, err_down2,
                  P, P1, T0, T10, Ntransits, Ntransits1,
                  use_mass_prior=True):
    lp = log_prior(params, use_mass_prior=use_mass_prior)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(params, observed_times1, observed_times2,
                                err_up1, err_down1, err_up2, err_down2,
                                P, P1, T0, T10, Ntransits, Ntransits1)


