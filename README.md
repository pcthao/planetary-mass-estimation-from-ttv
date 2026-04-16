# **Planetary Mass Estimation From Transit Timing Variations (TTVs)** 
End-to-end pipeline combining dynamical simulation (`TTV2Fast2Furious`) with Bayesian inference (MCMC) to estimate exoplanet masses from noisy timing data.

# **Overview** 
This project estimates the masses of planets in the HIP 67522 b using Transit Timing Variations (TTVs) -- small deviations in the timing of planetary transits caused by graviational interactions in multi-planet systems. 

I integrated the TTV2Fast2Furious to generate model transit timing signals and apply a Markov Chain Monte Carlo (MCMC) method  to infer planetary masses and orbital parameters from the observed data. The analysis focuses on determing wheterh TTV data alone can constrain masses and how those estimate compared to indepednent measurements.

# **Key Questions**
- Can the observed TTV signal place a meaningful constraint on the mass of planet c?
- How well does the best-fit TTV model reproduced the observed transit times?
- Does the TTV-derived mass of planet b align with independent estimates from transmission spectroscopy?

# **Methodology** 
- **Simulation**: TTV signals genered using `TTV2Fast2Furious`
- **Inference**: MCMC (`emcee`) used to estimate masses and orbital parameters
- **Liklihood Design**: Incorporates timing uncertainities
- **Validation**: Synthetic data test and residual analysis

# **Results**
- The TTV signal in this system is relatively low amplitude (~ 5 minutes for planet b and ~10 minutes for planet c). 
- Despite the weak signal, MCMC inference places meaningful constraints on the mass of planet c, with uncertainties driven by measurement noise and parameter degeneracies
- The TTV-derived mass estimate for planet b is consisteny with indepednet constrains from transmission spectroscopy.

# **Repository Strucutre**
notebooks/   # Jupyter notebooks for modeling, MCMC analysis, and visualization
data/        # Input datasets (observed TTV data)
results/     # Output plots, posterior distributions, and diagnostics 
