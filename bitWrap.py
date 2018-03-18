import requests
import discord
import CoinMarketCap

def getReadableCoinName(coin):
    url = "https://bittrex.com/api/v1.1/public/getcurrencies"

    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()
        currencies = data["result"]
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

# Returns formatted market data for the bot to send
def getTickerMessage(ticker, pair):
    ticker = ticker[0]
    coin = getReadableCoinName(pair.split("-")[1])

    header = coin + " (" + pair.split("-")[1] + ") - Bittrex (default)"
    price = "Current Price: `" + "{:.8f}".format(ticker["Last"]) + "`\n"
    high = "24hr High: `" + "{:.8f}".format(ticker["High"]) + "`\n"
    low = "24hr Low: `" + "{:.8f}".format(ticker["Low"]) + "`\n"
    volume = "24hr Volume: `" + "{:.8f}".format(ticker["BaseVolume"]) + "`\n"

    changeNum = round(((ticker["Last"] - ticker["PrevDay"]) / ticker["PrevDay"]) * 100, 2)
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + str(changeNum) + "%```"

    data = price + volume + high + low + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "")

    return embed