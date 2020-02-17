import pandas as pd

csv = 'btc'

def pandasclean(csv):
    df = pd.read_csv('cryptodata/'+ csv +'usd.csv',parse_dates=['Date'],usecols=[1,2,3,4,5])
    df = df.set_index('Date').sort_index(ascending=True)
    df.dropna(inplace=True)
    return df

print(pandasclean(csv))