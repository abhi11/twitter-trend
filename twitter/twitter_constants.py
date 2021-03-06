#!/usr/bin/env python

"""
This file consists of only those fields that are specific to
the Twitter API.
This is to allow ease of configuration and changes if any later on.
"""
DOMAIN_NAME = "api.twitter.com"
URI_ACCESS_TOKEN = "/oauth2/token/"
API_GET_TWEETS = "/1.1/statuses/user_timeline.json"
API_TREND = "/1.1/trends/place.json"
API_TREND_TWEETS = "/1.1/search/tweets.json"
