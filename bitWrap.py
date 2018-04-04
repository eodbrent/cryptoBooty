import requests
import discord
import CoinMarketCap
import coindeskWrap
def getReadableCoinName(coin):
    url = "https://bittrex.com/api/v1.1/public/getcurrencies"

    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()
        currencies = data
        for currency in currencies:
            if currency["Currency"] == coin:
                return currency["CurrencyLong"]

    return None

# Returns ticker data from Bittrex for the given currency pair
def getTickerData(pair):
    url = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + pair

    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()["result"]

    return None

def getTickerMessage(ticker, pair, fiat):
    ticker = ticker[0]
    coin = pair.split("-")[1]
    coin = getReadableCoinName(pair.split("-")[1])

    price = "Current Price: `" + "{:.8f}".format(ticker["Last"])
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = ticker["Last"] * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = ticker["Last"] * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pair.split("-")[1] + ")"

    changeNum = round(((ticker["Last"] - ticker["PrevDay"]) / ticker["PrevDay"]) * 100, 2)
    sign = "+" if changeNum > 0 else ""
    change = "24hr Percent Change: ```diff\n" + sign + str(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via Bittrex | ?help for more bot info")

    return embed
