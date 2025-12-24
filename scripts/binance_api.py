import requests as re
import pandas as pd

binance_api = "https://api.binance.com"

def fetch_binance_prices():
    data = re.get(f"{binance_api}/api/v3/ticker/price", timeout = 10).json()
    df = pd.DataFrame(data)
    df["price"] = df["price"].astype(float)
    # Use milliseconds since epoch for compatibility with Cassandra
    df["fetch_time"] = int(time.time() * 1000)
    return df

def fetch_24h_stats():
    data = requests.get(f"{binance_api}/api/v3/ticker/24hr", timeout=10).json()
    df = pd.DataFrame(data)
    df["fetch_time"] = int(time.time() * 1000)
    return df

def fetch_order_book(symbol="BTCUSDT", limit=5):
    data = re.get(f"{binance_api}/api/v3/depth?symbol={symbol}&limit={limit}", timeout=10).json()
    bids = pd.DataFrame(data["bids"], columns=["price", "quantity"])
    asks = pd.DataFrame(data["asks"], columns=["price", "quantity"])
    bids["side"], asks["side"] = "bid", "ask"
    df = pd.concat([bids, asks])
    df["symbol"], df["fetch_time"] = symbol, int(time.time() * 1000)
    df["price"], df["quantity"] = df["price"].astype(float), df["quantity"].astype(float)
    return df