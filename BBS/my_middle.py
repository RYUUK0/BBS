from django.shortcuts import render, redirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from blog import models

class Check_Session(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        #判断是否有登录信息
        username = request.session.get('login_user_name')
        if username :
            userinfo = models.UserInfo.objects.filter(username = username).first()
            #print(request.session.get('login_user_name'))
            request.userinfo = userinfo
            return None
        else:
            request.userinfo = {}
            return None
    def process_response(self,request, response):
        return response