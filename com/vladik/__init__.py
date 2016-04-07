import numpy as np
from statsmodels.tsa.api import coint
from statsmodels.api import OLS
from statsmodels.tools.tools import add_constant
import CointegratedAssets
import DBUtil
import johansen
import math
import datetime

def calculateStat(y,x):
    cointegration = coint(y,x)
    signal = (cointegration[1] < 0.05).__int__()
    x= add_constant(x)
    reg = OLS(y, x).fit()
    # returns bo,b1,rmse
    return (signal, float(reg.params[0]),float(reg.params[1]), float(math.sqrt(reg.mse_resid)))

dbUtil = DBUtil.DBUtil();
dbUtil.getData()
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
# date now insert into statBidOaskB
date = datetime.datetime.now()
date = date.strftime('%Y-%m-%d %H:%M:%S')
statBidOaskB = list(statBidOaskB)
statBidOaskB.insert(0, date)
statBidOaskB = tuple(statBidOaskB)
#
array = statBidOaskB + statBidBaskO
print statBidOaskB
print statBidBaskO
print array
dbUtil.insertData(array)




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