from typing import List, Dict
from websocket import create_connection
import json


class KrakenWebSocketAPI:

    URL = "wss://ws.kraken.com/v2"

    def __init__(
            self,
            product_id:str,
    ):
        self.product_id = product_id
        self.subscribe(product_id)
   

    def subscribe(self, product_id):
        """
        Subscribes to the Kraken websocket api to retrieve live trades.
        """
        self._ws = create_connection(self.URL)

        print("Connection established...")

        print(f"Subscribing to {product_id} trades...")

        msg = {
                "method": "subscribe",
                "params": {
                    "channel": "trade",
                    "symbol": [
                        product_id
                    ],
                    "snapshot": False
                }
            }
        
        self._ws.send(json.dumps(msg))

        print("Subscription successful.")

        # Discarding first two messages because they contain no trade data
        _ = self._ws.recv()
        _ = self._ws.recv()
        

    def get_trades(self) -> List[Dict]:
        message = self._ws.recv()

        # return an empty list of response is a heartbeat
        if 'heartbeat' in message:
            return []

        # convert string to dict
        message = json.loads(message)


        # extract trades from message
        trades = []

        for trade in message['data']:
            trades.append({
                'product_id':self.product_id,
                'price': trade['price'],
                'volume': trade['qty'],
                'timestamp': trade['timestamp']
            })
        
        return trades