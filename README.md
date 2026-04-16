# planetary-mass-estimation-from-ttv

This project estimates the masses of exoplanets using Transit Timing Variations (TTVs) -- small deviations in the timing of planetary transits caused by graviational interactions in multi-planet systems. 

Using a two planet system, HIP 67522 b and c, I integrated the TTV2Fast2Furious simulator to generate the transit timing signals and comined it with a Bayesian inference pipeline to recover planetary masses from observed data. 


Key Features: 
- Leveraged TTV2Fast2Furious to simulate transit timing signals for interacting planetary systems
- Built an MCMC-based inference pipeline (using emcee) to estimate planetary masses and orbital parameters
- Designed a likelihood function incorporating observational uncertainties and timing errors
- Evaluated model performance using residuals and reduced chi-square statistics
