import requests
import discord
import CoinMarketCap
import coindeskWrap
# Returns ticker data from Binance for the given currency pair
def getTickerData(pair):
    url = "https://api.binance.com/api/v1/ticker/24hr?symbol=" + pair

    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()

    return None

def getTickerMessage(ticker, pair, fiat):
    pairPri = pair[:-3]
    coin = CoinMarketCap.getReadableCoinName(pairPri)

    price = "Current Price: `" + ticker["lastPrice"]
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = float(ticker["lastPrice"]) * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = float(ticker["lastPrice"]) * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"


    header = coin + " (" + pairPri + ")"
    final = price + fiatDisplay

    changeNum = float(ticker["priceChangePercent"])
    sign = "+" if changeNum > 0 else ""
    change = "24hr Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via Binance | ?help for more bot info")

    return embed
