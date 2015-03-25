#!/usr/bin/env python

"""
Takes 100 tweets and puts it in the database
"""

# Copyright (C) 2015  Abhishek Bhattacharjee <abhishek.bhattacharjee11@gmail.com>

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

from pymongo import MongoClient
from twitter import twrapper, constants

def put_into_database(trendname,screename,text,loc=None):
    try:
        client = MongoClient('localhost', 27017)
        db = client.test_database
        screen_name = db.tests.find_one({"trend":trendname,"screename":screename,"text":text})
        if not(screen_name):
            if loc:
                db.tests.insert({"trend":trendname,"screename":screename,"text":text,"location":loc})
            else:
                db.tests.insert({"trend":trendname,"screename":screename,"text":text,"location":"Others"})
            print("Gone into the database")

        else:
            print("Already present")
    except:
        print("database error")


def get_info_for_trends(trend, count=None):
    """
    get tweets for a trend and put them to the db
    """
    tw_obj = twrapper(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

    tweeets = tw_obj.get_trends_tweets(trend, 100)

    for t in tweets:
        location = t._get_location()
        time_zone = t._get_time_zone()
        if location:
            put_into_database(trend._get_name(), t._get_screen_name(),
                              t._get_tweet(), location)
        elif time_zone:
            put_into_database(trend._get_name(), t._get_screen_name(),
                              t._get_tweet(), time_zone)
        else:
            put_into_database(trend._get_name(), t._get_screen_name(),
                              t._get_tweet())

def main():
    """
    Creates a twrapper object
    """
    t_object = twrapper(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
    trends = t_object.get_trends(1)

    for trend in trends:
