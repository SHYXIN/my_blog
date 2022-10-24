from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    # changefreq和属性表示您的帖子页面的priority更改频率及其在您网站中的相关性（最大值为1）
    changefreq ='weekly'
    priority = 0.9
    
    def items(self):
        # 该items()方法返回要包含在此站点地图中的对象的 QuerySet。默认情况下，Django 调用get_absolute_url()每个对象的方法来检索其 URL。请记住，
        # 您在第 1 章，构建博客应用程序中创建了此方法，用于检索帖子的规范 URL。如果要为每个对象指定 URL，可以location向站点地图类添加一个方法。
        return Post.published.all()

    
    def lastmod(self, obj):
        # 该lastmod方法接收返回的每个对象，items()并返回该对象最后一次被修改的时间。
        return obj.updated