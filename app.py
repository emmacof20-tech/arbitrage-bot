from flask import Flask, request
import requests
import time
import os
import threading

app = Flask(__name__)

TELEGRAM_TOKEN = "8668464561:AAFCuZYgojo0VLaZLfP8mCJSAWTx4CJTBoU"
CHAT_ID = "6796711119"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
    except:
        pass

def check_arbitrage():
    coins = {
        "SOL": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=SOLUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=SOL-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=SOL-USDT"
        },
        "DOGE": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=DOGEUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=DOGE-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=DOGE-USDT"
        },
        "XRP": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=XRPUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=XRP-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=XRP-USDT"
        },
        "ADA": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=ADAUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=ADA-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=ADA-USDT"
        },
        "LINK": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=LINKUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=LINKUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=LINK-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=LINK-USDT"
        },
        "SUI": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=SUIUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=SUIUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=SUI-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=SUI-USDT"
        },
        "TON": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=TONUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=TON-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=TON-USDT"
        },
        "MNT": {
            "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=MNTUSDT",
            "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=MNTUSDT",
            "OKX": "https://www.okx.com/api/v5/market/ticker?instId=MNT-USDT",
            "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=MNT-USDT"
        }
    }
    
    for coin, exchanges in coins.items():
        prices = {}
        for exchange, url in exchanges.items():
            try:
                r = requests.get(url, timeout=5)
                data = r.json()
                
                if "binance" in url:
                    prices[exchange] = float(data["price"])
                elif "bybit" in url:
                    prices[exchange] = float(data["result"]["list"][0]["lastPrice"])
                elif "okx" in url:
                    prices[exchange] = float(data["data"][0]["last"])
                elif "kucoin" in url:
                    prices[exchange] = float(data["data"]["price"])
            except:
                pass
        
        if len(prices) >= 2:
            min_ex = min(prices, key=prices.get)
            max_ex = max(prices, key=prices.get)
            diff = ((prices[max_ex] - prices[min_ex]) / prices[min_ex]) * 100
            
            if diff > 0.5:
                msg = f"🚨 {coin} ARBITRAGE!\nBuy {min_ex}: ${prices[min_ex]:.4f}\nSell {max_ex}: ${prices[max_ex]:.4f}\nProfit: {diff:.2f}%"
                send_message(CHAT_ID, msg)

@app.route(f'/webhook/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        if text == '/start':
            send_message(chat_id, "🤖 Arbitrage Bot active!\nMonitoring: SOL, DOGE, XRP, ADA, LINK, SUI, TON, MNT\nAlert when profit > 0.5%")
    return 'ok', 200

@app.route('/')
def home():
    return "Arbitrage Bot is running!"

def run_arbitrage():
    while True:
        check_arbitrage()
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_arbitrage).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
