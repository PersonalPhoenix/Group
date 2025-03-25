import json
import logging
import redis

from backend.config import settings
from backend.users.domain.events import Event


logger = logging.getLogger(__name__)

r = redis.Redis(settings.get_redis_host_and_port)


def publish(channel, event: Event):
    logging.info(f"publishing: channel={channel}, event={channel}")
    r.publish(channel, json.dumps(event))


def start_redis():
    logger.info('Redis pubsub starting')
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    # pubsub.subscribe(settings.get_redis_channel())

    for n in pubsub.listen():
       ...


if __name__ == '__main__':
    start_redis()
