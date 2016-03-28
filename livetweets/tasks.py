from django.conf import settings
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


def stream_tweets():
    listener = StdOutListener()
    auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    # filter tweets
    stream.filter(track=['python', 'javascript', 'ruby'])
