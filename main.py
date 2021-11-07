import streamlit as st
import pandas as pd

import numpy as np
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta
from plotly.subplots import make_subplots

api_key = ""
api_secret = ""
client = Client(api_key, api_secret)
st.sidebar.image("wbor.png", use_column_width=True)
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

##ats exploration
df_initial_ats = pd.read_csv('index_ATS.csv', sep=',')
df_initial_ats['timeStamp'] = pd.to_datetime(df_initial_ats['date'])
df_initial_ats.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_ats.drop(['Unnamed: 0', 'date'], axis=1, inplace=True)
df_initial_ats.set_index('timeStamp', inplace=True)
df_initial_ats["mean"] = df_initial_ats.mean(axis=1)

##tps exploration
df_initial_tps = pd.read_csv('index_TPS.csv', sep=',')
df_initial_tps['timeStamp'] = pd.to_datetime(df_initial_tps['date'])
df_initial_tps.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_tps.drop(['Unnamed: 0', 'date'], axis=1, inplace=True)
df_initial_tps.set_index('timeStamp', inplace=True)
df_initial_tps["mean"] = df_initial_tps.mean(axis=1)

# substring a string to have btc not btcusdt
indexfi = selected_crypto.find('USDT')
selected_crypto_fi = selected_crypto[0:indexfi]

st.sidebar.header('Index Watch List')
list_index = ['TPS', 'ATS']
selected_index = st.sidebar.selectbox('Index', list_index)
list_index_interval = ['5min', '1hour', '4hour', '1day']
selected_index_interval = st.sidebar.selectbox('Interval', list_index_interval)
if selected_index == 'ATS':
    ats_pct_5min = df_initial_ats.pct_change().fillna(0) * 100
    ats_pct_5min_last = ats_pct_5min.iloc[-1].sort_values(ascending=False, inplace=False)
    ats_pct_1h = df_initial_ats.pct_change(12).fillna(0) * 100
    ats_pct_1h_last = ats_pct_1h.iloc[-1].sort_values(ascending=False, inplace=False)
    ats_pct_4h = df_initial_ats.pct_change(48).fillna(0) * 100
    ats_pct_4h_last = ats_pct_4h.iloc[-1].sort_values(ascending=False, inplace=False)
    ats_pct_1d = df_initial_ats.pct_change(288).fillna(0) * 100
    ats_pct_1d_last = ats_pct_1d.iloc[-1].sort_values(ascending=False, inplace=False)
    fig7 = go.Figure()
    if selected_index_interval == '5min':
        fig7.add_trace(
            go.Bar(y=ats_pct_5min_last[:10].iloc[::-1].index, x=ats_pct_5min_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(ats_pct_5min_last[:10].iloc[::-1].values, decimals=2)
        xindex = ats_pct_5min_last[:10].iloc[::-1].index

    if selected_index_interval == '1hour':
        fig7.add_trace(
            go.Bar(y=ats_pct_1h_last[:10].iloc[::-1].index, x=ats_pct_1h_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(ats_pct_1h_last[:10].iloc[::-1].values, decimals=2)
        xindex = ats_pct_1h_last[:10].iloc[::-1].index

    if selected_index_interval == '4hour':
        fig7.add_trace(
            go.Bar(y=ats_pct_4h_last[:10].iloc[::-1].index, x=ats_pct_4h_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(ats_pct_4h_last[:10].iloc[::-1].values, decimals=2)
        xindex = ats_pct_4h_last[:10].iloc[::-1].index

    if selected_index_interval == '1day':
        fig7.add_trace(
            go.Bar(y=ats_pct_1d_last[:10].iloc[::-1].index, x=ats_pct_1d_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(ats_pct_1d_last[:10].iloc[::-1].values, decimals=2)
        xindex = ats_pct_1d_last[:10].iloc[::-1].index

if selected_index == 'TPS':
    tps_pct_5min = df_initial_tps.pct_change().fillna(0) * 100
    tps_pct_5min_last = tps_pct_5min.iloc[-1].sort_values(ascending=False, inplace=False)
    tps_pct_1h = df_initial_tps.pct_change(12).fillna(0) * 100
    tps_pct_1h_last = tps_pct_1h.iloc[-1].sort_values(ascending=False, inplace=False)
    tps_pct_4h = df_initial_tps.pct_change(48).fillna(0) * 100
    tps_pct_4h_last = tps_pct_4h.iloc[-1].sort_values(ascending=False, inplace=False)
    tps_pct_1d = df_initial_tps.pct_change(288).fillna(0) * 100
    tps_pct_1d_last = tps_pct_1d.iloc[-1].sort_values(ascending=False, inplace=False)
    fig7 = go.Figure()
    if selected_index_interval == '5min':
        fig7.add_trace(
            go.Bar(y=tps_pct_5min_last[:10].iloc[::-1].index, x=tps_pct_5min_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(tps_pct_5min_last[:10].iloc[::-1].values, decimals=2)
        xindex = tps_pct_5min_last[:10].iloc[::-1].index

    if selected_index_interval == '1hour':
        fig7.add_trace(
            go.Bar(y=tps_pct_1h_last[:10].iloc[::-1].index, x=tps_pct_1h_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(tps_pct_1h_last[:10].iloc[::-1].values, decimals=2)
        xindex = tps_pct_1h_last[:10].iloc[::-1].index

    if selected_index_interval == '4hour':
        fig7.add_trace(
            go.Bar(y=tps_pct_4h_last[:10].iloc[::-1].index, x=tps_pct_4h_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(tps_pct_4h_last[:10].iloc[::-1].values, decimals=2)
        xindex = tps_pct_4h_last[:10].iloc[::-1].index

    if selected_index_interval == '1day':
        fig7.add_trace(
            go.Bar(y=tps_pct_1d_last[:10].iloc[::-1].index, x=tps_pct_1d_last[:10].iloc[::-1].values, marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ), orientation='h'))
        y_s = np.round(tps_pct_1d_last[:10].iloc[::-1].values, decimals=2)
        xindex = tps_pct_1d_last[:10].iloc[::-1].index

fig7.update_layout(
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
    ),

    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=False,
        showgrid=False,
    ),

    legend=dict(x=0.029, y=1.038, font_size=10),
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
)

annotations = []

# Adding labels
for yd, xd in zip(y_s, xindex):
    annotations.append(dict(xref='x1', yref='y1',
                            y=xd, x=yd + 66,
                            text=str(yd) + '%',
                            font=dict(family='Arial', size=12,
                                      color='rgb(50, 171, 96)'),
                            showarrow=False))

fig7.update_layout(title_text="Percentage evolution of  " + selected_index + " in the last "+selected_index_interval,annotations=annotations)

st.header('**Top 10 Watch ATS/TPS List**')
st.plotly_chart(fig7)

fig4 = go.Figure()
x1=rawbtc.timestamp
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
fig4.update_xaxes(matches='x1')

# Add figure title
fig4.update_layout(title_text=" close btc and crypto", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                   width=800,
                   height=500,hovermode='x unified')

# Set x-axis title
fig4.update_xaxes(showgrid=False, title_text="datetime")
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
fig4.update_yaxes(showgrid=False, title_text="<b>close " + str(selected_crypto) + "</b>  ", secondary_y=False)
fig4.update_yaxes(showgrid=False, title_text="<b>close_btc</b> ", secondary_y=True)

st.header('**Closing Price**')

st.plotly_chart(fig4)

fig5 = go.Figure()
#fig5 = make_subplots(rows=3, cols=1)
fig5 = make_subplots(rows=5, cols=1, shared_xaxes=True,
                    specs=[[{"secondary_y": True}],[{"secondary_y": True}],[{"secondary_y": True}],[{"secondary_y": True}],[{"secondary_y": True}]])
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')), row=1,
               col=1, secondary_y=False,)
fig5.add_trace(go.Scatter(x=rawbtc.timestamp, y=rawbtc['close'],name='close BTC',line=dict(width=2,
                         color='rgb(229, 151, 50)')), row=1,
               col=1, secondary_y=True,)
fig5.add_trace(
    go.Scatter(x=df_initial_ats.index, y=df_initial_ats[selected_crypto_fi], name="ats " + selected_crypto_fi ,visible='legendonly'), row=2,
    col=1, secondary_y=False,)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and ats_index' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')), row=2,
               col=1, secondary_y=True,)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats[selected_crypto_fi].rolling(6).mean(),
                          name="MAVG_ats " + selected_crypto_fi, line=dict(width=2,
                                                                    color='rgb(0, 0, 250)')), row=2, col=1, secondary_y=False)

fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats["mean"], name='ats_weighted_global', visible='legendonly'), row=3, col=1, secondary_y=False,)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and ats_index' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')), row=3,
               col=1, secondary_y=True,)
