import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import poloWrap
import bitWrap
import binWrap
import yobitWrap
import kucoinWrap
import krakenWrap
import nanexWrap
import re
import requests
import sys
import json
from os.path import expanduser

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

@client.event
async def on_ready():
    print("BOT IS RUNNING!")
    #
    # ticker = requests.get(url)
    # ticker.json()
    # #jsonToPython = json.loads(jsonData
    # print(ticker)
    # ticker = ticker[0]
    # print(ticker)
    # high = ticker['last']
    # print(high)
    #
    # start logging /primarily for adding new coins or exchanges
    #   from requests !add

@client.event
async def on_message(message):
    msg = message.content.lower()
    split = msg.split(' ')
    if msg == 'gfy':
        await client.send_message(message.channel, "Yup, GFY")

    #read messages
    if msg.startswith('^'):
        #this is what we want, so split it.  Don't do anything otherwise.
        sp = split[0:]
        await client.send_message(message.channel, "first = "+sp[0]+" second = "+sp[1])
        pair = sp[0]
        pair = pair[1:5]
        curr = sp[1]

        if pair == "pair":
            await client.send_message(message.channel, "Your chosen pair is " + curr)
            pair = curr.upper()
            try:
                exch = sp[2]
                await client.send_message(message.channel, "Your preferred exchange is " + exch)
            except:
                exch = 'bittrex'
                await client.send_message(message.channel, "No exchange chosen, default is bittrex.")

            pairMsg = coinData(pair, exch)
            await client.send_message(message.channel, embed=pairMsg)
            #error = formError("Wrong format")
        else:
            await client.send_message(message.channel, "Unsuccessful: " + pair + " is not pair")
            await client.send_message(message.channel, "Checking command...")
    elif msg.startswith('!'):
        sp = split[0:]
        coin = sp[0]
        coin = coin[1:].upper()
        await client.send_message(message.channel, "Going to search for " + coin)
        coinMsg = findCoin(coin)
        await client.send_message(message.channel, coinMsg)
    elif msg.startswith('+'):
        sp = split[0:]
        hp = sp[0]
        hp = hp[1:].lower()
        if hp == "help":
            helpMsg = help()
            await client.send_message(message.author, embed=helpMsg)
    #if message isn't right format
        #provide error
    #if message is correct format
        #break up the message and send to correct function

#function for getting the right exchange "get" info
def coinData(pair, exch):
    #FORMAT Exchange and Pair for conditional statements
    exch = exch.lower()
    pair = pair.replace("-", "_")
    pairsplit = pair.split("_")
    samp = pairsplit[0]

    print ("sample is: " + samp)

    if samp == 'BTC':
        if exch == 'poloniex':
            pairFmt = formPair(exch, pair)
            ticker = poloWrap.getTickerData(pairFmt)
            if ticker:
                coinMsg = poloWrap.getTickerMessage(ticker, pairFmt)
                return coinMsg
        elif exch == 'bittrex':
            pairFmt = formPair(exch, pair)
            ticker = bitWrap.getTickerData(pairFmt)
            if ticker:
                coinMsg = bitWrap.getTickerMessage(ticker, pairFmt)
                return coinMsg
        elif exch == 'binance':
            pairFmt = formPair(exch, pair)
            ticker = binWrap.getTickerData(pairFmt)
            if ticker:
                coinMsg = binWrap.getTickerMessage(ticker, pairFmt)
                return coinMsg
        elif exch == "nanex":
            pairFmt = formPair(exch, pair)
            ticker = nanexWrap.getTickerData(pairFmt)
            if ticker:
                coinMsg = nanexWrap.getTickerMessage(ticker, pairFmt)
                return coinMsg
        elif exch != 'poloniex' or exch != 'bittrex' or exch!= 'binance' or exch != "nanex":
            pairFmt = formPair("bittrex", pair)
            ticker = bitWrap.getTickerData(pairFmt)
            if ticker:
                coinMsg = bitWrap.getTickerMessage(ticker, pairFmt)
                return coinMsg
    elif exch == 'yobit':
        pairFmt = formPair(exch, pair)
        ticker = yobitWrap.getTickerData(pairFmt)
        if ticker:
            coinMsg = yobitWrap.getTickerMessage(ticker, pairFmt)
            return coinMsg
        else:
            return formError("No return from server")
    elif exch == 'kucoin':
        pairFmt = formPair(exch, pair)
        ticker = kucoinWrap.getTickerData(pairFmt)
        if ticker:
            coinMsg = kucoinWrap.getTickerMessage(ticker, pairFmt)
            return coinMsg
        else:
            return formError("No return from server")
    elif exch == 'kraken':
        pairFmt = formPair(exch, pair)
        ticker = krakenWrap.getTickerData(pairFmt)
        if ticker:
            coinMsg = krakenWrap.getTickerMessage(ticker, pairFmt)
            return coinMsg
        else:
            return formError("No return from server")
    elif exch == 'nanex':
        pairFmt = formPair(exch, pair)
        ticker = nanexWrap.getTickerData(pairFmt)
        if ticker:
            coinMsg = nanexWrap.getTickerMessage(ticker, pairFmt)
            return coinMsg
        else:
            return formError("No return from server")
    else:
        return formError("Currency not found")

