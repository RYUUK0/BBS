# from django.test import TestCase
# # from bs4 import BeautifulSoup
# #
# # # Create your tests here.
# #
# # text = '''
# #     <span>这是spanspanspan</span>
# #     <div>这是divdivdivdiv</div>
# #
# # '''
# # ret = BeautifulSoup(text, 'html.parser')
# # print(ret.text)

from blog import models

user_pk = 2
user_password = models.UserInfo.objects.filter(pk = user_pk).values('password')
print(user_password)