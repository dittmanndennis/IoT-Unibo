# Python
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

df = pd.read_csv('lab6/tseries_pm_new.csv')
print(df.head())

m = Prophet()
m.fit(df)

future = m.make_future_dataframe(periods=365)
print(future.tail())

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)

fig2 = m.plot_components(forecast)

plot_plotly(m, forecast)

plot_components_plotly(m, forecast)
