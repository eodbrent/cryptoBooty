import requests
import discord
import CoinMarketCap
import coindeskWrap
#https://www.cryptopia.co.nz/api/GetMarket/DOT_BTC

def getTickerData(pair):
    url = "https://www.cryptopia.co.nz/api/GetMarket/" + pair

    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()["Data"]

    return None

def getTickerMessage(ticker, pair, fiat):
    coin = CoinMarketCap.getReadableCoinName(pair.split("_")[0])

    price = "Current Price: `" + "{:.8f}".format(ticker["LastPrice"])
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = float(ticker["LastPrice"]) * float(fiatConv["rate_float"])
        fin = fin
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = float(ticker["LastPrice"]) * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pair.split("_")[0] + ")"

    changeNum = ticker["Change"]
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + str(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via Cryptopia | ?help for more bot info")

    return embed
