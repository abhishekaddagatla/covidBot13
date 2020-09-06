import tweepy
import requests
from datetime import datetime
import time

#TWITTER API INITIALIZATION
consumer_key = '####'
consumer_secret = '####'
access_token = '####'
access_token_secret = '####'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#ACCESSING OPEN COVID19 API
covidDailyURL = 'https://api.covid19api.com/world/total'
covidDaily = requests.get(covidDailyURL).json()


def Generate_Desc():
    Cases = covidDaily['TotalConfirmed']
    Deaths = covidDaily['TotalDeaths']
    Recovered = covidDaily['TotalRecovered']

    desc = "TODAYS STATS [" + str(
        datetime.today().date()) + "]\nTotal Confirmed Cases: " + str(
            Cases) + "\nTotal Confirmed Deaths: " + str(
                Deaths) + "\nTotal Confirmed Recovered: " + str(
                    Recovered
                ) + "\nThat's alot! Stay safe and dont forget to wear a mask!"
    return desc


#FUNCTION FOR POSING THE STATS
def Generate_Tweet(tweet):
    message = tweet
    api.update_status(status=message)

# def Generate_Tweet():
#     message = datetime.today().time()
#     api.update_status(status = message)


#timer to post at noon everyday

while True:
    Generate_Tweet(Generate_Desc())
    time.sleep(86400)
