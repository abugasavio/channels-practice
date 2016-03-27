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
        return "/liveblog/%s/" % self.blog
        
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