import urllib.request, urllib.parse, urllib.error
import twurl
import ssl
import json


# downloaded from https://www.py4e.com/code3/


def fr_list(name, counter: int):
    """
    Returns a JSON file of user's friends list by receiving a username
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    acct = name
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': counter})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    return json.loads(data)
