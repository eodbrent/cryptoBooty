import requests
import discord
import CoinMarketCap
# Returns ticker data from Binance for the given currency pair
# TODO GET FULL NAME FOR CURRENCY
def getTickerData(pair):
    url = "https://yobit.net/api/3/ticker/" + pair
    ticker = requests.get(url)
    if ticker.status_code == 200:
        return ticker.json()[pair]

    return None

# Returns formatted market data for the bot to send
# TODO PUT IN DOLLAR VALUE
def getTickerMessage(ticker, pair):

    #search for the name with coinmarketcap

    #switch pair to send to coinmarketcap class 'LTC'_BTC
    pairPri = pair.split('_')[0]
    coin = CoinMarketCap.getReadableCoinName(pairPri)
    header = "(" + coin + ") - YObit"
    price = "Current Price: `" + "{:.8f}".format(ticker["last"]) + "`\n"
    high = "24hr High: `" + "{:.8f}".format(ticker["high"]) + "`\n"
    low = "24hr Low: `" + "{:.8f}".format(ticker["low"]) + "`\n"
    volume = "24hr Volume: `" + "{:.8f}".format(ticker["vol"]) + "`\n"

    #changeNum = float(ticker["priceChangePercent"])
    #sign = "+" if changeNum > 0 else ""
    #change = "Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = price + volume + high + low # change

    # if changeNum < 0:
    #     col = 0xFF0000
    # elif changeNum > 0:
    #     col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = 0xFF0000) #col
    embed.set_footer(text = "FOOTER")

    return embed
