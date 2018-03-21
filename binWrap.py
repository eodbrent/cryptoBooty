import requests
import discord
import CoinMarketCap
# Returns ticker data from Binance for the given currency pair
def getTickerData(pair):
    url = "https://api.binance.com/api/v1/ticker/24hr?symbol=" + pair

    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()

    return None

# Returns formatted market data for the bot to send
def getTickerMessage(ticker, pair):
    pairPri = pair[:-3]
    coin = CoinMarketCap.getReadableCoinName(pairPri)

    header = coin + " (" + pairPri + ") - Binance"
    price = "Current Price: `" + ticker["lastPrice"] + "`\n"
    high = "24hr High: `" + ticker["highPrice"] + "`\n"
    low = "24hr Low: `" + ticker["lowPrice"] + "`\n"
    volume = "24hr Volume: `" + ticker["quoteVolume"] + "`\n"

    changeNum = float(ticker["priceChangePercent"])
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = price + volume + high + low + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "")

    return embed
