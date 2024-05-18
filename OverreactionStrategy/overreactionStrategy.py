import backtrader as bt
import datetime

class OverreactionStrategy(bt.Strategy):
    params = (
        ("std_mult", 2),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.daily_returns = self.dataclose / self.dataclose(-1) - 1
        self.avg_return = bt.indicators.SimpleMovingAverage(self.daily_returns, period=1)
        self.std_dev = bt.indicators.StdDev(self.daily_returns, period=1)

    def next(self):
        current_time = self.data.datetime.time()
        current_date = self.data.datetime.date()
        overreaction_threshold = self.avg_return[0] + self.params.std_mult * self.std_dev[0]

        if not self.position:
            if self.daily_returns[0] > overreaction_threshold and current_time == datetime.time(18, 0):
                self.buy()
            elif self.daily_returns[0] < -overreaction_threshold and current_time == datetime.time(16, 0):
                self.sell()
        else:
            if current_time == datetime.time(0, 0):
                self.close()

cerebro = bt.Cerebro()
data = bt.feeds.GenericCSVData(dataname='your_bitcoin_data.csv')
cerebro.adddata(data)
cerebro.addstrategy(OverreactionStrategy)
cerebro.run()
