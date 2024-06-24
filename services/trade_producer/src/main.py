from quixstreams import Application
from time import sleep
from kraken_api import KrakenWebSocketAPI
from loguru import logger


def produce_trades(
        kafka_broker_address:str,
        kafka_topic_name:str
) -> None:
    """
    Pulls data from the kraken web socket API and then saves it as a topic.

    Args:
        kafka_broker_address: str ---> the address of the apache kafka broker
        kafka_topic_name: str ---> the name of the kafka topic the data will be stored in

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_address)

    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    kraken_api = KrakenWebSocketAPI(product_id="BTC/USD")

    with app.get_producer() as producer:

        while True:

            trades = kraken_api.get_trades()
            logger.info("Got trades!")

            for trade in trades:

                message = topic.serialize(key=trade['product_id'], value=trade)

                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    key=message.key
                )

                logger.info(f"Sent data: {trade}")

                sleep(1)


if __name__ == '__main__':

    produce_trades(
        kafka_broker_address='redpanda-0:9092',
        kafka_topic_name='trade'
    )

