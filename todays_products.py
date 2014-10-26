import json
import requests
import datetime
import pprintpp as pp
from time import sleep
import os

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
        self.product_url = requests.get(self.redirect_url).url

    def __unicode__(self):
        return "{} at {}".format(self.name, self.redirect_url)

    def __repr__(self):
        return "{} at {}".format(self.name, self.redirect_url)



def get_auth_token(base, config):
    auth = requests.post(base + '/oauth/token', data={
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'grant_type': config['grant_type']
    })
    return auth


def get_posts_for_today():
    base = 'https://api.producthunt.com/v1'
    this_dir = os.path.dirname(__file__)
    with open(os.path.join(this_dir, 'config.json')) as config:
        config = json.load(config)

    auth = get_auth_token(base, config)

    head = {'Authorization': 'Bearer ' + auth.json()['access_token']}

    posts_today = []
    today = requests.get(base + '/posts?days_ago=' + str(0), headers=head)
    today = today.json()
    for post_json in today["posts"]:
        posts_today.append(Post(post_json))
    return posts_today


def main():
    posts_today = get_posts_for_today()


if __name__ == "__main__":
    main()