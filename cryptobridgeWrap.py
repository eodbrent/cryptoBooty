import requests
import discord
import CoinMarketCap
import coindeskWrap

# Returns ticker data from Bittrex for the given currency pair
def getTickerData(pair):
    url = "https://api.crypto-bridge.org/api/v1/ticker"
    test = pair
    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()
        currencies = data
        for id in currencies:
            if id["id"] == pair:
                return id
    return None

def getTickerMessage(ticker, pair, fiat):
    pairsplit = pair.split("_")
    coin = CoinMarketCap.getReadableCoinName(pairsplit[0])

    flLast = float(ticker["last"])
    price = "Current Price: `" + "{:.8f}".format(flLast)
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = flLast * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = flLast * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pairsplit[0] + ")"

    # changeNum = round(((ticker["Last"] - ticker["PrevDay"]) / ticker["PrevDay"]) * 100, 2)
    # sign = "+" if changeNum > 0 else ""
    # change = "24hr Percent Change: ```diff\n" + sign + str(changeNum) + "%```"
    change = "24hr Percent Change: ```diff\n Not supported by CryptoBridge API```"

    data = final + change

    # if changeNum < 0:
    #     col = 0xFF0000
    # elif changeNum > 0:
    #     col = 0x00ff00
    col = 0x630057  #just make it purple for now, until cryptobridge supports change %

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via CryptoBridge | ?help for more bot info")

    return embed