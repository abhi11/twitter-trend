# Twitter API wrapper

## Uses the REST API(Version 1.1)

## List of APIs Currently Covered:

* API to fetch from a User Timeline (statuses/user_timeline)
* API to fetch current Trends (trends/place)
* API to search tweets for a trend.
* More will be added

## Things you don't have to worry about

* HTTPS Connnection
* Correct API URLs
* Authentication mechanism(Although, one needs to have an app registered with Twitter)

## Usage

* Clone the repo first and create a constants.py under twitter directory.
* Add the following in the above created file
```
CONSUMER_KEY = your consumer key
CONSUMER_SECRET = your consumer secret
```
* CONSUMER_KEY and CONSUMER_SECRET could be acquired by registering an app with Twitter [Here](https://apps.twitter.com/). Login and create a new app ;-)
* Look at [test.py](https://github.com/abhi11/twitter-trend/blob/master/test.py) to understand how to use the module.


## And Example to show the usability.

### Time Zone Wise Contribution to trends

* Takes 100 tweets for every trending topic and pushes it into a database(trend_insert.py).[Yet to be ported]
* Prints Time-Zone wise contribution for each trending topic(calculate.py).[Yet to be ported]
* Uses [MongoDB](http://www.mongodb.org/ "MongoDB") and moongodb client for python

## TODO
* Adding more wrapper for different use-cases.
* Adding wrappers to fetch stale data from db.
* Making a python module out of this.
