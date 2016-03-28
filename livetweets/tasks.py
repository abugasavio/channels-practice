import json
from django.conf import settings
from channels import Group
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class LivetweetsListener(StreamListener):

    def on_data(self, data):

        data = json.loads(data)
        print(data)

        tweet = {
            "id": data["id"],
            "user": data['user']['screen_name'],
            "text": data['text'],
            "created": data['created_at'],
        }
        # Encode and send that message to the whole channels Group for our
        # liveblog. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        Group('livetweets').send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(tweet),
        })
        return True

    def on_error(self, status):
        print(status)


def stream_tweets():
    listener = LivetweetsListener()
    auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    # filter tweets
    #stream.filter(track=['javascript', 'ruby', 'python', 'easter monday'])
    stream.filter(track=['safaricom', 'safaricomltd', 'mpesa', 'safaricom_care'
                         'airtel_ke', 'airtel kenya' 'airtel_kenya',
                          'zuku', 'hudumakenya', 'kplc'])
