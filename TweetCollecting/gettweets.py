#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import json
import sys
import dotenv # import the .env with privat data

# Twitter API credentials (put it in .env file and set .gitignore, so you dont push these to git ;))
access_key = "YOUR_ACCESS_KEY"
access_secret = "YOUR_ACCESS_SECRET"
owner = "USERNAME"
owner_ID = "USER_ID"
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"

def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=199)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    i = 0
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("Tweet " + str(len(alltweets)))
        i += 1
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=199, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    # print total tweets fetched from given screen name
    print("Total tweets downloaded from %s are %s" % (screen_name, len(alltweets)))

    return alltweets


def fetch_tweets(screen_names):
    # initialize the list to hold all tweets from all users
    alltweets = []

    # get all tweets for each screen name
    for screen_name in screen_names:
        alltweets.extend(get_all_tweets(screen_name))

    return alltweets


def store_tweets(alltweets, file):
    # a list of all formatted tweets
    tweet_dict = dict()
    i = 0

    for tweet in alltweets:
        # a dict to contain information about single tweet
        tweet_information = dict()

        # text of tweet
        tweet_information['text'] = tweet.text.encode().decode("unicode-escape").encode("latin").decode("utf8")

        # date and time at which tweet was created
        tweet_information['created_at'] = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # id of this tweet
        tweet_information['id_str'] = tweet.id_str

        # source of the tweet
        tweet_information['source'] = tweet.source

        # check if it's a retweet
        #tweet_information['retweet'] = tweet.retweet

        # retweet count
        #tweet_information['retweet_count'] = tweet.retweet_count

        # favourites count
        #tweet_information['favorite_count'] = tweet.favorite_count

        # screename of the user to which it was replied (is Nullable)
        tweet_information['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name

        # user information in user dictionery
        #user_dictionery = tweet._json['user']

        # no of followers of the user
        #tweet_information['followers_count'] = user_dictionery['followers_count']

        # screename of the person who tweeted this
        #tweet_information['screen_name'] = user_dictionery['screen_name']

        # add this tweet to the tweet_list
        tweet_dict[i] = tweet_information

        i += 1

    file_des = open(file, "w")

    #for single_tweet in tweet_list:
    #    for item in single_tweet:
    #        file_des.write(str(item) + ": " + str(single_tweet[item]) + "\n")
    #    file_des.write("\n")

    # dump tweets to the file
    json.dump(tweet_dict, file_des, indent=4, sort_keys=True)

    # close the file_des
    file_des.close()


def getalltweets(filename, age):
    file = open(filename, "r", encoding='utf-8')

    remember = open("counted_tweets.txt", "a+", encoding='utf-8')

    if (file):
        print("File openend")

    total = 0
    people = 0

    for line in file:
        user = line.strip()
        people += 1
        print(user)
        remember.write(user)
        alltweets = get_all_tweets(user)
        remember.write(": " + str(len(alltweets)) + "\n")
        total += len(alltweets)
        store_tweets(alltweets, "Tweets/" + age + "/" + user + ".json")

    remember.write("Total tweets: " + str(total) + "\n")
    remember.write("People: " + str(people))


if __name__ == "__main__":
    getalltweets(sys.argv[1], sys.argv[2])
