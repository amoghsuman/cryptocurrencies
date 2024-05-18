import backtrader as bt

class MovingAverageStrategy(bt.Strategy):
    params = dict(
        ma_period=10,
        active_pct=0.1
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.ma_period)

    def next(self):
        position_size = self.broker.get_value() * self.params.active_pct

        if not self.position:
            if self.data_close[-1] > self.sma[-1]:
                self.buy(size=position_size / self.data_close[0])
        else:
            if self.data_close[-1] < self.sma[-1]:
                self.sell(size=self.position.size)

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    data = bt.feeds.GenericCSVData(
        dataname='path/to/your/bitcoin_data.csv',
        dtformat=('%Y-%m-%d'),
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.addstrategy(MovingAverageStrategy)
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
