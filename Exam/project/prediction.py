import datetime
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from statsmodels.tsa.ar_model import AutoReg, ar_select_order



def predict_alarm_in(alarm_level, time, weight, temperature, humidity):
    df_weight = pd.DataFrame({'weight': weight}, time)
    df_weight = df_weight.asfreq(pd.infer_freq(df_weight.index))


    df_all = pd.DataFrame({'weight': weight, 'temperature': temperature, 'humidity': humidity}, time)
    df_all = df_all.asfreq(pd.infer_freq(df_all.index))

    return __predict_on_weight(alarm_level, df_weight), __predict_on_all(alarm_level, df_all)


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
    if len(df_all) < 20: return None

    if df_all['weight'].iloc[-1] <= alarm_level:
        t = datetime.datetime.strptime("00:00:00","%H:%M:%S")
        return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    
    model = VAR(df_all)
    model.select_order(int(len(df_all)/20))
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


def __mse_predict_on_weight():
    return None

def __mse_predict_on_all():
    return None


if __name__ == "__main__":
    alarm_level = 200

    curr_time = datetime.datetime.now()
    time = [ curr_time + datetime.timedelta(0, t*60) for t in range(20) ]
    weight = [ w for w in range(2500, 500, -100) ]
    temperature = [ t for t in range(40 , 20, -1) ]
    humidity = [ h for h in range(50, 30, -1) ]

    print(predict_alarm_in(alarm_level, time, weight, temperature, humidity))
