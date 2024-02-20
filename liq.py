from settings import *
import websocket
import json
import pandas as pd
import time
import requests
import rel
import os
import pickle

was_time   = 0
start_time = 0
# ------------------------------------------
def on_message(ws, message):
    global was_time
    global liq_df
    global liq_df_15m
    global liq_df_4h

    if os.path.exists('data/liq.csv') == False:     liq_df     = liq_df[0:0]
    if os.path.exists('data/liq_15m.csv') == False: liq_df_15m = liq_df_15m[0:0]
    if os.path.exists('data/liq_4h.csv') == False:  liq_df_4h  = liq_df_4h[0:0]

    response = json.loads(message)
    df = pd.json_normalize(response)
    df = df.rename(columns={"o.s": "coin", "o.p": "price", "o.q": "amount","o.S": "type"})
    df = df.drop(['e', 'E', 'o.o', 'o.f', 'o.ap', 'o.X',  'o.l', 'o.z', 'o.T'], axis=1)
    liq_df = pd.concat([liq_df, df])
    now_time = int(int(time.time()) / 16) * 16 * 1000
    if was_time != now_time:
        was_time = now_time
        liq_df.to_csv("data/liq.csv", sep=',', mode='a', header=not os.path.exists("data/liq.csv"), index=False)
        liq_df_15m.to_csv("data/liq_15m.csv", sep=',', mode='a', header=not os.path.exists("data/liq_15m.csv"), index=False)
        liq_df_4h.to_csv("data/liq_4h.csv", sep=',', mode='a', header=not os.path.exists("data/liq_4h.csv"), index=False)

        liq_df     = liq_df[0:0]
        liq_df_15m = liq_df_15m[0:0]
        liq_df_4h  = liq_df_4h[0:0]
        print(' - Liquidations OK')
# ------------------------------------------
def on_error(ws, error):
    print(error)
# ------------------------------------------
def on_close(close_msg):
    print("### closed ###" + close_msg)
# ------------------------------------------
def CreateLiqStream():
    socket = f'wss://fstream.binance.com/ws/' + '!forceOrder@arr'
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever(dispatcher=rel, ping_interval=300, reconnect=20)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
# --------------------------------------
CreateLiqStream()

