#!/usr/bin/env python
import base64
import json
import pprint
import constants

#Imports that will fail in 3+
try:
    import httplib
except ImportError:
    import http.client as httplib

import urllib

### UTILS ###


def json_str_to_json(json_str):
    """
    Takes a JSON string and converts it to
    JSON obj(list dict etc)
    """
    return json.loads(json_str)

def get_tweets_from_json(json_data):
    """
    Takes a list
    and returns a list of tweet objects
    """
    tweets = list()
    list_of_tweets = json_str_to_json(json_data)

    return [Tweet(t) for t in list_of_tweets]


class https_req:
    def __init__(self, domain):
        """
        TODO:
        Need to make this work for Python 3+
        """
        try:
            self._conn = httplib.HTTPSConnection(domain)
        except:
            self._conn = None

    def _get_conn(self):
        """
        Returns connection object.
        """
        return self._conn

    def _make_req(self, uri, request_method, params, headers):
        """
        Performs request and returns payload.
        Returns None if unsuccessful.
        Note: This does not close the connection upon exit.
        TODO:
        Need to make this work for Python 3+
        """
        try:
            self._conn.request(request_method, uri, params, headers)
            response=self._conn.getresponse()
        except:
            print "Error while performing https request."
            return None
        else:
            payload = response.read()
            return payload

    def _close_conn(self):
        """
        Closes connection.
        """
        if self._conn != None:
            self._conn.close()

def make_https_req(domain, uri, request_method, params, headers):
    """
    Performs https requests on the given params.
    Returns payload if success, None if request failed.
    """

    conn = get_https_conn(domain)
    if conn == None:
        return None
    payload = make_https_req(conn, uri, request_method, params, headers)
    conn.close()
    return payload


def authenticate():
    '''
    Used to auntheticate. Consumer key and secret are
    pre-defined. Returns the header if succesful else
    exits.
    '''
    #Acquiring the access token
    domain_name = "api.twitter.com"
    request_method = "POST"
    uri = "/oauth2/token/"
    param = urllib.urlencode({'grant_type':'client_credentials'})

    CONSUMER_KEY=constants.CONSUMER_KEY
    CONSUMER_SECRET=constants.CONSUMER_SECRET
    enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)
    headers = {"Authorization":"Basic "+enc_str,
               "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}

    https_obj = https_req(domain_name)
    payload = https_obj._make_req(uri, request_method, param, headers)

    if payload == None:
        print "Authentication Failed."
        return None

    ## Converting the payload string to a dictionary

    dic = json_str_to_json(payload)

    try:
        dic = json.loads(payload)
    except ValueError:
        print "Authentication response Invalid."
        return None

    access_token = dic.get("access_token")
    get_headers={"Authorization":"Bearer "+access_token}
    return get_headers

def get_trends(authentication_token, geo_location):
    """
    Returns trend objects. Expects the geological area
    for which the trends are to be fetched
    """
    conn = httplib.HTTPSConnection("api.twitter.com")
    api_url = "/1.1/trends/place.json?id=%s"
    request = conn.request("GET", api_url % (geo_location),
                                 "", authentication_token)

    response = conn.getresponse()
    data_received = response.read()
    conn.close()

    json_data = json_str_to_json(data_received)
    trends = json_data[0]['trends']

    # return a list of trend objects
    return [Trend(t) for t in trends]


##################################### END UTILS ########################################


class UserTimeline():
    """
    A class which is used as a user timeline.
    """

    def __init__(self, screename, conn=None):
        """
        Expects the screen_name for which, the tweets will
        be fetched.
        """
        self._screename = screename
        self._conn = conn

    def _set_conn(self):
        """
        Sets the HTTP Connection with twitter api end point.
        Close the connection, when usage is done
        """
        self._conn = https_req("api.twitter.com")
        return self._conn

    def _close_conn(self):
        if self._conn:
            self._conn.close()

    def _fetch_tweets(self, authentication_token, counts):
        """
        Fetches <count> no. of tweets.
        Loads it into json and returns the json object.
        """
        try:
            api_url = "/1.1/statuses/user_timeline.json?screen_name=%s&count=%s"
            request = self._conn.request("GET", api_url % (self._screename, counts),
                                         "", authentication_token)

            response = self._conn.getresponse()
            data_received = response.read()

            # Returns tweet objects
            return get_tweets_from_json(data_received)

        except:
            return None


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

    def _set_conn(self):
        """
        Sets the HTTP Connection with twitter api end point.
        Close the connection, when usage is done
        """
        self._conn = httplib.HTTPSConnection("api.twitter.com")
        return self._conn

    def _close_conn(self):
        if self._conn:
            self._conn.close()

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

    def _fetch_tweets(self, authentication_token, counts):
        """
        Fetches tweets for the trend.
        Expects the geographical area for which the trends
        are to be fetched. For eg 1 is for world.
        """
        api_url = "/1.1/search/tweets.json?q=%s&count=%s"
        request = self._conn.request("GET", api_url % (self._get_query(), counts),
                                     "", authentication_token)

        response = self._conn.getresponse()
        data_received = response.read()

        json_data = json_str_to_json(data_received)
        statuses = json_data['statuses']

        # Returns tweet objects
        return [Tweet(status) for status in statuses]


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

    def _print_details(self):
        """
        Print the properties(not yet props)
        """
        print "Screen Name: " + self._get_screen_name()
        print "Tweet: " + self._get_tweet()
        print "Retweets: " + str(self._get_retweets())
        print "URLs: " + ", ".join(self._get_urls())
