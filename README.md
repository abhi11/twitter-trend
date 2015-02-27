# Twitter API wrapper

## Uses the REST API(Version 1.1)

## List of API Currently Covered:

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
* After adding the above lines in constants.py, come back to the root directory:
```
cd ~/twitter-trend/
```
* And run
```
sudo python setup.py install
```
* To check whether installation is done, cd to tests and run the tests.
```
cd tests && python test.py
```
* The above would also check whether CONSUMER_KEY and CONSUMER_SECRET are valid.


## An Example to show the usability.
Creating a twitter-trend object -
```
twitter_obj = twrapper(CONSUMER_KEY, CONSUMER_SECRET)
```
what this does is -
* Authenticates application using key and secret.
* Stores the obtained token for later requests.

Now you can use this `twitter_obj` to fetch data.
Let's say you want to fetch the latest couple of tweets from Leonardo DiCaprio, from his Twitter handle - @LeoDiCaprio

```
tweets = twitter_obj.get_user_timeline_tweets("LeoDiCaprio", 2)

```
and that's it!

Check out [test.py](https://github.com/abhi11/twitter-trend/blob/master/tests/test.py) which contains examples demonstrating different calls.

### Time Zone Wise Contribution to trends

* Takes 100 tweets for every trending topic and pushes it into a database(trend_insert.py).[Yet to be ported]
* Prints Time-Zone wise contribution for each trending topic(calculate.py).[Yet to be ported]
* Uses [MongoDB](http://www.mongodb.org/ "MongoDB") and moongodb client for python

## TODO
* Adding more wrapper for different use-cases.
* Adding wrappers to fetch stale data from db.
* Remove the dependency on constants.py(ugly). Ask user to provide it directly(For tests read from s specified file given as a command line argument).
