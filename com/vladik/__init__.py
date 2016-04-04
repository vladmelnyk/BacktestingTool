import numpy as np
import pandas as pd
from pandas import DataFrame
import CointegratedAssets
from statsmodels.tsa.api import coint
import DBUtil
import johansen
# import zipline


dbUtil = DBUtil.DBUtil();
print(dbUtil.getData())
bidO = dbUtil.bidO
askB = dbUtil.askB
time = dbUtil.p_time
print(time[0])
print(bidO)
print(askB)
t = np.array(time)
a = np.array(bidO)
b = np.array(askB)

d = {'ask_bitmex': b, 'bid_okcoin': a, 'time': pd.to_datetime(t, unit='s')}
df = DataFrame(data=d, columns=d.keys())
print(df)

assets = np.column_stack((a, b))
print(assets)
result = johansen.coint_johansen(assets, 0, 1)
print("1 " + str(result.eig))
print result.evec
print(result.lr1)
print(result.lr2)
print(result.cvt)
print(result.cvm)
print(result.ind)
print result.rkt
print result.r0t

data = df
cointegration = coint(a,b)
print cointegration
# s = bt.Strategy('s1', [bt.algos.SelectAll(),
#                        bt.algos.WeighEqually()
#                        ])
#
# test = bt.Backtest(s, data)
# res = bt.run(test)
# res.plot()
# res.display()
# line_chart = pygal.Line()
# line_chart.title = 'Browser usage evolution (in %)'
# line_chart.x_labels = map(str, range(2002, 2013))
# line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
# line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
# line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
# line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
# line_chart.render_to_file("time_series_chart.svg")
# cointegratedAssets = CointegratedAssets.CointegratedAssets()
# print cointegratedAssets.cointegration_test_stat()
# print cointegratedAssets.testForCointegrationJohansen(a,b)
# print cointegratedAssets.testForCointegration(assets)
# print cointegratedAssets.cointegration_test_stat()
# mdata = macrodata.load().data
# mdata = mdata[['realgdp','realcons']]
# data = mdata.view((float,2))
# data = np.diff(np.log(data), axis=0)
#
# #R: lmtest:grangertest
# r_result = [0.243097, 0.7844328, 195, 2]  #f_test
# gr = tsa_stats.grangercausalitytests(data[:,1::-1], 2, verbose=True)
# print gr
# cointegratedAssets.CointegratedAssets.
