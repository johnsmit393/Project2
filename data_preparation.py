import os
import json
import pandas as pd

from alpaca_trade_api.rest import REST, TimeFrame

data_path = './data'

for filename in os.listdir(data_path):
    filepath = os.path.join(data_path, filename)
    os.remove(filepath)

# Read the secret data from env file
with open("env", "r") as f:
    secret = json.loads(f.read())


def refresh_data(coin_name):
    """DEPRECATED
        coin_name: ETHUSD, BTCUSD
    """
    temp_data_path = f"./data/last_9_hours_alpaca{coin_name}.csv"

    # Get data from Alpaca API with 1 hour interval between 2018-01-01 and 2022-10-19
    with REST(key_id=secret['ALPACA_API_KEY'], secret_key=secret['ALPACA_SECRET_KEY']) as api:
        data = api.get_crypto_bars(coin_name, TimeFrame.Minute).df

    data.to_csv(temp_data_path)


def retreve_data_from_alpaca(coin, timeframe, effective_from, effective_to):
    """
        coin: str = ['BTCUSD', ETHUSD],
        timeframe: alpaca_trade_api.rest.TimeFrame = TimeFrame.Hour,
        effective_from = "2018-01-01",
        effective_to = "2019-01-01"
    """
    # Get data from Alpaca API with 1 hour interval between 2018-01-01 and 2022-10-19
    with REST(key_id=secret['ALPACA_API_KEY'], secret_key=secret['ALPACA_SECRET_KEY'], ) as api:
        data = api.get_crypto_bars(symbol=coin, timeframe=timeframe, start=effective_from, end=effective_to).df

    # Chose only FTXU data
    ftx_data = data[data.exchange == 'CBSE']

    # Prepare dataset for Prophet model
    prophet_data = ftx_data.reset_index()
    prophet_data = prophet_data[['timestamp', 'close']]
    prophet_data.columns = ['ds', 'y']
    prophet_data['ds'] = prophet_data['ds'].apply(lambda x: x.replace(tzinfo=None))  # remove timezone from timestamp
    return prophet_data


def get_last_value(coin_name):
    """DEPRECATED
        coin_name: ETHUSD, BTCUSD
    """
    temp_data_path = f"./data/last_9_hours_alpaca{coin_name}.csv"
    data = pd.read_csv(temp_data_path)
    data = data[data.exchange == 'ERSX']  # TODO: which exchange?

    return data.close.to_list()[-1]


refresh_data("ETHUSD")
refresh_data("BTCUSD")
