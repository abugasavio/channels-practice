import json
from channels import Group
from .models import Liveblog

# The 'slug' keyword argument here comes from the regex capture group in
# routing.py


def connect_blog(message, slug):
    try:
        liveblog = Liveblog.objects.get(slug=slug)
    except Liveblog.DoesNotExist:
        # You can see what messages back to a Websocket lool
        message.reply_channel.send({
            'text': json.dumps({'error': 'bad_slug'}),
            'close': True,
        })
        return
    # Each different client has a different "reply_channel", which is how you
    # send information back to them. We can add all the different reply channels
    # to a single Group, and the when we send a message to the Group, they'll get the
    # same message
    Group(liveblog.group_name).add(message.reply_channel)


def disconnect_blog(message, slug):
    """
    Removes the user from the liveblog group when they disconnect.
    Channels will auto-cleanup eventually, but it can take a while, and having old
    entries cluttering up your group will reduce performance.
    """
    try:
        liveblog = Liveblog.objects.get(slug=slug)
    except Liveblog.DoesNotExist:
        # This is the disconnect message, so the socket is already gone; we can't
        # send an error back. Instead, we just return from the consumer.
        return
    # It's called .discard() because if the reply channel is already there it
    # won't fail - just like the set() type.
    Group(liveblog.group_name).discard(message.reply_channel)

