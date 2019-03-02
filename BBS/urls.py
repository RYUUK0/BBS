"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from blog import views, blog_url
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #登录
    re_path('^login/$', views.login),
    #注册
    re_path(r'^register/$', views.register),
    #首页
    re_path(r'^index/$', views.index),
    #注销函数
    re_path(r'^logoff/$', views.logoff),

    #使用路由分发
    re_path(r'^blog', include(blog_url)),

    #关于后台管理的函数
    re_path(r'^backstage/add_article', views.add_article),

    #后台管理总页面
    re_path(r'^backstage/total', views.control_backstage),



    #处理极验滑动验证码的视图函数
    re_path(r'^pc-geetest/register', views.get_geetest),
    #测试向视图函数
    re_path('^test/$', views.test),
    #media相关的路由设置
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT})
]
