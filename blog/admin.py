# Register your models here.
from django.contrib import admin
from .models import Post

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''This is the Custom Administration Site'''
    list_display = ('title', 'slug', 'author', 'publish', 'satus')
    list_filter = ('satus', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {
        'slug': ('title',)
    }
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('satus',  'publish')

