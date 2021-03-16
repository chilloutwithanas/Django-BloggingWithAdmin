# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
def post_list(request):
    '''To (render) list all the published posts'''
    #posts = Post.objects_published.all()
    object_list = Post.objects_published.all()
    paginator = Paginator(object_list, 4) # 4 posts in each page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not correct then reflect the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page out of range then the relect the last page
        posts = paginator.page(paginator.num_pages)    
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})
    
def post_detail(request, year, month, day, post):
    '''To display a single post'''
    post = get_object_or_404(Post,  slug=post,
                                    satus='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    return render(request, 'blog/post/detail.html', {'post':post}) 


