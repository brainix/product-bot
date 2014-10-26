import json
import datetime

import requests
import os
from bot import redis


__author__ = 'rogueleaderr'


class Post(object):
    """
    Class containing the metadata of a product post to ProductHunt
    """

    def __init__(self, post_json):
        self.comments_count = post_json["comments_count"]
        self.created_at = post_json["created_at"]
        self.day = post_json["day"]
        self.discussion_url = post_json["discussion_url"]
        self.id = post_json["id"]
        self.maker_inside = post_json["maker_inside"]
        self.name = post_json["name"]
        self.redirect_url = post_json["redirect_url"]
        self.tagline = post_json["tagline"]
        self.user = post_json["user"]
        self.votes_count = post_json["votes_count"]
        self.screenshot_url = post_json['screenshot_url']["850px"]
        try:
            self.product_url = requests.get(self.redirect_url, timeout=2).url
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            self.product_url = None

    def __unicode__(self):
        return "{} at {}".format(self.name, self.redirect_url)

    def __repr__(self):
        return "{} at {}".format(self.name, self.redirect_url)


def get_auth_token(base_uri):
    """
    Fetch the client auth token from Redis or get a new one
    :param base_uri:
    :return:
    """

    auth = redis.get("client_token")
    if not auth:
        auth = requests.post(base_uri + '/oauth/token', data={
            'client_id': os.environ['PRODUCT_HUNT_CLIENT_ID'],
            'client_secret': os.environ['PRODUCT_HUNT_CLIENT_SECRET'],
            'grant_type': os.environ['PRODUCT_HUNT_GRANT_TYPE']
        })
        redis.setex("client_token", auth, 100)
    return auth


def get_posts_for_today():
    """
    Hit the product hunt API and create a list of Post objects corresponding to the posts from today.

    :return:
    """
    base_uri = 'https://api.producthunt.com/v1'
    auth = get_auth_token(base_uri)
    head = {'Authorization': 'Bearer ' + auth.json()['access_token']}
    url = '{}/posts?days_ago=0'.format(base_uri)

    posts_today = []
    response = requests.get(url, headers=head)
    response = response.json()
    for post_json in response["posts"]:
        posts_today.append(Post(post_json))

    return posts_today


def main():
    posts_today = get_posts_for_today()
    date = str(datetime.date.today())
    for post in posts_today:
        if post.product_url:  # sometimes the redirect dereference times out
            post_info = json.dumps({"name": post.name,
                                    "producthunt_url": post.discussion_url,
                                    "screenshot_url": post.screenshot_url
            })
            redis.hset(date, post.product_url, post_info)


if __name__ == "__main__":
    main()