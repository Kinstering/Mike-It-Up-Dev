from settings import *
import os
import websocket
import json
import pandas as pd
import asyncio
import time
import datetime
import requests
import rel
import numpy as np
import pickle

was_time = 0
total_a_df = pd.DataFrame({'coin': pd.Series(dtype='str'),
                           'v': pd.Series(dtype='float'),
                           'price': pd.Series(dtype='float')})

total_b_df = pd.DataFrame({'coin': pd.Series(dtype='str'),
                           'v': pd.Series(dtype='float'),
                           'price': pd.Series(dtype='float')})


api_key = "3NQ3eBCvOnTDpmkO6yOI7SkqoKvLhpF2ddFyaYWEQf0QmLyweQgx6Oyw62q5xNC9"
api_secret = "YcOEDE19tnJIRZJxgI9hEugVmha4grCrEXDCJH7kNRJtdIwN38QO9FjFc71n636c"

BINANCE_END_POINT = "https://api.binance.com/api/v3/userDataStream"
BINANCE_FUTURES_END_POINT = "https://fapi.binance.com/fapi/v1/listenKey"
real_time_price = {}
# 'ONGUSDT', , 'IDUSDT'
max_coin_v_1h = {}


def create_spot_listen_key(api_key):
    response = requests.post(url=BINANCE_END_POINT, headers={'X-MBX-APIKEY': api_key})
    return response.json()['listenKey']

def on_message(ws, message, n):
    global was_time
    global total_a_df

    global total_b_df

    global real_time_price

    if os.path.exists(f'data/asks_{n}.csv')==False:        total_a_df     = total_a_df[0:0]

    if os.path.exists(f'data/bids_{n}.csv')==False:        total_b_df     = total_b_df[0:0]

    response = json.loads(message)
    if message.find('depthUpdate') > 0:
        df_b = pd.DataFrame(response['b'], columns=['price', 'v'])
        df_b[["price", "v"]] = df_b[["price", "v"]].apply(pd.to_numeric)
        df_b['coin'] = response['s']
        df_a = pd.DataFrame(response['a'], columns=['price', 'v'])
        df_a[["price", "v"]] = df_a[["price", "v"]].apply(pd.to_numeric)
        df_a['coin'] = response['s']

        if (len(df_b) > 0):
            total_b_df = pd.concat([total_b_df, df_b])

        if (len(df_a) > 0):
            total_a_df = pd.concat([total_a_df, df_a])

        now_time = int(int(time.time()) / 5) * 5 * 1000
        if was_time != now_time:
            was_time = now_time
            total_a_df.to_csv(f"data/asks_{n}.csv", sep=',', mode='a', header=not os.path.exists(f"data/asks_{n}.csv"))
            
            total_b_df.to_csv(f'data/bids_{n}.csv', sep=',', mode='a', header=not os.path.exists(f"data/bids_{n}.csv"))


            total_a_df     = total_a_df[0:0]

            total_b_df     = total_b_df[0:0]
            print(f' - asks bids {n} OK')
# --------------------------------------------
def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def main(n, array_count):
    global real_time_price
    websocket.enableTrace(False)
    listen_key = create_spot_listen_key(api_key)
    mystreams = ''
    for cc_ in array_count:
        mystreams = mystreams + '/' + cc_.lower() + '@depth'
    # 'solusdt@depth'
    socket = f'wss://data-stream.binance.com:9443/ws/{listen_key}' + mystreams
    # print(socket)
    ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: on_message(ws, msg, n), on_error=on_error, on_close=on_close)
    ws.run_forever(dispatcher=rel, ping_interval=300, reconnect=20)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()