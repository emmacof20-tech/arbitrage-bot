import requests
import time
from telegram import Bot

TELEGRAM_TOKEN = "8657139653:AAH0eBi8NzXN1DvTqRQY9tfTGNxHM89ZL3I"
CHAT_ID = "6796711119"

bot = Bot(token=TELEGRAM_TOKEN)

exchanges = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
    "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=SOLUSDT",
    "OKX": "https://www.okx.com/api/v5/market/ticker?instId=SOL-USDT",
    "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=SOL-USDT",
    "Kraken": "https://api.kraken.com/0/public/Ticker?pair=SOLUSD",
    "Coinbase": "https://api.coinbase.com/v2/prices/SOL-USD/spot",
    "Gate.io": "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=SOL_USDT",
    "Huobi": "https://api.huobi.pro/market/detail/merged?symbol=solusdt",
    "Bitstamp": "https://www.bitstamp.net/api/v2/ticker/solusd/",
    "Crypto.com": "https://api.crypto.com/exchange/v1/public/get-ticker?instrument_name=SOL_USDT"
}

def get_price(exchange_name, url):
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if exchange_name == "Binance":
            return float(data["price"])
        elif exchange_name == "Bybit":
            return float(data["result"]["list"][0]["lastPrice"])
        elif exchange_name == "OKX":
            return float(data["data"][0]["last"])
        elif exchange_name == "KuCoin":
            return float(data["data"]["price"])
        elif exchange_name == "Kraken":
            return float(data["result"]["XSOLZUSD"]["c"][0])
        elif exchange_name == "Coinbase":
            return float(data["data"]["amount"])
        elif exchange_name == "Gate.io":
            return float(data[0]["last"])
        elif exchange_name == "Huobi":
            return float(data["tick"]["close"])
        elif exchange_name == "Bitstamp":
            return float(data["last"])
        elif exchange_name == "Crypto.com":
            return float(data["result"]["data"]["i"])
    except Exception as e:
        print(f"{exchange_name} error: {e}")
        return None

def check_arbitrage():
    prices = {}
    for name, url in exchanges.items():
        price = get_price(name, url)
        if price:
            prices[name] = price
            print(f"{name}: ${price}")
    
    if len(prices) < 2:
        return
    
    min_ex = min(prices, key=prices.get)
    max_ex = max(prices, key=prices.get)
    min_price = prices[min_ex]
    max_price = prices[max_ex]
    diff_percent = ((max_price - min_price) / min_price) * 100
    
    if diff_percent > 1.5:
        msg = f"🚨 ARBITRAGE!\nBuy: {min_ex} @ ${min_price}\nSell: {max_ex} @ ${max_price}\nProfit: {diff_percent:.2f}%"
        bot.send_message(chat_id=CHAT_ID, text=msg)
        print(msg)
    else:
        print(f"No profit. Best spread: {diff_percent:.2f}%")

while True:
    check_arbitrage()
    time.sleep(30)
