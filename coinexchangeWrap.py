import requests
import discord
import CoinMarketCap

#TODO FIRST - GET the correct market ID using the pair
def getID(pair):
    url = "https://www.coinexchange.io/api/v1/getcurrencies"
    ticker = requests.get(url)
    ticker = ticker
    if ticker.status_code == 200:
        data = ticker.json()["result"]
        currencies = data
        pairInfo = []
        for id in currencies:
            if id["TickerCode"] == pair:
                pairInfo.append(id["CurrencyID"])
                pairInfo.append(id["Name"])
                pairInfo.append(id["TickerCode"])
                return pairInfo
    return None

def getTickerData(pair):
    pairID = getID(pair)
    url = "https://www.coinexchange.io/api/v1/getmarketsummaries"
    ticker = requests.get(url)

    if ticker.status_code == 200:
        data = ticker.json()["result"]
        currencies = data
        for id in currencies:
            if id["MarketID"] == pairID[0]:
                return id
    #"MarketID":"18","LastPrice":"0.01895001","Change":"1.55","HighPrice":"0.01919000","LowPrice":"0.01845009","Volume":"7.39267340"
    return None


# Returns formatted market data for the bot to send
# TODO PUT IN DOLLAR VALUE
def getTickerMessage(ticker, pair):
    pairID = getID(pair)
    coin = pairID[1]
    data = getTickerData(pair)

    flLast = float(data["LastPrice"])
    flHigh = float(data["HighPrice"])
    flLow = float(data["LowPrice"])
    flVol = float(data["Volume"])
    flChange = float(data["Change"])
    header = coin + " (" + pair + ") - CurrencyExchange"
    price = "Current Price: `" + "{:.8f}".format(flLast) + "`\n"
    high = "24hr High: `" + "{:.8f}".format(flHigh) + "`\n"
    low = "24hr Low: `" + "{:.8f}".format(flLow) + "`\n"
    volume = "24hr Volume: `" + "{:.8f}".format(flVol) + "`\n"

    changeNum = flChange
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