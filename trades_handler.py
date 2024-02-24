from settings import *
import websocket
import json
import pandas as pd
import time
import requests
import rel
import os

was_time = 0
start_time=0
# ------------------------------------------
def on_message(ws, message, n):
    global was_time
    global total_df

    if os.path.exists(f'data/trades_{n}.csv') == False:     total_df     = total_df[0:0]

    response = json.loads(message)
    df = pd.json_normalize(response)
    df = df.rename(columns={"s": "coin", "p": "price", "q": "amount", "m": "buyer"})
    df = df.drop(['e', 'E', 'a', 'f', 'l', 'T', 'M'], axis=1)
    total_df     = pd.concat([total_df, df])

    now_time = int(int(time.time()) / 16) * 16 * 1000
    if was_time != now_time:
        was_time = now_time
        total_df.to_csv(f"data/trades_{n}.csv", sep=',', mode='a', header=not os.path.exists(f"data/trades_{n}.csv"))

        total_df     = total_df[0:0]

        print(f' - trades {n} OK')
# ------------------------------------------
def on_error(ws, error):
    print(error)
# ------------------------------------------
def on_close(close_msg):
    print("### closed ###" + close_msg)
# ------------------------------------------
def create_spot_listen_key(api_key):
    response = requests.post(url=end_point, headers={'X-MBX-APIKEY': api_key})
    #print(response.json())
    return response.json()['listenKey']
# ------------------------------------------
def CreateStream(n, array_count):
    listen_key = create_spot_listen_key(api_key)
    mystreams =''
    for cc_ in array_count:
        mystreams = mystreams + '/' + cc_.lower() + '@aggTrade'
    socket = f'wss://data-stream.binance.com:9443/ws/{listen_key}' + mystreams
    #print(socket)
    ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: on_message(ws, msg, n), on_error=on_error, on_close=on_close)
    ws.run_forever(dispatcher=rel, ping_interval=300, reconnect=20)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
# --------------------------------------
start_time = int(int(time.time()) / 16) * 16 * 1000