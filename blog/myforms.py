from django import forms
from django.core.exceptions import ValidationError
from blog import models

#定义一个用于注册的表单类
class Register(forms.Form):
    username = forms.CharField(
        max_length = 16,
        min_length = 6,
        required = True,
        label = '账户',
        error_messages = {
            'max_length': '最大长度不能超过16',
            'min_length': '最小长度不能低于6',
            'required': '用户输入不能为空'
        },
        widget = forms.widgets.TextInput(
            attrs = {'class': 'form-control'},
        )
    )
    password = forms.CharField(
        max_length=16,
        min_length=6,
        required=True,
        label = '密码',
        error_messages={
            'max_length': '最大长度不能超过16',
            'min_length': '最小长度不能低于6',
            'required': '用户输入不能为空'
        },
        widget = forms.widgets.PasswordInput(
            attrs = {'class': 'form-control'},
            render_value = True,

        )
    )
    re_password = forms.CharField(
        max_length=16,
        min_length=6,
        required=True,
        label = '确认密码',
        error_messages={
            'max_length': '最大长度不能超过16',
            'min_length': '最小长度不能低于6',
            'required': '用户输入不能为空'
        },
        widget = forms.widgets.PasswordInput(
            attrs = {'class': 'form-control'},
            render_value = True,
        )
    )

    #重写clean函数，对输入数据进行进一步校验
    def clean(self):
        userpass = self.cleaned_data.get('password')
        re_userpass = self.cleaned_data.get('password')
        #两次密码不一致
        if re_userpass and re_userpass != userpass:
            self.add_error('re_password', ValidationError('两次密码不一致'))
        else:
            return self.cleaned_data

    def clean_username(self):
        input_user = self.cleaned_data.get('username')
        is_alive = models.UserInfo.objects.filter(username = input_user).first()
        # 返回结果为真--》存在相同用户名
        if is_alive:
            self.add_error('username', ValidationError('用户已存在'))
        else:
            return self.cleaned_data['username']


#定义一个用于登录的表单类
class Login(forms.Form):
    username = forms.CharField(
        max_length = 16,
        min_length = 6,
        required = True,
        label = '用户名',
        widget = forms.widgets.TextInput(
            attrs = {'class': 'form-control'},
        ),
        error_messages = {
            'max_length': '长度不能超过16',
            'min_length': '长度不能小于8',
            'required': '用户名不能为空',
        },
    )
    password = forms.CharField(
        max_length = 16,
        min_length = 6,
        required = True,
        label = '密码',
        widget = forms.widgets.PasswordInput(
            attrs = {'class': 'form-control'},
            render_value = True,
        ),
        error_messages={
            'max_length': '长度不能超过16',
            'min_length': '长度不能小于8',
            'required': '请输入密码',
        },
    )

    #username的检验函数
    def clean_username(self):
        get_name = self.cleaned_data.get('username')
        #从数据库中检验用户是否存在
        is_alive = models.UserInfo.objects.filter(username = get_name).first()
        #如果不存在
        if not is_alive:
            self.add_error('username', ValidationError('用户不存在'))
        else:
            return self.cleaned_data['username']

    def clean(self):
        get_name = self.cleaned_data.get('username')
        get_pass = self.cleaned_data.get('password')
        user_obj = models.UserInfo.objects.filter(username = get_name).first()
        #print(type(get_name))
        #print('账户名是',get_name)
        #print(type(get_pass))
        #print('获得的密码是', get_pass)

        #密码验证
        if user_obj and get_pass == user_obj.password:
            #print(user_obj.password)
            return self.cleaned_data
        else:
            self.add_error('password', ValidationError('密码错误'))


#定义用于处理点赞验证的表单类
class GorB(forms.Form):

    username = forms.CharField(
        max_length = 20,
        min_length = 6,
        required = True,
        error_messages = {'required': '请登录'}
    )
    article = forms.IntegerField(
        required = True,
        error_messages = {'required': '选择文章'}
    )
    outcome = forms.CharField(
        required = True,
    )

    def clean_outcome(self):
        get_out = self.cleaned_data['outcome']
        if get_out == 'true':
            self.cleaned_data['outcome'] = True

        else:
            self.cleaned_data['outcome'] = False

        return self.cleaned_data['outcome']
    def clean(self):
        username = self.cleaned_data.get('username')
        #print(username)
        article = self.cleaned_data.get('article')
        #判断是否评论过
        is_gorbed = models.GorB.objects.filter(user__username = username, art__id = article)
        if is_gorbed:
            self.add_error('outcome', ValidationError('该用户已经评论过了'))
        else:
            return self.cleaned_data




#验证评论的表单
class Detail(forms.Form):
    user_id = forms.IntegerField(required = True,)
    art_id = forms.IntegerField(required = True, )
    father_id = forms.IntegerField(required = False,)
    content = forms.CharField(min_length = 10,
                              required = True,
                              error_messages = {
                                  'required': '请填写评论',
                                  'min_length': '评论最少十个字',
                              }
                              )

