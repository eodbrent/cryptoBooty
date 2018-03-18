import requests
import discord
import CoinMarketCap

def getTickerData(pair):
    url = "https://nanex.co/api/public/ticker/" + pair
    ticker = requests.get(url)

    if ticker.status_code == 200:
        return ticker.json()

    return None


# Returns formatted market data for the bot to send
# TODO PUT IN DOLLAR VALUE
def getTickerMessage(ticker, pair):

    #search for the name with coinmarketcap

    #switch pair to send to coinmarketcap class 'LTC'_BTC
    # pair = CoinMarketCap.search()
    pairN = pair[3:]
    coin = CoinMarketCap.getReadableCoinName(pairN)
    flLast = float(ticker["last_trade"])
    #flHigh = float(ticker[pair]["h"][1])
    #flLow = float(ticker["l"][1])
    flVol = float(ticker["quote_volume"])
    flOpen = float(ticker["price_change"])
    header = coin + " (" + pairN + ") - Nanex"
    price = "Current Price: `" + "{:.2f}".format(flLast) + "`\n"
    high = "24hr High: `" + "not supported by Nanex`\n"
    low = "24hr Low: `" + "not supported by Nanex`\n"
    volume = "24hr Volume: `" + "{:.2f}".format(flVol) + "`\n"

    changeNum = flOpen
    sign = "+" if changeNum > 0 else ""
    change = "Percent Change: ```diff\n" + sign + "{:.2f}".format(changeNum) + "%```"

    data = price + volume + high + low + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col) #col
    embed.set_footer(text = "")

    return embed