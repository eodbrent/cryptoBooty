import requests
import discord
import CoinMarketCap
import coindeskWrap

def getTickerData(pair):
    url = "https://nanex.co/api/public/ticker/" + pair
    ticker = requests.get(url)

    if ticker.status_code == 200:
        return ticker.json()

    return None


# Returns formatted market data for the bot to send
def getTickerMessage(ticker, pair, fiat):
    pair = pair.upper()
    pairN = pair[3:]
    pairU = pair[:-4]
    coin = CoinMarketCap.getReadableCoinName(pairN)

    notNano = CoinMarketCap.getCoinData(pairU)

    flLast = float(ticker["last_trade"])
    flOpen = float(ticker["price_change"])

    price = "Current Price: `" + "{:.2f}".format(flLast) + " " + coin + " per " + pairU
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = float(fiatConv["rate_float"]) / flLast
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        fin = float(notNano["price_usd"]) / flLast
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pairN + ")"

    changeNum = flOpen
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via Nanex | ?help for more bot info")

    return embed
