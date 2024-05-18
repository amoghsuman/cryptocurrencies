import numpy as np
import pandas as pd
import statsmodels.api as sm
import backtrader as bt

class CointegratedCrypto(bt.Strategy):
		params = ( ('c', 0.5), )

		def __init__(self):
		    self.btc = self.datas[0]
		    self.eth = self.datas[1]
		    self.ltc = self.datas[2]
		    self.bch = self.datas[3]
		
		def next(self):
		    # Prepare data
		    data = pd.DataFrame({'BTC': self.btc.get(size=100), 'ETH': self.eth.get(size=100), 'LTC': self.ltc.get(size=100), 'BCH': self.bch.get(size=100)})
		
		    # OLS Regression
		    X = data[['ETH', 'LTC', 'BCH']]
		    X = sm.add_constant(X)
		    y = data['BTC']
		
		    model = sm.OLS(y, X).fit()
		    beta1, beta2, beta3 = model.params[1], model.params[2], model.params[3]
		
		    # Calculate spread S
		    spread = self.btc[0] + beta1 * self.eth[0] + beta2 * self.ltc[0] + beta3 * self.bch[0]
		
		    # Calculate mean and standard deviation of spread
		    mean_spread = np.mean(data['BTC'])
		    std_spread = np.std(data['BTC'])
		
		    # Trading logic
		    long_condition = spread < mean_spread - self.params.c * std_spread
		    short_condition = spread > mean_spread + self.params.c * std_spread
		
		    if long_condition:
		        self.buy(data=self.btc)
		        self.buy(data=self.eth, size=beta1)
		        self.buy(data=self.ltc, size=beta2)
		        self.buy(data=self.bch, size=beta3)
		    elif short_condition:
		        self.sell(data=self.btc)
		        self.sell(data=self.eth, size=beta1)
		        self.sell(data=self.ltc, size=beta2)
		        self.sell(data=self.bch, size=beta3)
