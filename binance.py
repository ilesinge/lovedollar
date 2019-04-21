import requests
import json
import websockets
from transaction import Transaction

async def subscribe(transporter):
    
    r = requests.get("https://api.binance.com/api/v3/ticker/price")
    symbols = json.loads(r.content)
    symbol_ids = []
    for symbol in symbols:
        symbol_ids.append(symbol['symbol'])

    async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
        streams = []
        for symbol in symbol_ids:
            streams.append(symbol.lower()+'@trade')
        streamstring = "/".join(streams)
        async with websockets.connect('wss://stream.binance.com:9443/stream?streams='+streamstring) as websocket:
            async for message in websocket:
                data = json.loads(message)
                transaction = formatter(data)
                await transporter(transaction)

def formatter(data):
    """
    {
        "e": "trade",     // Event type
        "E": 123456789,   // Event time
        "s": "BNBBTC",    // Symbol
        "t": 12345,       // Trade ID
        "p": "0.001",     // Price
        "q": "100",       // Quantity
        "b": 88,          // Buyer order ID
        "a": 50,          // Seller order ID
        "T": 123456785,   // Trade time
        "m": true,        // Is the buyer the market maker?
        "M": true         // Ignore
    }
    """
    data = data['data']
    if data['e'] == 'trade':
        symbol = data['s']
        base = symbol[0:3]
        quote = symbol[3:6]
        side = 'BUY' if data['m'] else 'SELL'
        price = data['p']
        size = data['q']
        transaction = Transaction(base, quote, side, price, size, 'BINANCE')
        return transaction
    return None