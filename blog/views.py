# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    '''To (render) list all the published posts'''
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})
    
def post_detail(request, year, month, day, post):
    '''To display a single post'''
    post = get_object_or_404(Post,  slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    return render(request, 'blog/post/detail.html', {'post':post}) 


