import numpy as np
from statsmodels.tsa.api import coint
from statsmodels.api import OLS
from statsmodels.tools.tools import add_constant
import CointegratedAssets
import DBUtil
import johansen
import math

def calculateStat(x,y):
    cointegration = coint(x,y)
    signal = cointegration[1] < 0.05
    x= add_constant(x)
    reg = OLS(y, x).fit()
    # returns bo,b1,rmse
    return [signal, reg.params[0],reg.params[1], math.sqrt(reg.mse_resid)]

dbUtil = DBUtil.DBUtil();
bidO = dbUtil.bidO
askB = dbUtil.askB
bidB = dbUtil.bidB
askO = dbUtil.askO
time = dbUtil.p_time
t = np.array(time)
bidO = np.array(bidO)
askB = np.array(askB)
bidB = np.array(bidB)
askO = np.array(askO)


statBidOaskB =  calculateStat(bidO,askB)
statBidBaskO =  calculateStat(bidB,askO)
print statBidOaskB
print statBidBaskO




# d = {'ask_bitmex': b, 'bid_okcoin': a, 'time': pd.to_datetime(t, unit='s')}
# df = DataFrame(data=d, columns=d.keys())
# print df
# assets = np.column_stack((a, b))
# result = johansen.coint_johansen(assets, 0, 1)
# print("1 " + str(result.eig))
# print result.evec
# print(result.lr1)
# print(result.lr2)
# print(result.cvt)
# print(result.cvm)
# print(result.ind)
#
# data = df