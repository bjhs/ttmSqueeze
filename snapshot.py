import csv
import yfinance as yf

with open("datasets/currencyPairs.csv") as f:
    file = csv.reader(f)
    for row in file:
        print(row[0])

        df = yf.download(row[0], start="2021-06-01")
        df.to_csv("datasets/currencies/daily/{}.csv".format(row[0]))
    