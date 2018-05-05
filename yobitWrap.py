import requests
import discord
import CoinMarketCap
import coindeskWrap
# Returns ticker data from Binance for the given currency pair

# TODO GET FULL NAME FOR CURRENCY
def getTickerData(pair):
    url = "https://yobit.net/api/3/ticker/" + pair
    ticker = requests.get(url)
    if ticker.status_code == 200:
        result = ticker.json()[pair]
        if result["error"]:
            return None
        else:
            return ticker.json()[pair]
    return None

# Returns formatted market data for the bot to send
# TODO PUT IN DOLLAR VALUE
def getTickerMessage(ticker, pair, fiat):
    pair = pair.upper()
    pairPri = pair.split('_')[0]
    coin = CoinMarketCap.getReadableCoinName(pairPri)

    price = "Current Price: `" + "{:.8f}".format(ticker["last"])
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = float(ticker["last"]) * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = float(ticker["last"]) * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pairPri + ")"

    # changeNum = round(((ticker["Last"] - ticker["PrevDay"]) / ticker["PrevDay"]) * 100, 2)
    # sign = "+" if changeNum > 0 else ""
    # change = "24hr Percent Change: ```diff\n" + sign + str(changeNum) + "%```"
    change = "24hr Percent Change: ```diff\n Not supported by YoBit API```"

    data = final + change

    # if changeNum < 0:
    #     col = 0xFF0000
    # elif changeNum > 0:
    #     col = 0x00ff00
    col = 0x630057  # just make it purple for now, until yobit supports change %

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via YoBit | ?help for more bot info")

    return embed
