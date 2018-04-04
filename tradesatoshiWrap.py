import requests
import discord
import CoinMarketCap
import coindeskWrap

# Returns ticker data from Bittrex for the given currency pair
def getTickerData(pair):
    url = "https://tradesatoshi.com/api/public/getticker?market=" + pair

    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()["result"]
    return None

def getTickerMessage(ticker, pair, fiat):
    pairsplit = pair.split("_")

    pairN = pairsplit[0]
    coin = CoinMarketCap.getReadableCoinName(pairN)

    price = "Current Price: `" + "{:.8f}".format(ticker["last"])
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = ticker["last"] * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = ticker["last"] * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pairN + ")"

    # changeNum = round(((ticker["Last"] - ticker["PrevDay"]) / ticker["PrevDay"]) * 100, 2)
    # sign = "+" if changeNum > 0 else ""
    # change = "24hr Percent Change: ```diff\n" + sign + str(changeNum) + "%```"
    change = "24hr Percent Change: ```diff\n Not supported by TradeSatoshi API```"

    data = final + change

    # if changeNum < 0:
    #     col = 0xFF0000
    # elif changeNum > 0:
    #     col = 0x00ff00
    col = 0x630057  # just make it purple for now, until tradesatoshi supports change %

    embed = discord.Embed(title=header, description=data, color=col)
    embed.set_footer(text = "via TradeSatoshi  | ?help for more bot info")

    return embed