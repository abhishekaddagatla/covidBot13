import tweepy
import requests
from datetime import datetime
from threading import Timer

#TWITTER API INITIALIZATION
consumer_key = 'DH2mxQWuKlKjvTQ34GXVRJ2iE'
consumer_secret = 'FeOCVyyjjbqtkhX3v3xMI3WaMMLL4bOttUmuvwqLKNpIXwWJdm'
access_token = '1302277618801217539-HI2IwnhUTWcug4n729aSgNmeFZpzUY'
access_token_secret = 'nEXQRtRH9KrzPjcctvoxMVOyxkQDysKzj6M7B45RbclTe'

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


# 1. read a tweet that has us @
# 2. Check for keywords
# 3. access api with keywords
# 4. https://api.covid19api.com/country/<country>/status/confirmed
# 3.5. make sure that incorrect spellings etc. return an error


def reply():
    example = tweepy.Cursor(api.search, q='@covidbot13').items(1)
    for tweet in example:
        sn = tweet.user.screen_name
        country = tweet.text[19:]
        if (tweet.text[0:19] == "@covidBot13 STATUS "):
            template = 'https://api.covid19api.com/country/' + country + '/status/confirmed'
            countryJSON = requests.get(template).json()
            #print(countryJSON)
            if len(countryJSON) > 1:
                confirmedCasesCountry = countryJSON[-1]['Cases']
                finalTweet = '@' + sn + " Confirmed Cases in " + country + ": " + str(
                    confirmedCasesCountry)
                api.update_status(finalTweet, tweet.id)
            else:
                finalTweet = '@' + sn + ' no results found for country: ' + country + '. Maybe try checking your spelling'
                api.update_status(finalTweet, tweet.id)


#timer to post at noon everyday

x = datetime.today()
y = x.replace(day=x.day + 1, hour=3, minute=49, second=0, microsecond=0)
delta_t = y - x

secs = delta_t.seconds + 1

t = Timer(secs, Generate_Tweet('bruh'))
t.start()
