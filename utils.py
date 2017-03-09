"""non-play helper functions
"""
import requests
from getpass import getpass
import logging
import os.path
import pickle
import time
import random


# TODO: go for something more generic
DEFAULT_HEADER = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130626 Firefox/17.0 Iceweasel/17.0.7',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'www.neopets.com',
    'Referer': 'http://www.neopets.com/login/index.phtml'
}
#ALT_HEADER = {
#        'Host': 'www.neopets.com',
#        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#        'Accept-Language': 'en-US,en;q=0.5',
#        'DNT': '1',
#        'Connection': 'keep-alive' ,
#        'Upgrade-Insecure-Requests': '1'}
CRED_FILE = 'LOGIN'
SESSION_CACHE = '/tmp/login.pickle'


def login(username=None, password=None, headers=DEFAULT_HEADER):
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

    # paranoid mode
    #s.get('http://www.neopets.com', headers=headers)
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
    time.sleep(0.1 + normal() * 0.7)
