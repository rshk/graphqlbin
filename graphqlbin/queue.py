import json
import logging
import os
import time

import redis as Redis
from rx import Observable


logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
REDIS_CHAN = 'messages'

redis = Redis.from_url(REDIS_URL)
pubsub = redis.pubsub()
pubsub.subscribe(REDIS_CHAN)


def send_message(channel, text):
    redis.publish(REDIS_CHAN, json.dumps({'channel': channel, 'text': text}))


def watch_messages(channel):
    while True:
        msg = pubsub.get_message()
        if not msg:
            time.sleep(.001)
            continue

    # for msg in pubsub.listen():
        logger.debug('REDIS MSG: %s', msg)
        if msg['type'] == 'message':
            data = json.loads(msg['data'])
            if data['channel'] == channel:
                yield data


def get_watch_observable(channel):

    redis = Redis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    pubsub.subscribe(REDIS_CHAN)

    logger.debug('get_watch_observable: %s', channel)

    def get_stuff(obs):
        for msg in watch_messages(channel):
            logger.debug('Message: %s', msg)
            obs.on_next(msg)

        # while True:
        #     msg = pubsub.get_message()
        #     logger.debug('Message: %s', msg)
        #     if msg:
        #         obs.on_next(msg)
        #     obs.delay(1)

    return Observable.create(get_stuff)
