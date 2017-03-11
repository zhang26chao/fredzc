# !-*-coding=utf8-*-
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone 
import util

# Create your models here.
class Category(models.Model):
    name = models.CharField('名称', max_length=20)
    
    def __unicode__(self):
        return self.name
    
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=100)
    summary = models.TextField('摘要', null=True)
    content = RichTextField('内容')
    create_time = models.CharField('创建日期', max_length=16)
    category = models.ForeignKey(Category)
    publish_year = models.CharField('发布年份', max_length=4)
    publish_month = models.CharField('发布月份', max_length=2)
    publish_date = models.CharField('发布日期', max_length=2)
    comment_count = models.IntegerField('评论数', default=0)
    keywords = models.CharField('关键字', null=True, blank=True, max_length=256)
    description = models.CharField('描述', null=True, blank=True, max_length=1024)
    english_name = models.CharField('英文名称', max_length=64)
    path = models.CharField('文件路径', max_length=64)

    def save(self):
        # 修改文章也是调用的save方法，所以需要判断，这样才能保证创建时间不会变
        if not self.create_time:
            self.create_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        elif len(self.create_time) == 14:
            self.publish_year = self.create_time[0:4]
            self.publish_month = self.create_time[4:6]
            self.publish_date = self.create_time[6:8]
        else:
            self.publish_year = self.create_time[0:4]
            self.publish_month = self.create_time[5:7]
            self.publish_date = self.create_time[8:10]
        if not self.publish_date:
            self.publish_year, self.publish_month, self.publish_date = util.get_year_month_day()
#             en_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#             self.publish_date = '%s %d, %s' % (en_months[int(month) - 1], int(date), year)
#             self.publish_month = '%s %s' % (en_months[int(month) - 1], year)
        # 保存摘要
        summary_index = self.content.find('<!--more-->')
        if (summary_index >= 0):
            self.summary = self.content[0:summary_index]
        # 设置文件相对路径
        if len(self.create_time) == 14:
            self.path = '%s/%s/%s.html' % (self.create_time[0:4], self.create_time[4:6], self.english_name)
        else:
            self.path = '%s/%s/%s.html' % (self.create_time[0:4], self.create_time[5:7], self.english_name)
        # 先生成html再保存到数据库，即使保存数据库失败也没有影响；
        # 如果先保存数据库再生成文件，可能出现文件生成失败的情况，那样会出现有数据没有页面的情况
        util.render_html(self)
        super(Article, self).save()
            
class Comment(models.Model):
    email = models.CharField('电子邮箱', max_length=100)
    subject = models.CharField('主题', max_length=100)
    content = RichTextField('内容')
    create_time = models.DateTimeField('创建日期', auto_now_add=True, auto_now=False)
    article = models.ForeignKey(Article)

class Message(models.Model):
    name = models.CharField('名称', max_length=32)
    email = models.EmailField('电子邮箱', max_length=64)
    subject = models.CharField('主题', max_length=255)
    message = models.TextField('内容')
    create_time = models.DateTimeField('创建日期', auto_now_add=True, auto_now=False)
