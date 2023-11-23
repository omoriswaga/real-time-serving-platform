from MessageProducer import MessageProducer

import time
import random
import randomname

RANDOMNAME_CATEGORY = 'n/food'
RANDOM_WAIT_RANGE_SECONDS = (1, 3)

class Feed:
    def __init__(self, producer: MessageProducer):
        self._producer = producer

    def start(self):
        while True:
            self._send_message()
            self._random_wait()

    def _send_message(self):
        msg = {
            'food': self._get_random_food()
        }

        print(f'Sending random message {msg}...')
 
        self._producer.send(msg)

    def _random_wait(self):
        wait_seconds = random.randrange(*RANDOM_WAIT_RANGE_SECONDS)
        print(f'Waiting {wait_seconds} seconds...')
        time.sleep(wait_seconds)

    def _get_random_food(self):
        return randomname.generate(RANDOMNAME_CATEGORY)