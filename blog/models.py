# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    '''customized manager to retrieve all posts with the published status'''
    def get_queryset(self):
        '''The get function of the customized manager'''
        return super().get_queryset().filter(satus='published')



class Post (models.Model):
    '''This is Blog's Post Data Schema'''
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name = 'blog_posts'
    )
    # testField = models.CharField(max_length=250, default='AnasKhanTesting')
    body = models.TextField(default='Default Body')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    satus = models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='draft')

    objects = models.Manager() # The default manager.
    
    # this published custom manager was conflicting with 
    # the published variable defined above. Thus, I changed 
    # it to objects_published
    objects_published = PublishedManager() #my custom manager
    
    class Meta:
        '''Add the metadata'''
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        '''To build the canonical URL for Post objects'''
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
