import requests
import discord
import CoinMarketCap
import coindeskWrap

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
def getTickerMessage(ticker, pair, fiat):
    pairID = getID(pair)
    coin = pairID[1]
    tick = getTickerData(pair)

    flLast = float(tick["LastPrice"])
    flChange = float(tick["Change"])
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
    header = coin + " (" + pair + ")"

    changeNum = flChange
    sign = "+" if changeNum > 0 else ""
    change = "24hr Percent Change: ```diff\n" + sign + str(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via CoinExchange  | ?help for more bot info")

    return embed
