import json
import tweepy
from google.cloud import pubsub_v1
from google.oauth2 import service_account
key_path = "project-tweet-359811-fb0d85feafbc.json"
credentials = service_account.Credentials.from_service_account_file(
key_path,
scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = client.topic_path('project-tweet', 'tweets')
consumer_key = 'ALSKTAyOEQwSKwH6LML4u1CDb'
consumer_secret = 'gdA2jRr6VCpZpYAqOB6t94xp2NFjUHj5EFp4l8vNI1rFgcwPgs'
access_token  = '1558754145355476992-PYGHMZxkVpuRi3OsMJroNxwfDx3b4c'
access_token_secret  = 'qBY5CaZbwnviN161VnmT3ohewKSL7f3IPSnwlYJjO1tTk'

class SimpleStreamListener(tweepy.Client):
    def on_status(self, status):
        print(status)
        tweet = json.dumps({'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)
        client.publish(topic_path, data=tweet.encode('utf-8'))
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

stream_listener = SimpleStreamListener(consumer_key, consumer_secret,access_token, access_token_secret)

stream_listener.get_bookmarks()

