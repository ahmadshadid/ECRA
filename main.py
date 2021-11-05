import streamlit as st
import pandas as pd

import numpy as np
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta
from plotly.subplots import make_subplots
api_key = "uGiXeptXdpw1MaptLsVJnXEcCIxLz7q766XUF4lkDnOQn1WzzjzbnGsvmyBBR4r4"
api_secret = "nz5Sw5IKOPQVPl3hYJTywuJvaoQbQKJ9OMXFi6rV1wWs4h0EpHuscVymH2JhH2Il"
client = Client(api_key, api_secret)

st.title('Cryptos Exploration')

st.markdown("""
This app fro analysing cryptos 
""")

st.sidebar.header('User Input Features')
list_crypto = ['ANTUSDT', 'ALGOUSDT', 'ADAUSDT', 'ATOMUSDT', 'ATAUSDT', 'ARUSDT', 'AVAUSDT', 'AVAXUSDT', 'BTCUSDT',
               'CELOUSDT',
               'CELRUSDT', 'CKBUSDT', 'BLZUSDT', 'CHRUSDT', 'DASHUSDT', 'BANDUSDT', 'BTGUSDT', 'CFXUSDT', 'CTXCUSDT',
               'CVCUSDT',
               'CTSIUSDT', 'CTKUSDT', 'FETUSDT', 'DGBUSDT', 'DCRUSDT', 'DOCKUSDT', 'DUSKUSDT', 'DOTUSDT', 'FIROUSDT',
               'EGLDUSDT', 'ETCUSDT', 'GTOUSDT', 'GTCUSDT', 'DATAUSDT', 'EOSUSDT', 'DENTUSDT', 'HIVEUSDT'
    , 'DNTUSDT', 'KEEPUSDT', 'ELFUSDT', 'LTCUSDT', 'FTMUSDT', 'HOTUSDT', 'FILUSDT', 'FLOWUSDT', 'KEYUSDT', 'KMDUSDT',
               'JSTUSDT', 'GRTUSDT', 'LINKUSDT', 'LSKUSDT', 'ICXUSDT', 'KSMUSDT', 'HBARUSDT', 'LUNAUSDT', 'LTOUSDT',
               'NEARUSDT'
    , 'LITUSDT', 'IOTXUSDT', 'HNTUSDT', 'MATICUSDT', 'IOSTUSDT', 'IRISUSDT', 'MDTUSDT', 'MASKUSDT', 'IOTAUSDT',
               'ICPUSDT', 'NULSUSDT', 'NKNUSDT', 'NANOUSDT', 'OCEANUSDT', 'ONEUSDT'
    , 'OMGUSDT', 'OGNUSDT', 'MINAUSDT', 'QNTUSDT', 'RIFUSDT', 'RSRUSDT', 'TOMOUSDT', 'PAXGUSDT', 'SCUSDT', 'OXTUSDT',
               'MTLUSDT', 'PUNDIXUSDT', 'VETUSDT', 'KLAYUSDT', 'RVNUSDT', 'SKLUSDT', 'SFPUSDT', 'XLMUSDT', 'TFUELUSDT',
               'SXPUSDT',
               'THETAUSDT',
               'PONDUSDT', 'ONGUSDT', 'STMXUSDT', 'STRAXUSDT', 'TWTUSDT', 'DOGEUSDT', 'ETHUSDT', 'SOLUSDT', 'TRBUSDT',
               'TRXUSDT', 'VTHOUSDT', 'XECUSDT', 'XEMUSDT', 'VITEUSDT', 'COSUSDT', 'XRPUSDT', 'ZECUSDT', 'WAVESUSDT',
               'ZILUSDT', 'IDEXUSDT', 'XTZUSDT',
               'COCOSUSDT', 'GALAUSDT', 'FIOUSDT', 'QTUMUSDT', 'GHSTUSDT', 'ILVUSDT', 'BTTUSDT', 'MANAUSDT', 'WINUSDT',
               'NEOUSDT', 'WTCUSDT', 'STXUSDT', 'MBOXUSDT'
    , 'NUUSDT', 'ENJUSDT', 'ONTUSDT', 'ORNUSDT', 'TLMUSDT', 'PHAUSDT', 'ZENUSDT', 'XMRUSDT', 'REQUSDT', 'NMRUSDT',
               'ROSEUSDT', 'POLYUSDT', 'POLSUSDT', 'SLPUSDT', 'WANUSDT', 'STPTUSDT', 'ZRXUSDT', 'SYSUSDT', 'TVKUSDT',
               'YGGUSDT', 'TORNUSDT',
               'UTKUSDT', 'RLCUSDT', 'SANDUSDT', 'WAXPUSDT', 'COTIUSDT', 'VIDTUSDT', 'LPTUSDT']

selected_crypto = st.sidebar.selectbox('Crypto', list_crypto)


