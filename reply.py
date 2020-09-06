import tweepy
import requests
from tweepy.streaming import StreamListener
from tweepy import Stream
import json

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

# 1. read a tweet that has us @
# 2. Check for keywords
# 3. access api with keywords
# 4. https://api.covid19api.com/country/<country>/status/confirmed
# 3.5. make sure that incorrect spellings etc. return an error

def reply(data):
    sn = data['user']['screen_name']
    country = data['text'][19:]
    realCountry = ''
    for i in range(len(country)):
        if country[i] == ' ':
            realCountry = country[0:i] + '-' + country[i + 1:]
        else:
            realCountry = country
    template = 'https://api.covid19api.com/country/' + realCountry + '/status/confirmed'
    countryJSON = requests.get(template).json()
    if len(countryJSON) > 1:
        confirmedCasesCountry = countryJSON[-1]['Cases']
        finalTweet = '@' + sn + " Confirmed Cases in " + realCountry + ": " + str(confirmedCasesCountry)
        api.update_status(finalTweet, data['user']['id'])
    else:
        finalTweet = '@' + sn + ' no results found for country: ' + realCountry + '. Maybe try checking your spelling'
        api.update_status(finalTweet, data['user']['id'])

class StdOutListener(StreamListener):
    def on_data(self, data):
        givenData = json.loads(data)
        reply(givenData)
        return True
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener()
    stream = Stream(auth, listener)

    stream.filter(track = ['@covidBot13 STATUS'])
