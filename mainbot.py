import discord
from discord.ext import commands
import poloWrap
import bitWrap
import binWrap
import yobitWrap
import kucoinWrap
import krakenWrap
import nanexWrap
import cryptopiaWrap
import CoinMarketCap
import coinexchangeWrap
import stocksExchangeWrap
import coindeskWrap
import cryptobridgeWrap
import tradesatoshiWrap
import os

Client = discord.Client()
client = commands.Bot(command_prefix = "$")
# TODO CHECKLIST FOR ADDING NEW EXCHANGES
#   ADD to: sptExch list in async def on_message
#   ADD to: wrap in def searchCoin
#   ADD to: def formPair
#   ADD to: fix up wrapper
@client.event
async def on_ready():
    print("BOT IS RUNNING!")
    #
    # start logging /primarily for adding new coins or exchanges
    #   from requests !add
@client.event
async def on_message(message):

    msg = message.content.lower()
    split = msg.split(' ')
    if message.author == client.user or isinstance(message.channel, discord.PrivateChannel):
        return
    sptExch = ["binance", "bittrex", "coinexchange", "cryptopia", "cryptobridge", "kucoin", "nanex", "poloniex", "tradesatoshi", "yobit"]
    if msg.startswith('.'):
        splitmsg = msg.split(" ")
        originalPair = splitmsg[0][1:]
        if len(splitmsg) > 1:
            i = 0
            while i <= len(sptExch):
                if splitmsg[1] == sptExch[i]:
                    found = searchCoin(originalPair, sptExch, sptExch.index(splitmsg[1]), None)
                    break
                i += 1
        elif len(splitmsg) <= 1:
            found = searchCoin(originalPair, sptExch, 0, None)

        await client.send_message(message.channel, embed=found)
    elif msg.startswith('?'):
        sp = split[0:]
        hp = sp[0]
        hp = hp[1:].lower()
        if hp == "help":
            helpMsg = help()
            await client.send_message(message.author, embed=helpMsg)
        if hp == "cmc":
            cmcMsg = CoinMarketCap.coinStats()
            await client.send_message(message.channel, embed=cmcMsg)

def searchCoin(pair, sptExch, num, fiat):
    wrap = [binWrap, bitWrap, coinexchangeWrap, cryptopiaWrap, cryptobridgeWrap, kucoinWrap, nanexWrap, poloWrap, tradesatoshiWrap, yobitWrap]
    pair = pair.upper()
    pairsplit = pair.split("_")

    # CHECK First currency.  If it's a FIAT (found in coindesk), fix the right parameters and recursive call
    cdCurrencies = coindeskWrap.getSupportedCurrencies()
    if pairsplit[0] in cdCurrencies:
        fiat = pairsplit[0]
        pair = "BTC" + "_" + pairsplit[1]
        searchCoin(pair, sptExch, num, fiat)

    i = num

    while i < len(sptExch):
        fmtPair = formPair(sptExch[i], pair)
        try:
            result = wrap[i].getTickerData(fmtPair)
            if result:
                found = wrap[i].getTickerMessage(result, fmtPair, fiat)
                return found
        except:
            print("not on that exchange")
        i += 1
    error = formError(pair + " is not found on exchanges supported by this bot - weird, cause it has a lot!  "
                            "Or, something went terribly wrong and logging isn't built in yet.")
    return error


def formPair(exch, pair):
    if exch == "binance": # ex LTCBTC
        pairsplit = pair.split("_")
        pair = pairsplit[1] + pairsplit[0]
        pair = pair.upper()
        return pair
    elif exch == "bittrex": # ex BTC-LTC
        pair = pair.replace("_", "-")
        pair = pair.upper()
        return pair
    elif exch == "coinexchange": # ex BTC_LTC (Just need tickercode = LTC)
        pairsplit = pair.split("_")
        pair = pairsplit[1]
        pair = pair.upper()
        return pair
    elif exch == "cryptobridge": # ex LTC_BTC
        pairsplit = pair.split("_")
        pair = pairsplit[1] + "_" + pairsplit[0]
        pair = pair.upper()
        return pair
    elif exch == "cryptopia": # ex LTC/BTC
        pairsplit = pair.split("_")
        pair = pairsplit[1] + "_" + pairsplit[0]
        pair = pair.upper()
        return pair
    elif exch == "kraken": # ex BCHUSD
        pair = pair.replace("-", "_")
        pairsplit = pair.split("_")
        pair = pairsplit[0] + pairsplit[1]
        pair = pair.upper()
        return pair
    elif exch == "kucoin": # ex LTC-BTC
        pair = pair.replace("_", "-")
        pairsplit = pair.split("-")
        pair = pairsplit[1] + "-" + pairsplit[0]
        pair = pair.upper()
        return pair
    elif exch == "nanex": # ex btcnano
        pair = pair.replace("-", "_")
        pairsplit = pair.split("_")
        pair = pairsplit[0] + pairsplit[1]
        pair = pair.lower()
        return pair
    elif exch == "poloniex": # ex BTC_LTC
        # THIS IS HOW USERS WILL INPUT...do nothing / except ensure uppercase
        pair = pair.upper()
        return pair
    elif exch == "stocksexchange": # ex LTC_BTC
        pairsplit = pair.split("_")
        pair = pairsplit[1] + "_" + pairsplit[0]
        pair = pair.upper()
        return pair
    elif exch == "tradesatoshi": # ex LTC_BTC
        pairsplit = pair.split("_")
        pair = pairsplit[1] + "_" + pairsplit[0]
        pair = pair.upper()
        return pair
    elif exch == "yobit": # ex ltc_btc
        pair = pair.replace("-", "_")
        pairsplit = pair.split("_")
        pair = pairsplit[1] + "_" + pairsplit[0]
        pair = pair.lower()
        return pair
    else:
        return None

def help():
    title = "Assistance - AKA Help"
    intro = "You have asked for help, and you shall have it"
    embed = discord.Embed(title=title, description=intro, color=0x0000ff)

    exchanges = "Supported exchanges: `Binance`, `Bittrex`, `CryptoBridge`, `Cryptopia`, `Kucoin`, `Nanex`, `Poloniex`, `TradeSatoshi`, `YoBit`\n\n"
    embed.add_field(name="Supported Exchanges", value=exchanges)

    cmdCoin = "`.pair` - Returns market data for the specified coin.\t (ex:`.btc_ltc`)\n" \
              "\t- Fiat is now supported, `.gbp_ltc` will return Litecoin value in British Pound Sterling\n" \
              "\t- Additionally, you may request an exchange `.btc_ltc cryptopia`\n" \
              "\t- Note: if an exchange is not specified, see supported exchange list, for exchange\n" \
              "\t\tsearch priority\n"
    cmdHelp = "\t`?help` - Returns information about Tales-From-the-Cryptos.\n"
    cmdCmc = "\t`?cmc` - Returns the top 5 coins on CoinMarketCap\n\n"
    embed.add_field(name="Supported Commands", value=cmdCoin + cmdHelp + cmdCmc)

    github = "This project is a work in progress and was derived from Satoshi bot, found at https://github.com/cmsart/Satoshi`\n"
    thanks = "-Thanks for helping me open the door to PYTHON.-"
    embed.add_field(name="Project", value=github + thanks)

    return embed

#format error function
def formError(error):
    title = "Uh Oh"
    embed = discord.Embed(title=title, description='', color=0xff0000)
    embed.add_field(name="Error", value=error)
    embed.set_footer(text="Logging coming. ?help for more bot info")
    return embed

client.run(os.environ.get('BOT_TOKEN',None))