fig5.add_trace(
    go.Scatter(x=df_initial_ats.index, y=df_initial_ats["mean"].rolling(6).mean(), name="MAVG_ats_weighted_global ", line=dict(width=2,
                                                                    color='rgb(0, 0, 250)')
               ), row=3, col=1, secondary_y=False)


fig5.add_trace(
    go.Scatter(x=df_initial_tps.index, y=df_initial_tps[selected_crypto_fi], name="tps " + selected_crypto_fi, line=dict(width=2,
                                                                    color='rgb(250, 0, 0)')), row=4,
    col=1, secondary_y=False)
fig5.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps[selected_crypto_fi].rolling(6).mean(),
                          name="MAVG_tps " + selected_crypto_fi, visible='legendonly'), row=4, col=1, secondary_y=False)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and tps_index' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')), row=4,
               col=1, secondary_y=True,)

fig5.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps["mean"], name='tps_weighted_global', line=dict(width=2,
                                                                    color='rgb(250, 0, 0)')), row=5, col=1, secondary_y=False)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and ats_index' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')), row=5,
               col=1, secondary_y=True,)
fig5.add_trace(
    go.Scatter(x=df_initial_tps.index, y=df_initial_tps["mean"].rolling(6).mean(), name="MAVG_tps_weighted_global ",
               visible='legendonly'), row=5, col=1, secondary_y=False)
fig5.update_xaxes(matches='x1')

fig5.update_layout(title_text="Side By Side ATS/TPS " + selected_crypto + " ATS/TPS GLOBAL", paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',hovermode='x unified', width=800,
                   height=700,yaxis=dict(title="close price"),yaxis3=dict(title="ats index"),yaxis5=dict(title="ats global index"),yaxis7=dict(title="tps index"),yaxis9=dict(title="tps global index"))
st.header('**Side By Side ATS/TPS**')

st.plotly_chart(fig5)






# Ticker data
st.header('**Cypto data Summary**')
st.write(rawfinal)
