import statsmodels.api as sm
import pandas as pd
import os


""" df = pd.read_csv('data/2024_03_11.csv')

idx = pd.to_datetime(df["fecha"], format = "%d/%m/%Y")
df.set_index(idx, inplace=True)

series = df['SL11298'][400:-1]

x13 = sm.tsa.x13_arima_analysis(series, x12path = "C:/Users/alvar/Desktop/BDE/banxico-md/x13as")
 """

dta = sm.datasets.co2.load_pandas().data
dta.co2.interpolate(inplace=True)
dta = dta.resample('M').sum()


print('EEEE',os.getenv("X13PATH", ""))
x13 = sm.tsa.x13_arima_analysis(dta.co2)
print(x13.trend)

""" plt.plot(dta.co2)
plt.plot(x13.trend)
plt.show() """
