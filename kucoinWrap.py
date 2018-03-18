#https://api.kucoin.com/v1/BTCP-BTC/open/tick
import requests
import discord
import CoinMarketCap
import re

# data: "coinType":"XRB"
# Returns ticker data from Kucoin for the given currency pair
def getTickerData(pair):
    url = "https://api.kucoin.com/v1/" + pair + "/open/tick"
    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()["data"]

    return None

# Returns formatted market data for the bot to send
# TODO PUT IN DOLLAR VALUE
def getTickerMessage(ticker, pair):

    coin = CoinMarketCap.getReadableCoinName(ticker["coinType"])

    header = coin + " (" + ticker["coinType"] + ") - Kucoin"
    price = "Current Price: `" + "{:.8f}".format(ticker["lastDealPrice"]) + "`\n"
    high = "24hr High: `" + "{:.8f}".format(ticker["high"]) + "`\n"
    low = "24hr Low: `" + "{:.8f}".format(ticker["low"]) + "`\n"
    volume = "24hr Volume: `" + "{:.8f}".format(ticker["vol"]) + "`\n"

    changeNum = float(ticker["changeRate"])  ###changeRate * 100
    changeNum = changeNum * 100
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = price + volume + high + low + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col) #col
    embed.set_footer(text = "FOOTER")

    return embed