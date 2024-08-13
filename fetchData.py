from kiteconnect import KiteConnect, KiteTicker
import logging
from datetime import datetime
import pandas as pd
from utils import getStocks as gs
import connect
import time
import json
# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Your Zerodha API credentials
# api_key = "YOUR_API_KEY"
# api_secret = "YOUR_API_SECRET"
# access_token = "YOUR_ACCESS_TOKEN"

# # Initialize KiteConnect
# kite = KiteConnect(api_key=api_key)

# # Set access token
# kite.set_access_token(access_token)

# # Initialize KiteTicker
# kws = KiteTicker(api_key, access_token)

# # Dictionary to store the latest tick data for each instrument
latest_ticks = {}

def on_ticks(ws, ticks,count):
    all_dataframes=[]
    for tick in ticks:
        instrument_token = tick['instrument_token']
        latest_ticks[instrument_token] = tick
        
        # Print the real-time data
        df= store_tick_data(tick)
        all_dataframes.append(df)
    
    combined_df= pd.concat(all_dataframes, ignore_index=True)
    combined_df.to_csv(f"storageBuffer/DataValues{count}.csv")

def on_connect(ws, response,kite):
    logging.debug("Successfully connected. Response: {}".format(response))
    
    # Define the list of stocks you want to track (replace with your desired stocks)
    stocks = gs.get_the_ticker_codes()
    new_stocks= [stk[:-3] for stk in stocks]
    
    # Get instrument tokens for the stocks
    instruments = kite.instruments("NSE")
    stock_tokens = [instrument['instrument_token'] for instrument in instruments if instrument['tradingsymbol'] in new_stocks]
    mapp={}
    for k,v in zip(stock_tokens,new_stocks):
        mapp[k]=mapp[v]
    
    with open('ALLSTOCKJSON.json','w') as f:
        json.dump(mapp,f,indent=2)
    
    with open("tempStocks.txt",'w') as fl:
        fl.write(str(stock_tokens))
    print(stock_tokens)
    
    # Subscribe to the stock tokens
    ws.subscribe(stock_tokens)
    ws.set_mode(ws.MODE_FULL, stock_tokens)

def on_close(ws, code, reason):
    logging.debug("Connection closed: {code} - {reason}".format(code=code, reason=reason))

def store_tick_data(tick):
    print("===KEYS===")
    print(tick.keys())
    with open('dictJSON.json','w') as ff:
        json.dump(tick,ff,indent=2)
    with open('ALLSTOCKJSON.json','r') as f:
        mapp= json.load(f)

    timestamp = tick['exchange_timestamp']
    df = pd.DataFrame({
            'timestamp': [timestamp],
            'symbol': [mapp[tick['instrument_token']]],
            'ltp': [tick['last_price']],
            'ltq':[tick['last_traded_quantity']],
            'avg_traded_price':[tick['average_traded_price']],
            'ltt':[tick['last_trade_time']],
            'change': [tick['change']],
            'volume': [tick['volume_traded']],
            'buy_qty':[tick['total_buy_quantity']],
            'sell_qty':[tick['total_sell_quantity']],
            'open': [tick['ohlc']['open']],
            'high': [tick['ohlc']['high']],
            'low': [tick['ohlc']['low']],
            'close': [tick['ohlc']['close']]
        })
    # all_dataframes.append(df)
    return df



if __name__=='__main__':
    kite,kws= connect.getKite()
    kws.on_connect= lambda ws, response: on_connect(ws,response,kite=kite)
    c=1
    kws.on_ticks= lambda ws, response: on_ticks(ws,response,count=c)
    kws.on_close = on_close
    c+=1
    kws.connect(threaded=True)
    while True:
        time.sleep(2)
    


# Assign the callbacks
# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.on_close = on_close

# # Connect to the WebSocket
# kws.connect(threaded=True)

# # Keep the main thread running
# import time
# while True:
#     time.sleep(1)