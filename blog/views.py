from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm, SearchForm
from django.core.mail import send_mail  # 发邮件用
from taggit.models import Tag  # 用来标签的
from django.db.models import Count  # 推荐推荐
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity  # 全文搜索用


# Create your views here.
def post_list(request, tag_slug=None):
    objects_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        objects_list = objects_list.filter(tags__in=[tag])
    paginator = Paginator(objects_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果不是整数，则返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果超出索引，则返回最后一页
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag,
                                                   })


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # 找到这个post所有的comment
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        # 先调用方法如果非法，就会添加error
        if comment_form.is_valid():
            # 创建了新评论但是不提交到数据库中
            new_comment = comment_form.save(commit=False)
            # 将post添加到commnet中
            new_comment.post = post
            # 最后提交，保存数据库中
            new_comment.save()

    else:
        comment_form = CommentForm()

    # 推荐相似博客
    post_tags_ids = post.tags.values_list('id', flat=True)  # 得到tag的id列表
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)  # 得到相似博客，同时排除自己
    # 计算tags的数量，命名为same_tags，按照tags的数量降序，发布时间降序
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     })


class PostListView(ListView):
    template_name = 'blog/post/list.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by: int = 3


def post_share(request, post_id):
    """分享博客"""
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # 是post请求
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 表单校验通过，如果不通过，则会增加error信息
            cd = form.cleaned_data
            # 准备发送邮件
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}推荐你阅读{post.title}"
            message = f"{post.title}链接为{post_url}\n\n" \
                f"{cd['name']} 的评论为 {cd['comments']}"
            send_mail(subject, message,
                      #   'x3280877@gmail.com',
                      'admin@myblog.com',
                      [cd['to']])
            sent = True
    else:
        # get请求初始化部件，展示出来
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': form,
                                                    'post': post,
                                                    'sent': sent,
                                                    })


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # 1
            # results = Post.published.annotate(
            #     search=SearchVector('title', 'body')
            # ).filter(search=query)
            
            # # 2 增加排名
            # search_vectors = SearchVector('title', 'body')
            
            # search_query = SearchQuery(query)
            # results = Post.published.annotate(
            #                 search=search_vectors,
            #                 rank=SearchRank(search_vectors, search_query)
            #                 ).filter(search=query).order_by('-rank')
            
            # # 3 加权排名
            # # 默认权重是D、C、B和A，它们分别指的是数字0.1、0.2、0.4和1.0
            # search_vector = SearchVector('title', weight='A') + \
            #     SearchVector('body', weight='B')
            # search_query = SearchQuery(query)
            # results = Post.published.annotate(
            #         rank=SearchRank(search_vector, search_query)
            #         ).filter(rank__gte=0.3).order_by('-rank')
            
            # 4 三元组检索 yango 词干检索 
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
            

    
    return render(request, 'blog/post/search.html', {'form': form,
                                                     'query': query,
                                                     'results': results,
                                                     })