#USERS WILL INPUT BTC_LTC as a format.  Don't restrict the user.
# This function formats the pair for the given exchange and returns it to be used in the ticker.
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
    elif exch == "poloniex": # ex BTC_LTC
        # THIS IS HOW USERS WILL INPUT...do nothing / except ensure uppercase
        pair = pair.upper()
        return pair
    elif exch == "yobit": # ex ltc_btc
        pair = pair.replace("-", "_")
        pairsplit = pair.split("_")
        pair = pairsplit[1] + "_" + pairsplit[0]
        pair = pair.lower()
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
    elif exch == "kraken": # ex BCHUSD
        pair = pair.replace("-", "_")
        pairsplit = pair.split("_")
        pair = pairsplit[0] + pairsplit[1]
        return pair
    else:
        return None


def findCoin(coin):
    pair = "BTC_" + coin

    # if no exchange chosen, bittrex is default
    ticker = bitWrap.getTickerData(pair)
    if ticker:
        return bitWrap.getTickerMessage(ticker, pair)
    else:
        return formError(coin + " is NOT a correct pair")

def help():
    title = "Assistance AKA Help"
    intro = "You have asked for help, and you shall have it"
    embed = discord.Embed(title=title, description=intro, color=0x0000ff)

    exchanges = "The exchanges currently supported are: `Bittrex`, `Poloniex`, `Binance`, `YObit`, `Kucoin`\n\n"
    embed.add_field(name="Supported Exchanges", value=exchanges)

    cmdCoin = "`^pair <currency pair> <exchange>` - Returns market data for the specified coin/exchange.\n\n\t- Example: `^pair BTC_LTC Poloniex`\n\n"
    #cmdBitcoin = "`^BTC <currency>` - Returns current bitcoin price for the specified currency.\n\n\t- Example: `^bitcoin GBP`\n\n"
    cmdHelp = "`+help` - Returns information about CryptoDabloons.\n\n"
    embed.add_field(name="Commands", value=cmdCoin + cmdHelp)

    lookup = """For simple currency information, !coin will return data on the single coin."""
    embed.add_field(name="Single Currency Lookup", value=lookup)

    github = "This project is a work in progress and was derived from Satoshi bot, found at https://github.com/cmsart/Satoshi`\n"
    thanks = "-Thanks for helping me open the door to PYTHON.-"
    embed.add_field(name="Project", value=github + thanks)

    return embed


#format error function
def formError(error):
    embed = discord.Embed(title="ERROR", description=error, color=0xFF0000)
    embed.set_footer(text="Ask for help numbnuts (+help)")
    footer = "Ask for help numbnuts"
    nextTry = "```prolog\nERROR: " + error + "\n" + footer + "\n```"
    return nextTry


client.run("TOKEN")