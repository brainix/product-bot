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

import tweepy

import bot



last_updated = datetime.datetime.now()



class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        print('Incoming: {0}'.format(data))
        delta = datetime.datetime.now() - last_updated
        return delta.seconds < 60 * 60



def main():
    listener = StreamListener()
    stream = tweepy.Stream(bot.auth, listener)
    while True:
        # TODO: Replace bot.PHRASES with product URLs below.
        stream.filter(track=bot.PHRASES)
        last_updated = datetime.datetime.now()
        stream.disconnect()

if __name__ == '__main__':
    main()
