from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

# Create your views here.
def post_list(request):
    objects_list = Post.published.all()
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
    
    return render(request, 'blog/post/list.html', {'posts':posts, 'page': page})

def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    template_name = 'blog/post/list.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by: int = 3
    
