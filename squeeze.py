import os
import pandas
import plotly.graph_objects as go


files = os.listdir("datasets/currencies/daily")

for file in files:
    df = pandas.read_csv("datasets/currencies/daily/{}".format(file))

    if df.empty:
        continue

    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['stdDev'] = df['Close'].rolling(window=20).std()

    df['BBandUpper'] = df['20sma'] + (2*df['stdDev'])
    df['BBandLower'] = df['20sma'] - (2*df['stdDev'])

    df['TR'] = abs(df['High']-df['Low'])
    df['10ATR'] = df['TR'].rolling(window=20).mean()

    df['KeltnerUpperBand'] = df['20sma'] + (1.5*df['10ATR'])
    df['KeltnerLowerBand'] = df['20sma'] - (1.5*df['10ATR'])


    def inSqueeze(df):
        return df['BBandUpper'] < df['KeltnerUpperBand'] and df['BBandLower'] > df['KeltnerLowerBand']

    df['InSqueeze'] = df.apply(inSqueeze, axis=1)



    if df.iloc[-2]['InSqueeze']:

        print("{} was in the squeeze".format(file))

        if not df.iloc[-1]['InSqueeze']:
            print("{} brokeout".format(file))

        candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])

        BBandUpper = go.Scatter(x=df['Date'], y=df['BBandUpper'], name=' Upper Bollinger band', line={'color':'red'})
        BBandLower = go.Scatter(x=df['Date'], y=df['BBandLower'], name=' Lower Bollinger band', line={'color':'red'})
        
        KeltnerBandUpper = go.Scatter(x=df['Date'], y=df['KeltnerUpperBand'], name=' Lower Keltner band', line={'color':'blue'})
        KeltnerBandLower = go.Scatter(x=df['Date'], y=df['KeltnerLowerBand'], name=' Lower Keltner band', line={'color':'blue'})
        
        fig = go.Figure(data=[candlestick, BBandUpper, BBandLower, KeltnerBandUpper, KeltnerBandLower], layout_title_text=file)
        fig.layout.xaxis.type = 'category'
        #fig.layout.xaxis.rangeslider.visible = False
        fig.layout.yaxis.tickformat = ".5f" 
        fig.show()