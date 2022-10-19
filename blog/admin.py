from django.contrib import admin
from .models import Post
# Register your models here.
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # 展示文章列表
    list_filter = ('status', 'created', 'publish', 'author')  # 右侧过滤器
    search_fields = ('title', 'body')  # 上方搜索框
    prepopulated_fields = {'slug': ('title',)}  # 新增post时如是英文自动填充，链接跟随标题
    raw_id_fields =('author', )  # 会添加一个小组件
    date_hierarchy = 'publish'  # 列表上方会增加一个可以钻取的发布时间小控件
    ordering = ('status', 'publish') # 排序设置，按照状态、发布时间

    
    