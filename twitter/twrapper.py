#!/usr/bin/env python

"""
It is the main module, which serves as the wrapper for the APIs.
It offers a Twrapper class which provides methods to talk to differnt APIs
and fetch data. Other classes are Tweet and Trend.
"""

# Copyright (C) 2015  Abhishek Bhattacharjee <abhishek.bhattacharjee11@gmail.com>
# Copyright (C) 2015  G Nithin

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

################################################################################

import base64
import json
import pprint

try: # if python 2.x
    from urllib import urlencode
    from req import https_req
    import twitter_constants as t_const
except ImportError: # Python 3.x
    import urllib
    from urllib.parse import urlencode
    from .req import https_req
    from . import twitter_constants as t_const


######################################## UTILS ########################################

def log(s):
    """
    Used to print to screen.
    Can be controlled to be turned off or modified later on.
    """
    print(s)

##################################### END UTILS ########################################

class Twrapper:
    def __init__(self, key, secret):
        self.__key = key
        self.__secret = secret
        self.__https_obj = https_req(t_const.DOMAIN_NAME)
        token = self.__authenticate()
        #raise Invalid creds exception here.
        if token == None:
            raise Exception("Cannot authenticate key and secret!")
        else:
            self.__token = token

    def __authenticate(self):
        '''
        Used to auntheticate. Consumer key and secret are
        pre-defined. Returns the header if succesful else
        exits.
        '''
        #Acquiring the access token
        request_method = "POST"
        uri = t_const.URI_ACCESS_TOKEN
        param = urlencode({'grant_type':'client_credentials'})

        CONSUMER_KEY = self.__key
        CONSUMER_SECRET = self.__secret
        to_encode = CONSUMER_KEY + ":" + CONSUMER_SECRET

        try: # 2.x
            enc_str = base64.b64encode(to_encode)
        except TypeError: # 3.x
            enc_bytes = base64.b64encode(bytes(to_encode, 'UTF-8'))
            enc_str = enc_bytes.decode('UTF-8')

        headers = {
            'Authorization' : 'Basic ' + enc_str,
            'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        payload = self.__https_obj.make_req(uri, request_method, param, headers)
        if payload == None:
            log("Authentication Failed.")
            return None

        #Response type is always json
        #ref - https://dev.twitter.com/oauth/reference/post/oauth2/token
        try:
            dic = json.loads(payload.decode('UTF-8'))
        except ValueError:
            log("Authentication response Invalid.")
            return None
        if "errors" in dic or "access_token" not in dic:
            log("Error in authentication")
            return None

        access_token = dic.get("access_token")
        get_headers={"Authorization":"Bearer "+access_token}
        return get_headers

    def __get_tweets_from_json(self, json_data):
        """
        Takes a list
        and returns a list of tweet objects
        """
        list_of_tweets = json.loads(json_data.decode('UTF-8'))
        return [Tweet(t) for t in list_of_tweets]

    def get_user_timeline_tweets(self, screen_name, tweet_count):
        api_url = t_const.API_GET_TWEETS + "?screen_name=%s&count=%s"
        json_tweets = self.__https_obj.make_req(api_url % (screen_name, tweet_count),"GET", "", self.__token)
        if json_tweets == None:
            log("Error in receiving data")
            return None
        tweets = self.__get_tweets_from_json(json_tweets)
        return tweets

    def get_trends(self, geo_location):
        """
        Returns trend objects. Expects the geological area
        for which the trends are to be fetched
        """
        api_url = t_const.API_TREND + "?id=%s"
        json_str = self.__https_obj.make_req(api_url % (geo_location), "GET", "", self.__token)
        res_data = json.loads(json_str.decode('UTF-8'))

        trends = res_data[0]['trends']
        # return a list of trend objects
        return [Trend(t) for t in trends]

    def get_trends_tweets(self, trend_obj , counts):
        api_url = t_const.API_TREND_TWEETS + "?q=%s&count=%s"
        data_received = self.__https_obj.make_req(api_url % (trend_obj._get_query(), counts), "GET",
                                        "", self.__token)
        res_data = json.loads(data_received.decode('UTF-8'))
        statuses = res_data['statuses']
        # Returns tweet objects
        return [Tweet(status) for status in statuses]

    def __del__(self):
        #Closing the connection.
        self.__https_obj.close_conn()

class Trend():
    """
    Small class for trend.
    Use to fetch tweets for the trend
    """
    def __init__(self, json_data):
        """
        Initialize object with a trend
        """
        self._trend = json_data

    def _get_name(self):
        """
        Get name if the trend.
        """
        return self._trend['name']

    def _get_query(self):
        """
        Returns the URL Encoded name. Use for
        querying in ither api
        """
        return self._trend['query']

# add all the attributes as properties
# will make it more efficient
# shouldn't calculate if things have
# been calculated once
class Tweet():
    """
    Class representing a Tweet.
    """
    def __init__(self, json_data):
        """
        Initialize the object with the tweet data(json)
        """
        self._tweet = json_data

    def _get_user(self):
        """
        Returns a dict with user details.
        Eg followers, location, screen_name etc
        """
        return self._tweet['user']

    def _get_screen_name(self):
        """
        Method to give the screen name for the tweet
        """
        user = self._get_user()
        return user['screen_name']

    def _get_location(self):
        """
        Returns location of the user
        """
        return self._get_user()['location']

    def _get_retweets(self):
        """
        Gives the count of retweets
        """
        return int(self._tweet['retweet_count'])

    def _get_tweet(self):
        """
        Gives the tweet. Could be a link or text
        """
        return self._tweet['text']

    def _get_urls(self):
        """
        Returns usable URLs (list o f URLs).
        The URLS can be directly used by urllib etc
        """
        usable_urls = list()
        urls = self._tweet['entities']['urls']

        for url in urls:
            usable_url = url['expanded_url']
            usable_url = usable_url.replace(" ","") # trimming
            usable_urls.append(usable_url)

        return usable_urls

    def _get_time_zone(self):
        """
        Gives the time zone of the tweet
        """
        return self._get_user()['time_zone']

    def _get_json_data(self):
        """
        Gives back the real JSON data
        """
        return self._tweet

    def __str__(self):
        """
        Print the properties(not yet props)
        """
        print_li = [
            "Screen Name: " + self._get_screen_name(),
            "Tweet: " + self._get_tweet(),
            "Retweets: " + str(self._get_retweets()),
            "URLs: " + ", ".join(self._get_urls())
            ]

        try: #python 2
            print_s = '\n'.join(print_li).encode('utf-8').strip()
            return print_s + '\n' + '-'*34
        except:
            print_s = '\n'.join(print_li)
            return print_s + '\n' + '-'*34
