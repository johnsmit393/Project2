import os
import json
import pandas as pd

from alpaca_trade_api.rest import REST, TimeFrame

data_path = './data'

for filename in os.listdir(data_path):
    filepath = os.path.join(data_path, filename)
    os.remove(filepath)


def refresh_data(coin_name):
    """
        coin_name: ETHUSD, BTCUSD
    """
    temp_data_path = f"./data/last_9_hours_alpaca{coin_name}.csv"

    # Read the secret data from env file
    with open("env", "r") as f:
        secret = json.loads(f.read())

    # Get data from Alpaca API with 1 hour interval between 2018-01-01 and 2022-10-19
    with REST(key_id=secret['ALPACA_API_KEY'], secret_key=secret['ALPACA_SECRET_KEY']) as api:
        data = api.get_crypto_bars(coin_name, TimeFrame.Minute).df

    data.to_csv(temp_data_path)


def get_last_value(coin_name):
    """
        coin_name: ETHUSD, BTCUSD
    """
    temp_data_path = f"./data/last_9_hours_alpaca{coin_name}.csv"
    data = pd.read_csv(temp_data_path)
    data = data[data.exchange == 'ERSX']  # TODO: which exchange?

    return data.close.to_list()[-1]


refresh_data("ETHUSD")
refresh_data("BTCUSD")
