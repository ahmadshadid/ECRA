import streamlit as st
import pandas as pd

import numpy as np
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta
from plotly.subplots import make_subplots

from mongodbcon import crypto_klines, load_data,load_tps_rps

st.set_page_config(layout="wide")
st.sidebar.image("wbor.png", use_column_width=True)
st.title('Cryptos Exploration')

st.markdown("""
This app fro analysing cryptos 
""")

st.sidebar.header('User Input Features')

list_crypto=crypto_klines.distinct('symbol')
selected_crypto = st.sidebar.selectbox('Crypto', list_crypto)


# Web scraping of NBA player stats



rawfinal = load_data(selected_crypto)

#rawfinal = raw[(raw.timestamp >= '2021-10-14 23:05:00') & (raw.timestamp <= '2021-10-16 15:00:00')]
rawbtc = load_data("BTCUSDT")
#rawbtc = rawbtc[(rawbtc.timestamp >= '2021-10-14 23:05:00') & (rawbtc.timestamp <= '2021-10-16 15:00:00')]

##ats exploration
df_initial_ats = load_tps_rps('rps_raw')
df_initial_ats['timeStamp'] = pd.to_datetime(df_initial_ats['date'])
df_initial_ats.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_ats.drop(['date'], axis=1, inplace=True)
df_initial_ats.set_index('timeStamp', inplace=True)
df_initial_ats["mean"] = df_initial_ats.mean(axis=1)

##tps global exploration

df_initial_ats_global = load_tps_rps('rps_global')
df_initial_ats_global['timeStamp'] = pd.to_datetime(df_initial_ats_global['date'])
df_initial_ats_global.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_ats_global.drop(['date'], axis=1, inplace=True)
df_initial_ats_global.set_index('timeStamp', inplace=True)

##tps exploration
df_initial_tps = load_tps_rps('tps_raw')
df_initial_tps['timeStamp'] = pd.to_datetime(df_initial_tps['date'])
df_initial_tps.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_tps.drop(['date'], axis=1, inplace=True)
df_initial_tps.set_index('timeStamp', inplace=True)
df_initial_tps["mean"] = df_initial_tps.mean(axis=1)

##tps global exploration
df_initial_tps_global = load_tps_rps('tps_global')
df_initial_tps_global['timeStamp'] = pd.to_datetime(df_initial_tps_global['date'])
df_initial_tps_global.replace([np.inf, -np.inf], np.nan, inplace=True)
df_initial_tps_global.drop(['date'], axis=1, inplace=True)
df_initial_tps_global.set_index('timeStamp', inplace=True)


# substring a string to have btc not btcusdt
indexfi = selected_crypto.find('USDT')
selected_crypto_fi = selected_crypto[0:indexfi]

st.sidebar.header('Index Watch List')
list_index = ['TPS', 'ATS']
selected_index = st.sidebar.selectbox('Index', list_index)
list_index_interval = ['1hour', '4hour', '1day']
selected_index_interval = st.sidebar.selectbox('Interval', list_index_interval)
if selected_index == 'ATS':

    ats_pct_1h = df_initial_ats.pct_change(4).fillna(0) * 100
    ats_pct_1h_last = ats_pct_1h.iloc[-1].sort_values(ascending=False, inplace=False)
    ats_pct_4h = df_initial_ats.pct_change(16).fillna(0) * 100
    ats_pct_4h_last = ats_pct_4h.iloc[-1].sort_values(ascending=False, inplace=False)
    ats_pct_1d = df_initial_ats.pct_change(96).fillna(0) * 100
    ats_pct_1d_last = ats_pct_1d.iloc[-1].sort_values(ascending=False, inplace=False)
    fig7 = go.Figure()

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
    tps_pct_1h = df_initial_tps.pct_change(12).fillna(0) * 100
    tps_pct_1h_last = tps_pct_1h.iloc[-1].sort_values(ascending=False, inplace=False)
    tps_pct_4h = df_initial_tps.pct_change(48).fillna(0) * 100
    tps_pct_4h_last = tps_pct_4h.iloc[-1].sort_values(ascending=False, inplace=False)
    tps_pct_1d = df_initial_tps.pct_change(288).fillna(0) * 100
    tps_pct_1d_last = tps_pct_1d.iloc[-1].sort_values(ascending=False, inplace=False)
    fig7 = go.Figure()

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
    autosize=True,
    #width=1500,
    height=500,
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
st.plotly_chart(fig7,use_container_width=True)

fig4 = go.Figure()
x1=rawbtc.timestamp
fig4 = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig4.add_trace(
    go.Scatter(x=rawbtc.timestamp, y=rawbtc['close'],
               name='close BTC',
               line=dict(width=2,
                         color='rgb(229, 151, 50)')),
    secondary_y=True,
)
fig4.add_trace(
    go.Scatter(x=rawfinal.timestamp, y=rawfinal['close'],
               name='close' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')),
    secondary_y=False,
)
fig4.update_xaxes(automargin=True)

# Add figure title
fig4.update_layout(title_text=" close btc and "+selected_crypto+" crypto", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                   #width=1500,
                   height=500,hovermode='x')

# Set x-axis title
fig4.update_xaxes(showgrid=False, title_text="datetime")
fig4.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1h", step="hour", stepmode="backward"),
            dict(count=4, label="4h", step="hour", stepmode="backward"),
            dict(count=24, label="1d", step="hour", stepmode="todate"),
            dict(count=15, label="15d", step="day", stepmode="backward"),
            dict(step="all")
        ])
    ))
