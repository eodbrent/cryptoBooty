#get full currency name from coinmarket cap
import requests
import discord
import CoinMarketCap
def getReadableCoinName(coin):
    coin = coin.upper()
    url = "https://api.coinmarketcap.com/v1/ticker/"

    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()
        currencies = data
        for symbol in currencies:
            if symbol["symbol"] == coin:
                return symbol["name"]
    return None