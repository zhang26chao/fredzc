# !-*-coding=utf8-*-
from django.contrib import admin
from blog.models import Article
from blog.models import Category
from blog.models import Comment
from blog.models import Message
import util

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    actions = ['really_delete_selected', 're_generate_article']
    list_display = ('title', 'create_time')
    search_fields = ('title',)
    fields = ('title', 'english_name', 'category', 'keywords', 'description', 'content')

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            # 先删除数据库记录再删除页面
            obj.delete()
            util.delete_html(obj)
                
    really_delete_selected.short_description = 'delete artile and file'

    # 每次修改模板需要重新生成文件，用这个方法批量生成
    def re_generate_article(self, request, queryset):
        for obj in queryset:
            util.render_html(obj)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'create_time')
    search_fields = ('title',)
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Message, MessageAdmin)
admin.site.register(Category, CategoryAdmin)
