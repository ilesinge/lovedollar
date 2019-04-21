# pylint: disable=no-member

import asyncio
import requests
import coinbase
import binance
from pythonosc import udp_client

osc = udp_client.SimpleUDPClient("127.0.0.1", 6010)

history = {}

def compare(transaction):
    symbol = transaction.base + transaction.quote
    if symbol not in history:
        history[symbol] = transaction.price
        transaction.set_change(0)
    else:
        old_price = history[symbol]
        history[symbol] = new_price = transaction.price
        change = (new_price - old_price) / old_price
        transaction.set_change(change)


async def transporter(transaction):
    if transaction:
        # print(transaction.__dict__)
        compare(transaction)
        transaction.display()
        sender(transaction)

def sender(transaction):
    # print('QTY', transaction.size)
    osc.send_message("ctrl", ["QTY", transaction.size])
    # print('PRICE', transaction.formatprice)
    osc.send_message("ctrl", ["PRICE", transaction.formatprice])
    # print('BIGCHANGE', transaction.bigchange)
    osc.send_message("ctrl", ["BIGCHANGE", transaction.bigchange])

async def binanceloop():
    await binance.subscribe(transporter)

async def coinbaseloop():
    await coinbase.subscribe(transporter)

asyncio.get_event_loop().run_until_complete(asyncio.gather(coinbaseloop(), binanceloop()))
