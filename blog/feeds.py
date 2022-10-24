from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LastestPostFeeds(Feed):
    title = '我的博客'
    link = reverse_lazy('blog:post_list')
    description = '我最新的博文'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self,item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.body, 30)
        