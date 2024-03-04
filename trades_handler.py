from settings import *
import websocket
import json
import pandas as pd
import time
import requests
import rel
import os
from datetime import datetime, timedelta

was_time = 0
total_df = pd.DataFrame()

# ---------------------------------------
def set_file_name(type_, number_):
    current_time = datetime.now()
    current_minute = current_time.minute
    current_hour = current_time.hour
    current_day = current_time.day
    current_month = current_time.month
    current_year = current_time.year

    minute_interval = (current_minute // 15) * 15
    fname = f"{type_}_{number_}_{current_year}_{current_month}_{current_day}_{current_hour}_{minute_interval}.csv"
    return fname

# ------------------------------------------
def on_message(ws, message, n):
    global was_time
    global total_df

    response = json.loads(message)
    df = pd.json_normalize(response)
    df = df.rename(columns={"s": "coin", "p": "price", "q": "amount", "m": "buyer"})
    df = df.drop(['e', 'E', 'a', 'f', 'l', 'T', 'M'], axis=1)

    total_df = pd.concat([total_df, df])

    now_time = int(int(time.time()) / 900) * 900 * 1000
    if was_time != now_time:
        was_time = now_time
        fname = set_file_name("trades", n)
        total_df.to_csv(f"data/{fname}", sep=',', mode='a', header=not os.path.exists(f"data/{fname}"))
        total_df = total_df[0:0]

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
    return response.json()['listenKey']

# ------------------------------------------
def CreateStream(n, array_count):
    listen_key = create_spot_listen_key(api_key)
    mystreams = ''
    for cc_ in array_count:
        mystreams = mystreams + '/' + cc_.lower() + '@aggTrade'

    socket = f'wss://data-stream.binance.com:9443/ws/{listen_key}' + mystreams

    ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: on_message(ws, msg, n), on_error=on_error, on_close=on_close)
    ws.run_forever(dispatcher=rel, ping_interval=300, reconnect=20)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

# --------------------------------------
start_time = int(int(time.time()) / 16) * 16 * 1000

