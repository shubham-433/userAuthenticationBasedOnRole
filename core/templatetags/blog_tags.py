from django import template
from ..models import *
from django.db.models import Count
register = template.Library()
from django.template.defaultfilters import truncatewords
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('latest_post.html')
def show_latest_posts(count=5):
    latest_posts=Post.published.order_by('publish')[0:count]
    for post in latest_posts:
        post.body = truncatewords(post.body, 10)
    return {'latest_posts':latest_posts}


@register.inclusion_tag('post_category.html')
def post_category():
    post_category=Category.objects.all()
    return {'post_category':post_category}


# @register.simple_tag
# def get_most_commented_posts(count=5):
#  return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


   

from django.utils.safestring import mark_safe
import markdown
@register.filter(name='markdown')
def markdown_format(text):
 return mark_safe(markdown.markdown(text))


