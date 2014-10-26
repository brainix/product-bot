#-----------------------------------------------------------------------------#
#   Product Bot - A mashup of the Product Hunt and Twitter APIs.              #
#   reply.py                                                                  #
#                                                                             #
#   Copyright (c) 2014, Seventy Four, Inc.                                    #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU General Public License as published by      #
#   the Free Software Foundation, either version 3 of the License, or         #
#   (at your option) any later version.                                       #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU General Public License for more details.                              #
#                                                                             #
#   You should have received a copy of the GNU General Public License         #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#-----------------------------------------------------------------------------#



import datetime
import json
import urlparse

import tweepy

import bot



last_updated = datetime.datetime.now()
products = {}



class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        print('Incoming: {0}'.format(data))
        tweet = json.loads(data)
        screen_name = tweet['user']['screen_name']
        me = screen_name == bot.SCREEN_NAME
        retweet = 'retweeted_status' in tweet
        if not me and not retweet:
            product = get_product(data)
            if product is not None:
                reply = "@{0} Like {1}? Upvote it on #ProductHunt: {2}"
                reply = reply.format(screen_name, product['name'], product['producthunt_url'])
                log = u'Outgoing: {0}'.format(reply)
                print(log)
                if bot.ENV == 'production':
                    try:
                        bot.api.update_status(reply, tweet['id'])
                    except tweepy.TweepError:
                        pass
        delta = datetime.datetime.now() - last_updated
        return delta.seconds < 10 * 60



def get_products():
    keys = sorted(bot.redis.keys())
    try:
        keys.remove('client_token')
    except ValueError:
        pass
    key = keys[-1]

    tmp = bot.redis.hgetall(key)
    for key, value in tmp.items():
        key = urlparse.urlparse(key).netloc
        value = json.loads(value)
        products[key] = value
    return products

def get_product(data):
    for key in products.keys():
        if key in data:
            return products[key]

def main():
    listener = StreamListener()
    stream = tweepy.Stream(bot.auth, listener)
    while True:
        last_updated = datetime.datetime.now()
        products = get_products()
        stream.filter(track=products.keys())
        stream.disconnect()

if __name__ == '__main__':
    main()
