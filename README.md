# A twitter api wrapper to fetch tweet for a given twitter handle(For a public account)

## Uses the rest api.(Ver 1.1)

## List of API Currently Covered:

* API to fetch from a User Timeline (statuses/user_timeline)
* API to fetch current Trends (trends/place)
* API to search tweets for a trend.
* More will be added

## Usage

* Clone the repo first and create a constants.py under twitter directory.
* Add the following in the above created file
```
CONSUMER_KEY = your consumer key
CONSUMER_SECRET = your consumer secret
```
* Look at test.py to understand how to use the module.


## And Example to show the usability.

### Time Zone Wise Contribution to trends

> Takes 100 tweets for every trending topic and pushes it into a database(trend_insert.py).[Yet to be ported]
> Prints Time-Zone wise contribution for each trending topic(calculate.py).[Yet to be ported]
> Uses [MongoDB](http://www.mongodb.org/ "MongoDB") and moongodb client for python

## TODO
* Adding more wrapper for different use-cases.
* Adding wrappers to fetch stale data from db.
* Making a python module out of this.
