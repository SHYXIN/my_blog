from django.urls import path
from . import views
from .feeds import LastestPostFeeds

app_name = 'blog'

urlpatterns = [
    # 博客
    path('', views.post_list, name='post_list'),   # 博客列表
    path('list/', views.PostListView.as_view(), name='post_list2'), # 博客列表class
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),  # 博客单页
    
    # 标签 ,重用了post_list函数
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    
    # 增加feed
    path('feed/',LastestPostFeeds(), name='post_feed'),
    
    # 增加全文搜索功能
    path('search/',views.post_search, name='post_search'),

]
