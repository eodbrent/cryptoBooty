import requests
import discord
import CoinMarketCap
import json
def getPairs():
    url = "https://api.kraken.com/0/public/AssetPairs"
    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()["result"]
        currencies = data
    pairsList = []
    for result in currencies:
        pairsList.append(result)
    return pairsList

def getTickerData(pair):
    #pairsplit = pair.split("_")
    #pair = pairsplit[1] + pairsplit[0]
    pair = pair.upper()
    pair = pair.replace("_", "")
    url = "https://api.kraken.com/0/public/Ticker?pair=" + pair
    ticker = requests.get(url)

    if ticker.status_code == 200:
        return ticker.json()["result"]

    return None


# Returns formatted market data for the bot to send
# TODO PUT IN DOLLAR VALUE
def getTickerMessage(ticker, pair):

    pairN = pair[:-3]
    coin = CoinMarketCap.getReadableCoinName(pairN)

    flLast = float(ticker[pair]["c"][0])
    flHigh = float(ticker[pair]["h"][1])
    flLow = float(ticker[pair]["l"][1])
    flVol = float(ticker[pair]["v"][1])
    flOpen = float(ticker[pair]["o"])
    header = coin + " (" + pairN + ") - Kraken"
    price = "Current Price: `" + "{:.2f}".format(flLast) + "`\n"
    high = "24hr High: `" + "{:.2f}".format(flHigh) + "`\n"
    low = "24hr Low: `" + "{:.2f}".format(flLow) + "`\n"
    volume = "24hr Volume: `" + "{:.2f}".format(flVol) + "`\n"

    changeNum = flOpen / flLast
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
