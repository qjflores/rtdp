"""Main program for polling an api and publishing the content to kafka."""

from rtdp.publisher.poller import Poller
from rtdp import config

if __name__ == '__main__':
    poller = Poller(config.API_URL)
    poller.poll()
