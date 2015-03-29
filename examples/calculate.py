#!/usr/bin/env python

"""
calculates time-zone contribution for each trending topic
Ideally the data should be dumped in Mongo and queried out and
molded to a Twrapper object and calculation should be done.
But, currently the data trimmed and put into the db, so that
it becomes easy for this script.
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

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test_database
data = db.tests.find()
trend_contributions = dict() # dict for {trend1 : {loc1 : count, loc2 : count}, trend2 : {loc1 : count, loc2 : count}, ...}

trends = db.tests.distinct('trend')

for trend in trends:
    data = db.tests.find({'trend' : trend})
    trend_contributions[trend] = {} # new dict for each trend

    for d in data:
        if trend_contributions[trend].get(d['location']):
            trend_contributions[trend][d['location']] += 1
        else:
            trend_contributions[trend][d['location']] = 1

print("----------------Trends and time-zone wise contribution-------------")

for key in trend_contributions.keys():
    print("Trend: ",key)
    for loc, count in trend_contributions.get(key).items():
        print(loc, " : ", count)
    print("---------------------------------")