# Web scraping of NBA player stats
@st.cache
def load_data(crypto):
    raw = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_5MINUTE, "14 Oct, 2021", "17 Oct, 2021")
    raw = pd.DataFrame(raw)
    # print(raw)
    if not raw.empty:
        raw[0] = pd.to_datetime(raw[0], unit='ms')
        # print(raw)
        raw.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'IGNORE', 'quoteVolume', 'SELLVolume',
                       'BUY_VOL', 'BUY_VOL_VAL', 'x']

        del raw['IGNORE']
        del raw['BUY_VOL']
        del raw['BUY_VOL_VAL']
        del raw['x']
        del raw['SELLVolume']

        # convert to numbers
        raw["open"] = pd.to_numeric(raw["open"])
        raw["high"] = pd.to_numeric(raw["high"])
        raw["low"] = pd.to_numeric(raw["low"])
        raw["close"] = pd.to_numeric(raw["close"])
        raw["volume"] = round(pd.to_numeric(raw["volume"]))
        raw["quoteVolume"] = round(pd.to_numeric(raw["quoteVolume"]))
        raw.loc[raw.quoteVolume < 100, 'quoteVolume'] = 100

        raw['1h_future_close'] = raw['close'].shift(-12)
        raw['1h_close_future_pct'] = raw['1h_future_close'].pct_change(12) * 100
        raw['6h_future_close'] = raw['close'].shift(-72)
        raw['6h_close_future_pct'] = raw['6h_future_close'].pct_change(72) * 100
        raw['12h_future_close'] = raw['close'].shift(-144)
        raw['12h_close_future_pct'] = raw['12h_future_close'].pct_change(144) * 100

    return raw


raw = load_data(selected_crypto)
rawfinal = raw[(raw.timestamp >= '2021-10-14 23:05:00') & (raw.timestamp <= '2021-10-16 15:00:00')]
rawbtc = load_data("BTCUSDT")
rawbtc = rawbtc[(rawbtc.timestamp >= '2021-10-14 23:05:00') & (rawbtc.timestamp <= '2021-10-16 15:00:00')]

# Ticker data
st.header('**Cypto data**')
st.write(rawfinal)

fig4 = go.Figure()

fig4 = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig4.add_trace(
    go.Scatter(x=rawbtc.timestamp, y=rawbtc['close'],
               name='close BTC',
               line=dict(width=2,
                         color='rgb(229, 151, 50)')),
    secondary_y=False,
)
fig4.add_trace(
    go.Scatter(x=rawfinal.timestamp, y=rawfinal['close'],
               name='close' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')),
    secondary_y=True,
)
# Add figure title
fig4.update_layout( title_text=" close btc and crypto",paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',width=800,
    height=500)

# Set x-axis title
fig4.update_xaxes(showgrid=False,title_text="datetime")
fig4.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1h", step="hour", stepmode="backward"),
            dict(count=3, label="4h", step="hour", stepmode="backward"),
            dict(count=6, label="12h", step="hour", stepmode="todate"),
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(step="all")
        ])
    ))
# Set y-axes titles
fig4.update_yaxes(showgrid=False,title_text="<b>close "+ str(selected_crypto)+"</b>  ", secondary_y=False)
fig4.update_yaxes(showgrid=False,title_text="<b>close_btc</b> ", secondary_y=True)

st.header('**Closing Price**')

st.plotly_chart(fig4)
##ats exploration
df_initial_ats = pd.read_csv('index_ATS.csv',sep=',')
df_initial_ats['timeStamp'] = pd.to_datetime(df_initial_ats['date'])
df_initial_ats.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_ats.drop(['Unnamed: 0', 'date'], axis=1,inplace=True)
df_initial_ats.set_index('timeStamp',inplace=True)
df_initial_ats["mean"] = df_initial_ats.mean(axis=1)

##tps exploration
df_initial_tps = pd.read_csv('index_TPS.csv',sep=',')
df_initial_tps['timeStamp'] = pd.to_datetime(df_initial_tps['date'])
df_initial_tps.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_tps.drop(['Unnamed: 0', 'date'], axis=1,inplace=True)
df_initial_tps.set_index('timeStamp',inplace=True)
df_initial_tps["mean"] = df_initial_tps.mean(axis=1)

#substring a string to have btc not btcusdt
indexfi=selected_crypto.find('USDT')
selected_crypto_fi=selected_crypto[0:indexfi]


fig5 = go.Figure()
fig5 = make_subplots(rows=3, cols=1)

fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats[selected_crypto_fi],name="ats "+selected_crypto_fi),row=1, col=1)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats[selected_crypto_fi].rolling(6).mean(),name="MAVG_ats "+selected_crypto_fi,visible='legendonly'),row=1, col=1)

fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats["mean"],name='ats_weighted_global'),row=2, col=1)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats["mean"].rolling(6).mean(),name="MAVG_ats_weighted_global ",visible='legendonly'),row=2, col=1,secondary_y=False)
fig5.add_trace(go.Scatter(x=rawfinal.timestamp, y=rawfinal['close'],name='close' + ' ' + str(selected_crypto)),row=3, col=1)


fig5.update_layout(title_text="Side By Side ATS "+selected_crypto+" ATS GLOBAL" ,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',width=800,
    height=500)


st.header('**Side By Side ATS**')

st.plotly_chart(fig5)



fig6 = go.Figure()
fig6 = make_subplots(rows=3, cols=1)

fig6.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps[selected_crypto_fi],name="tps "+selected_crypto_fi),row=1, col=1)
fig6.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps[selected_crypto_fi].rolling(6).mean(),name="MAVG_tps "+selected_crypto_fi,visible='legendonly'),row=1, col=1)

fig6.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps["mean"],name='tps_weighted_global'),row=2, col=1)
fig6.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps["mean"].rolling(6).mean(),name="MAVG_tps_weighted_global ",visible='legendonly'),row=2, col=1)
fig6.add_trace(go.Scatter(x=rawfinal.timestamp, y=rawfinal['close'],name='close' + ' ' + str(selected_crypto)),row=3, col=1)


fig6.update_layout(title_text="Side By Side TPS "+selected_crypto+" TPS GLOBAL" ,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',width=800,
    height=500)


st.header('**Side By Side TPS**')

st.plotly_chart(fig6)



