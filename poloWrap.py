#polo wrapper

import requests
import discord
import coindeskWrap
import CoinMarketCap

# Returns the coin name for the given symbol
def getReadableCoinName(coin):
    names = {"BCN": "Bytecoin", "BELA": "Belacoin", "BLK": "BlackCoin", "BTCD": "BitcoinDark", "BTM": "Bitmark", "BTS": "BitShares",
    "BURST": "Burst", "GNT": "Golem", "CLAM": "CLAMS", "DASH": "Dash", "DGB": "DigiByte", "DOGE": "Dogecoin", "EMC2": "Einsteinium",
    "FLDC": "FoldingCoin", "FLO": "Florincoin", "GAME": "GameCredits", "GRC": "Gridcoin Research", "HUC": "Huntercoin",
    "LTC": "Litecoin", "MAID": "MaidSafeCoin", "OMNI": "Omni", "NAUT": "Nautiluscoin", "NAV": "NAVCoin", "NEOS": "Neoscoin",
    "NMC": "Namecoin", "NOTE": "DNotes", "NXT": "NXT", "PINK": "Pinkcoin", "POT": "PotCoin", "PPC": "Peercoin", "RIC": "Riecoin",
    "SJCX": "Storjcoin X", "STR": "Stellar", "SYS": "Syscoin", "VIA": "Viacoin", "XVC": "Vcash", "VRC": "VeriCoin", "VTC": "Vertcoin",
    "XBC": "BitcoinPlus", "XCP": "Counterparty", "XEM": "NEM", "XMR": "Monero", "XPM": "Primecion", "XRP": "Ripple", "GNO": "Gnosis",
    "ETH": "Ethereum", "SC": "Siacoin", "BCY": "BitCrystals", "EXP": "Expanse", "FCT": "Factom", "RADS": "Radium", "AMP": "Synereo AMP",
    "DCR": "Decred", "LSK": "Lisk", "LBC": "LBRY Credits", "STEEM": "STEEM", "SBD": "Steem Dollars", "ETC": "Ethereum Classic",
    "REP": "Augur", "ARDR": "Ardor", "ZEC": "Zcash", "STRAT": "Stratis", "NXC": "Nexium", "PASC": "PascalCoin", "ZRX": "0x", "CVC": "Civic",
    "BCH": "Bitcoin Cash", "OMG": "OmiseGO", "GAS": "Gas", "STORJ": "Storj", "BTC": "Bitcoin"}

    return names[coin]

# Returns ticker data from Poloniex for the given currency pair
def getTickerData(pair):
    url = "https://poloniex.com/public?command=returnTicker"
    ticker = requests.get(url)
    if ticker.status_code == 200:
        ticker = ticker.json()
        if pair in ticker:
            return ticker[pair]

    return None

# Returns formatted market data for the bot to send
def getTickerMessage(ticker, pair, fiat):
    coin = getReadableCoinName(pair.split("_")[1])


    price = "Current Price: `" + ticker["last"]
    if fiat:
        fiatConv = coindeskWrap.getTickerData(fiat)
        fin = float(ticker["last"]) * float(fiatConv["rate_float"])
        fiatDisplay = " / {:.2f}".format(fin) + " " + fiat + "`\n"
    else:
        btc = coindeskWrap.getTickerData("USD")
        fin = float(ticker["last"]) * btc["rate_float"]
        fiatDisplay = " / {:.2f}".format(fin) + " USD`\n"

    final = price + fiatDisplay
    header = coin + " (" + pair.split("_")[1] + ")"

    changeNum = round((float(ticker["percentChange"]) * 100), 2)
    sign = "+" if changeNum > 0 else ""
    change = "24hr Percent Change: ```diff\n" + sign + str(changeNum) + "%```"

    data = final + change

    if changeNum < 0:
        col = 0xFF0000
    elif changeNum > 0:
        col = 0x00ff00

    embed = discord.Embed(title = header, description = data, color = col)
    embed.set_footer(text = "via Poloniex | ?help for more bot info")

    return embed
