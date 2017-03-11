# !-*-coding=utf8-*-
'''
Created on 2017-3-4

@author: Administrator
'''
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import io
import os
import datetime

def render_html(params):
    t = get_template('template.html')  
    html = t.render(Context({'id':params.id,
                             'title':params.title + u' - Fred Zhang的个人博客',
                             'article_title':params.title,
                             'content':params.content,
                             'publish_year':params.publish_year,
                             'publish_month':params.publish_month,
                             'publish_date':params.publish_date,
                             'category':params.category,
                             'create_time':params.create_time,
                             'domain':settings.DOMAIN,
                             'keywords':params.keywords,
                             'description':params.description,
                            }))
    # 文件的绝对路径
    store_path = '%s/%s' % (settings.ARTICLE_PATH, params.path)
    # 判断是否需要创建文件夹
    file_folder = os.path.dirname(store_path)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    fp = io.open(store_path, 'w', encoding='utf8')
    fp.write(html)
    fp.close()

def delete_html(obj):
    store_path = '%s/%s' % (obj.create_time[0:4], obj.create_time[5:7])
    path = '%s/%s/%s.html' % (settings.ARTICLE_PATH, store_path, obj.english_name)
    if os.path.isfile(path):
        os.remove(path)
        
def get_year_month_day():
    date_str = str(datetime.date.today())
    return (date_str[0:4], date_str[5:7], date_str[8:],)