import datetime
import pandas as pd
import numpy as np

from statsmodels.tsa.api import VAR
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from statsmodels.tools.eval_measures import mse



def predict_alarm_in(alarm_level, time, weight, temperature, humidity):
    df_weight = pd.DataFrame({'weight': weight}, time)
    df_weight = df_weight.asfreq(pd.infer_freq(df_weight.index))


    df_all = pd.DataFrame({'weight': weight, 'temperature': temperature, 'humidity': humidity}, time)
    df_all = df_all.asfreq(pd.infer_freq(df_all.index))

    return (__predict_on_weight(alarm_level, df_weight), __mse_predict_on_weight(df_weight)), (__predict_on_all(alarm_level, df_all), __mse_predict_on_all(df_all))


def __predict_on_weight(alarm_level, df_weight):
    if df_weight['weight'].iloc[-1] <= alarm_level:
        t = datetime.datetime.strptime("00:00:00","%H:%M:%S")
        return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    
    auto_lags = ar_select_order(df_weight, int(len(df_weight)/2-1)).ar_lags
    model = AutoReg(df_weight, auto_lags).fit()

    initial_time = df_weight.index[-1].to_pydatetime()
    curr_time = initial_time
    it = 0
    while (curr_time - initial_time).total_seconds() < 86400:
        predictions = model.predict(start=it*10+len(df_weight), end=it*10+9+len(df_weight))
        for i, pred in predictions.items():
            if pred <= alarm_level:
                return i.to_pydatetime() - initial_time
        
        it += 1
        curr_time = list(predictions.items())[-1][0].to_pydatetime()

    t = datetime.datetime.strptime("23:59:59","%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)


def __predict_on_all(alarm_level, df_all):
    if df_all['weight'].iloc[-1] <= alarm_level:
        t = datetime.datetime.strptime("00:00:00","%H:%M:%S")
        return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    
    if len(df_all) < 20: return None
    
    model = VAR(df_all)
    #model.select_order(int(len(df_all)/20))
    results = model.fit(maxlags=int(len(df_all)/7))
    freq = pd.to_timedelta(np.diff(df_all.index).min()).total_seconds()
    forecast = results.forecast(df_all.values, int(86400 / freq))
    df_forecast = pd.DataFrame(forecast, columns=df_all.columns)

    sec = freq
    for i, pred in df_forecast['weight'].items():
        if pred <= alarm_level:
            return datetime.timedelta(0, sec)
        sec += freq

    t = datetime.datetime.strptime("23:59:59","%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)


def __mse_predict_on_weight(df_weight):
    df_train = df_weight.iloc[:int(0.8*len(df_weight))]
    df_test = df_weight.iloc[int(0.8*len(df_weight)):]

    auto_lags = ar_select_order(df_train, int(len(df_train)/2-1)).ar_lags
    model = AutoReg(df_train, auto_lags).fit()
    predictions = model.predict(start=len(df_train), end=len(df_weight)-1)
    
    return mse(predictions.array, df_test['weight'].array)

def __mse_predict_on_all(df_all):
    if len(df_all) < 20: return None

    df_train = df_all.iloc[:int(0.8*len(df_all))]
    df_test = df_all.iloc[int(0.8*len(df_all)):]
    
    model = VAR(df_all)
    #model.select_order(int(len(df_all)/20))
    results = model.fit(maxlags=int(len(df_train)/7))
    forecast = results.forecast(df_train.values, len(df_all)-len(df_train))
    df_forecast = pd.DataFrame(forecast, columns=df_train.columns)

    return mse(df_forecast['weight'].array, df_test['weight'].array)


if __name__ == "__main__":
    alarm_level = 200

    curr_time = datetime.datetime.now()
    time = [ curr_time + datetime.timedelta(0, t*60) for t in range(20) ]
    weight = [ w for w in range(2500, 500, -100) ]
    temperature = [ t for t in range(40 , 20, -1) ]
    humidity = [ h for h in range(50, 30, -1) ]

    print(predict_alarm_in(alarm_level, time, weight, temperature, humidity))