fig4.update_xaxes(rangeselector_font_color="#1e222d")
# Set y-axes titles
fig4.update_yaxes(showgrid=False, title_text="<b>close " + str(selected_crypto) + "</b>  ", secondary_y=False)
fig4.update_yaxes(showgrid=False, title_text="<b>close_btc</b> ", secondary_y=True)
fig4.update_yaxes(automargin=True)
st.header('**Closing Price**')

st.plotly_chart(fig4,use_container_width=True)

fig5 = go.Figure()
fig5 = make_subplots(rows=5, cols=1, shared_xaxes=True,
                    specs=[[{"secondary_y": True}],[{"secondary_y": True}],[{"secondary_y": True}],[{"secondary_y": True}],[{"secondary_y": True}]])
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close' + ' ' + str(selected_crypto), line=dict(width=2,
                                                                    color='rgb(229, 151, 250)')), row=1,
               col=1, secondary_y=False,)
fig5.add_trace(go.Scatter(x=rawbtc.timestamp, y=rawbtc['close'],name='close BTC',line=dict(width=2,
                         color='rgb(229, 151, 50)')), row=1,
               col=1, secondary_y=True,)
#fig5.add_trace( go.Scatter(x=df_initial_ats.index, y=df_initial_ats[selected_crypto_fi], name="ats " + selected_crypto_fi ,visible='legendonly'), row=2, col=1, secondary_y=False,)
#fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close_with_ats' + ' ' + str(selected_crypto),visible='legendonly', line=dict(width=2,color='rgb(229, 151, 250)')), row=2,col=1, secondary_y=True,)
fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats[selected_crypto_fi].rolling(20).mean(),
                          name="MAVG_ats " + selected_crypto_fi, line=dict(width=2,
                                                                    color='rgba(0, 181, 204, 1)')), row=2, col=1, secondary_y=False)

#fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=df_initial_ats_global["rps_global"], name='ats_weighted_global', visible='legendonly'), row=3, col=1, secondary_y=False,)
#fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and global_ats_index' + ' ' + str(selected_crypto),visible='legendonly', line=dict(width=2,color='rgb(229, 151, 250)')), row=3,col=1, secondary_y=True,)
fig5.add_trace(
    go.Scatter(x=df_initial_ats.index, y=df_initial_ats_global["rps_global"].rolling(20).mean(), name="MAVG_ats_weighted_global ", line=dict(width=2,
                                                                    color='rgba(0, 181, 204, 1)')
               ), row=3, col=1, secondary_y=False)


fig5.add_trace(
    go.Scatter(x=df_initial_tps.index, y=df_initial_tps[selected_crypto_fi], name="tps " + selected_crypto_fi, line=dict(width=2,
                                                                    color='rgb(250, 0, 0)')), row=4,
    col=1, secondary_y=False)
#fig5.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps[selected_crypto_fi].rolling(20).mean(),name="MAVG_tps " + selected_crypto_fi, visible='legendonly'), row=4, col=1, secondary_y=False)
#fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and tps_index' + ' ' + str(selected_crypto), visible='legendonly', line=dict(width=2,color='rgb(229, 151, 250)')), row=4,col=1, secondary_y=True,)

fig5.add_trace(go.Scatter(x=df_initial_tps.index, y=df_initial_tps_global["tps_global"], name='tps_weighted_global', line=dict(width=2,
                                                                    color='rgb(250, 0, 0)')), row=5, col=1, secondary_y=False)
#fig5.add_trace(go.Scatter(x=df_initial_ats.index, y=rawfinal['close'], name='close and ats_index' + ' ' + str(selected_crypto), visible='legendonly', line=dict(width=2, color='rgb(229, 151, 250)')), row=5,col=1, secondary_y=True,)
#fig5.add_trace( go.Scatter(x=df_initial_tps.index, y=df_initial_tps_global["tps_global"].rolling(20).mean(), name="MAVG_tps_weighted_global ", visible='legendonly'), row=5, col=1, secondary_y=False)
fig5.update_xaxes(matches='x1',automargin=True,showgrid=False,
        showline=False)

fig5.update_layout(title_text="Side By Side ATS/TPS " + selected_crypto + " ATS/TPS GLOBAL", paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',hovermode='x',height=800,
                   #width=1500,
                   autosize=True,yaxis=dict(title="close price"),yaxis3=dict(title="ats index"),yaxis5=dict(title="ats global index"),yaxis7=dict(title="tps index"),yaxis9=dict(title="tps global index"))
fig5.update_yaxes(automargin=True,showgrid=False,
        showline=False)

st.header('**Side By Side ATS/TPS**')

st.plotly_chart(fig5,use_container_width=True)






# Ticker data
st.header('**Cypto data Summary**')
st.write(rawfinal)
