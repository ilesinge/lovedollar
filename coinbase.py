import requests
import json
import websockets
from transaction import Transaction

async def subscribe(transporter):
    
    r = requests.get("https://api.pro.coinbase.com/products")
    products = json.loads(r.content)
    product_ids = []
    for product in products:
        product_ids.append(product['id'])

    async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
        subscription = {
            'type': 'subscribe',
            'product_ids': product_ids,
            'channels': ['matches'] # ticker
        }
        await websocket.send(json.dumps(subscription))

        async for message in websocket:
            data = json.loads(message)
            transaction = formatter(data)
            await transporter(transaction)


def formatter(data):
    if data['type'] == 'match':
        """
        {
            "type":"match",
            "trade_id":46486450,
            "maker_order_id":"cb3e0c33-549f-4f14-88bf-5e2e650431da",
            "taker_order_id":"f84022de-2a73-4e43-925d-38806d1c7d07",
            "side":"buy",
            "size":"2.00000000",
            "price":"175.93000000",
            "product_id":"ETH-USD",
            "sequence":6549939050,
            "time":"2019-04-20T09:06:57.919000Z"
        }
        """
        product_id = data['product_id']
        product = product_id.split('-')
        base = product[0]
        quote = product[1]
        side = data['side'].upper()
        price = data['price']
        size = data['size']
        transaction = Transaction(base, quote, side, price, size, 'COINBASE')
        return transaction
    return None