from statsmodels.tsa.stattools import (adfuller, acf, pacf_ols, pacf_yw,
                                               pacf, grangercausalitytests,
                                               coint, acovf)

import numpy as np
import statsmodels.api as stat
import statsmodels.tsa.stattools as ts


class CointegratedAssets(object):
    # The "CointegratedAssets" class implements the Engle-Granger approach
    # to cointegrated time series.


    def testForCointegration(self, assets):
        x = np.random.normal(0,1, 1000)
        y = np.random.normal(0,1, 1000)
        x = np.array(x)
        y = np.array(y)
        c =np.column_stack((x,y))
        a = grangercausalitytests(c,-1,verbose=True)
        return a
    def testForCointegrationJohansen(self, series1,series2):
        a = coint(series1,series2, "ct")
        
        return a
    def cointegration_test_stat(self):
        x = np.random.normal(0,1, 1000)
        y = np.random.normal(0,1, 1000)
        result = stat.OLS(y, x).fit()
        return ts.adfuller(result.resid)

# assets = [Stock("MSFT"), Stock("GOOG")]
# ca = CointegratedAssets(assets)
