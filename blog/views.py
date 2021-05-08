# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
# from django.views import ListView
from django.views.generic.list import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

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

class PostListView(ListView):
    queryset = Post.objects_published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'
    
def post_share(request, post_id):
    # Get the post using the id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    
    # if the data has been posted
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # All the form's field passed validation
            cd = form.cleaned_data
            # Send the Email Now
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'f14365fbd2994a3f8110@mailspons.com', cd['to'])
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', 
                  {'post':post, 'form':, 'sent':sent})

