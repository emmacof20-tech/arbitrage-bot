import requests
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from flask import Flask
import threading

app = Flask(__name__)

TELEGRAM_TOKEN = "8657139653:AAH0eBi8NzXN1DvTqRQY9tfTGNxHM89ZL3I"
CHAT_ID = "6796711119"

bot = Bot(token=TELEGRAM_TOKEN)

def start(update, context):
    update.message.reply_text("🤖 Arbitrage Bot is active! I'll alert you when SOL price difference > 1.5%")

def check_arbitrage():
    exchanges = {
        "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
        "Bybit": "https://api.bybit.com/v5/market/tickers?category=spot&symbol=SOLUSDT",
        "OKX": "https://www.okx.com/api/v5/market/ticker?instId=SOL-USDT",
        "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=SOL-USDT",
        "Kraken": "https://api.kraken.com/0/public/Ticker?pair=SOLUSD",
        "Coinbase": "https://api.coinbase.com/v2/prices/SOL-USD/spot",
    }
    
    prices = {}
    for name, url in exchanges.items():
        try:
            r = requests.get(url, timeout=5)
            data = r.json()
            if name == "Binance":
                prices[name] = float(data["price"])
            elif name == "Bybit":
                prices[name] = float(data["result"]["list"][0]["lastPrice"])
            elif name == "OKX":
                prices[name] = float(data["data"][0]["last"])
            elif name == "KuCoin":
                prices[name] = float(data["data"]["price"])
            elif name == "Kraken":
                prices[name] = float(data["result"]["XSOLZUSD"]["c"][0])
            elif name == "Coinbase":
                prices[name] = float(data["data"]["amount"])
        except:
            pass
    
    if len(prices) >= 2:
        min_ex = min(prices, key=prices.get)
        max_ex = max(prices, key=prices.get)
        diff = ((prices[max_ex] - prices[min_ex]) / prices[min_ex]) * 100
        
        if diff > 1.5:
            msg = f"🚨 ARBITRAGE!\nBuy {min_ex}: ${prices[min_ex]}\nSell {max_ex}: ${prices[max_ex]}\nProfit: {diff:.2f}%"
            bot.send_message(chat_id=CHAT_ID, text=msg)

def run_bot():
    while True:
        check_arbitrage()
        time.sleep(60)

@app.route('/')
def home():
    return "Arbitrage Bot is running!"

if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    
    thread = threading.Thread(target=run_bot)
    thread.start()
    
    updater.start_polling()
    app.run(host="0.0.0.0", port=10000)
