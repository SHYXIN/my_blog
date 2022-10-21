from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):

    def get_queryset(self):
        # 依旧返回查询器，但是已经默认必须为“发布”装填
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '发布'),
    )
    title = models.CharField(verbose_name='标题', max_length=255)
    slug = models.SlugField(
        max_length=255, verbose_name='链接', unique_for_date='publish')
    author = models.ForeignKey(
        User, verbose_name='作者', on_delete=models.CASCADE, related_name='blog_post')  # 将指定数据库表名
    body = models.TextField(verbose_name='正文',)
    publish = models.DateTimeField(verbose_name='发布时间', default=timezone.now)
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    status = models.CharField(
        verbose_name='状态', max_length=10, choices=STATUS_CHOICES, default='draft')

    # ORM管理器
    objects = models.Manager()  # 默认的管理器
    published = PublishedManager()  # 我们自定义的模型管理器

    # 添加标签
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        # 可以在template中用这个获得路径
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    # related_name 用来设置查询
    # 默认是post.commet_set.all() ,如下设置后就是post.comments.all()
    post = models.ForeignKey(Post, 
                             related_name='comments',  
                             on_delete=models.CASCADE,
                             verbose_name='博客')
    
    name = models.CharField(max_length=80,verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    body = models.TextField(verbose_name='正文')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    active = models.BooleanField(verbose_name='active标识',
                                 default=True) # 可以删除不合适的评论
    
    class Meta:
        ordering = ('created', )
    
    def __str__(self):
        return f'{self.name}评论了{self.post}'
    