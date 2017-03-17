"""non-play helper functions
"""
import requests
from getpass import getpass
import logging
import os.path
import pickle
import time
import random
import tempfile


CRED_FILE = 'LOGIN'
SESSION_CACHE = os.join(tempfile.gettempdir(), 'login.pickle')


def login(username=None, password=None):
    """Return a logged in session."""
    s = requests.session()

    if os.path.isfile(SESSION_CACHE):
        logging.debug("session cache found")
        with open(SESSION_CACHE, 'rb') as cache:
            return pickle.load(cache)

    if not (username and password):
        if os.path.isfile(CRED_FILE):
            logging.debug("credentials found")
            with open(CRED_FILE, 'r') as credentials:
                # TODO: less silly
                login = credentials.readline()[:-1]
                username, password = login.split(' ')
        else:
            logging.debug("credentials not found")
            username = input('Username: ')
            password = getpass.getpass()

    logging.info("logging in")
    response = s.post('http://www.neopets.com/login.phtml',
                      data={'destination': "%2F",
                            'username': username,
                            'password': password},
                      headers=headers)

    # DEBUG
    #with open('/tmp/login.html', 'w') as fp:
    #    fp.write(response.content.decode('utf-8'))

    if response.status_code != 200:
        logging.error("login unsuccessful")
        return None

    with open(SESSION_CACHE, 'wb') as cache:
        pickle.dump(s, cache)
    logging.debug("session cached")

    return s


def normal(n=20):
    return sum(random.random() for _ in range(n))/n


def tick_delay():
    #time.sleep(0.0 + normal() * 0.1)
    pass
