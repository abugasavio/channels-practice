from channels import Group


def connect_tweeter(message):
    Group('livetweets').add(message.reply_channel)


def disconnect_tweeter(message):
    Group('livetweets').discard(message.reply_channel)

