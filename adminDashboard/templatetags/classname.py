from django import template
import datetime
register = template.Library()
@register.filter(name="getClassName")
def getClassName(value):
    return value.__class__.__name__
def contains(arrays,text):
    for item in arrays:
        if (item in text):
            return True
@register.filter(name="getLinks")
def getLinks(episode_obj):
    blocked = ["asianload",]
    if episode_obj.__class__.__name__.lower()=="episode":
        return [link for link in episode_obj.watch_episode.all() if not contains(blocked,link.source) ]
    return [link for link in episode_obj.watch.all() if not contains(blocked,link.source) ]
@register.filter
def isActive(obj):
    return obj.added_on.date() == datetime.date.today()