import json
from django.db import models
from django.template.defaultfilters import linebreaks_filter
from channels import Group


class Liveblog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return "/liveblog/%s/" % self.slug
        
    @property
    def group_name(self):
        """
        Returns the Channels Group name to use for sending notifications
        """
        return "liveblog-%s" % self.id


class Post(models.Model):
    liveblog = models.ForeignKey(Liveblog, related_name="posts")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#%i: %s" % (self.id, self.body_intro())

    def body_intro(self):
        return self.body[:50]

    def html_body(self):
        return linebreaks_filter(self.body)

    def send_notification(self):
        """
        Sends a notification to everyone in our Liveblog's group with our
        content.
        """
        # Make the payload of the notification. We'll JSONify this, so it has
        # to be simple types, which is why we handle the datetime here.
        notification = {
            "id": self.id,
            "html": self.html_body(),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }
        # Encode and send that message to the whole channels Group for our
        # liveblog. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        Group(self.liveblog.group_name).send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(notification),
        })

    def save(self, *args, **kwargs):
        """
        Hooking send_notification into the save of the object as I'm not
        the biggest fan of signals.
        """
        result = super(Post, self).save(*args, **kwargs)
        self.send_notification()
        return result