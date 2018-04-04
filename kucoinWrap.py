#https://api.kucoin.com/v1/BTCP-BTC/open/tick
import requests
import discord
import CoinMarketCap
import coindeskWrap
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
def getTickerMessage(ticker, pair, fiat):

    coin = CoinMarketCap.getReadableCoinName(ticker["coinType"])
    btc = coindeskWrap.getTickerData("USD")

    price = "Current Price: `" + "{:.8f}".format(ticker["lastDealPrice"])
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = float(ticker["lastDealPrice"]) * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        fin = ticker["lastDealPrice"] * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + ticker["coinType"] + ")"

    changeNum = float(ticker["changeRate"]) * 100
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via Kucoin | ?help for more bot info")

    return embed
