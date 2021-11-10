import streamlit as st
import pymongo
from pymongo import MongoClient
import pandas as pd
import ssl
import string


market_data = pymongo.MongoClient(
    "mongodb+srv://doadmin:2YjQ6con413i87R0@market-watch-74d794d0.mongo.ondigitalocean.com/admin?authSource=admin&tls=true&tls=true",ssl_cert_reqs=ssl.CERT_NONE)

# get_db

klines = market_data.get_database('klines')

crypto_klines = klines['crypto']

@st.cache
def load_data(crypto):
    cursor = crypto_klines.find({"symbol": crypto}, {"_id": 0, "data": 1})
    b = pd.DataFrame(cursor)
    raw = pd.DataFrame(b['data'][0])
    #raw[0] = pd.to_datetime(raw[0], unit='ms')
    raw.columns = ['timestamp', 'close', 'tps', 'rps', 'tps_std_110', 'rps_std_110', 'tps_std_1700', 'rps_std_1700']

    # print(raw)
    raw.columns = ['timestamp', 'close', 'tps', 'rps', 'tps_std_110', 'rps_std_110', 'tps_std_1700', 'rps_std_1700']
    # convert to numbers
    raw['timestamp'] = pd.to_datetime(raw['timestamp'])
    raw["close"] = pd.to_numeric(raw["close"])
    raw['1h_future_close'] = raw['close'].shift(-4)
    raw['1h_close_future_pct'] = raw['1h_future_close'].pct_change(4) * 100
    raw['6h_future_close'] = raw['close'].shift(-24)
    raw['6h_close_future_pct'] = raw['6h_future_close'].pct_change(24) * 100
    raw['12h_future_close'] = raw['close'].shift(-48)
    raw['12h_close_future_pct'] = raw['12h_future_close'].pct_change(48) * 100

    return raw


def load_tps_rps(index):
    custom_index = klines['custom_index']
    cursor = custom_index.find({"index_name": index}, {"_id": 0, "data": 1})
    b = pd.DataFrame(cursor)
    raw = pd.DataFrame(b['data'][0])
    return raw

