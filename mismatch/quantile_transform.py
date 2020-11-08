from __future__ import print_function
from __future__ import division
from . import C_

import numpy as np
import scipy.stats as stats

###################################################################################################################################################

def naive_quantile_normal(x, n_percentiles):
    # generate the percentiles to evaluate
    x_percentiles = np.linspace(0, 100, n_percentiles)
    
    # get ppf value acording to x-distribution and each percentile
    x_distr_ppf = np.percentile(x, x_percentiles)
    
    # get the interpolated percentile for each data point in x-distribution
    x_percentiles_i = np.interp(x, x_distr_ppf, x_percentiles)
    
    # using the interpolated percentiles, map to standar normal-distribution using the inverse of cdf (norm-ppf)
    # you can use another distribution if you know the cdf/ppf function
    normx = stats.norm.ppf(x_percentiles_i/100)

    norm_ppf = stats.norm.ppf(x_percentiles/100) # normal ppf to plot
    normx_percentiles_i = stats.norm.cdf(normx)*100 # normal ppf to plot
    
    return normx, [x_percentiles, x_distr_ppf, x_percentiles_i, normx_percentiles_i, norm_ppf]