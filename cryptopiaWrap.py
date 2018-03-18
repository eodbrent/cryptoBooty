import requests
import discord
import CoinMarketCap
#https://www.cryptopia.co.nz/api/GetMarket/DOT_BTC

def getTickerData(pair):
    url = "https://www.cryptopia.co.nz/api/GetMarket/" + pair

    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()["Data"]

    return None

# Returns formatted market data for the bot to send
def getTickerMessage(ticker, pair):
    coin = CoinMarketCap.getReadableCoinName(pair.split("_")[0])

    header = coin + " (" + pair.split("_")[0] + ") - Cryptopia"
    price = "Current Price: `" + "{:.8f}".format(ticker["LastPrice"]) + "`\n"
    high = "24hr High: `" + "{:.8f}".format(ticker["High"]) + "`\n"
    low = "24hr Low: `" + "{:.8f}".format(ticker["Low"]) + "`\n"
    volume = "24hr Volume: `" + "{:.8f}".format(ticker["Volume"]) + "`\n"

    changeNum = ticker["Change"]
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