from blog import views
from django.urls import re_path, path, include
from django.views.static import serve
from django.conf import settings




urlpatterns = [
    #在整则表达式中用命名的方式
    #依次为添加评论， 点赞， 查询评论的视图函数
    re_path(r'detail/$', views.get_detail),
    re_path(r'gorb/$', views.get_gorb),
    re_path(r'comment_list/(\d+)/$', views.comment_list),

    #文章详情
    re_path(r'article/(?P<art_id>\d+)$',views.art_select),

    #显示个人首页
    re_path(r'(?P<username>\w+)', views.personal),


    #media相关的路由设置
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]