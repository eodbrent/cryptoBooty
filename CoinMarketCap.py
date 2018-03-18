#get full currency name from coinmarket cap
import requests
import discord
import CoinMarketCap
def getReadableCoinName(coin):
    coin = coin.upper()
    url = "https://api.coinmarketcap.com/v1/ticker/"

    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()
        currencies = data
        for symbol in currencies:
            if symbol["symbol"] == coin:
                return symbol["name"]
    return coin

def coinStats():

    url = "https://api.coinmarketcap.com/v1/ticker/"

    ticker = requests.get(url)
    if ticker.status_code == 200:
        data = ticker.json()
        currencies = data
        cmcList = []
        for i in currencies:
            cmcList.append(i["name"] + " (" + i["symbol"] + ")_" + i["price_usd"] + "_" + i["price_btc"] + "_" + i["percent_change_24h"])
            if i == 5:
                break
    cmcFirst = cmcList[0].split("_")
    cmcSecond = cmcList[1].split("_")
    cmcThird = cmcList[2].split("_")
    cmcFourth = cmcList[3].split("_")
    cmcFifth = cmcList[4].split("_")
    first = "`$" + cmcFirst[1] + ", " + cmcFirst[2] + "-BTC, 24h Change: " + cmcFirst[3] + "%`\n"
    second = "`$" + cmcSecond[1] + ", " + cmcSecond[2] + "-BTC, 24h Change: " + cmcSecond[3] + "%`\n"
    third = "`$" + cmcThird[1] + ", " + cmcThird[2] + "-BTC, 24h Change: " + cmcThird[3] + "%`\n"
    fourth = "`$" + cmcFourth[1] + ", " + cmcFourth[2] + "-BTC, 24h Change: " + cmcFourth[3] + "%`\n"
    fifth = "`$" + cmcFifth[1] + ", " + cmcFifth[2] + "-BTC, 24h Change: " + cmcFifth[3] + "%`\n"
    embed = first + second + third + fourth + fifth

    title = "CoinMarketCap Top 5"
    intro = ""
    embed = discord.Embed(title=title, description=intro, color=0x630057)

    embed.add_field(name=cmcFirst[0], value=first)
    embed.add_field(name=cmcSecond[0], value=second)
    embed.add_field(name=cmcThird[0], value=third)
    embed.add_field(name=cmcFourth[0], value=fourth)
    embed.add_field(name=cmcFifth[0], value=fifth)

    return embed
