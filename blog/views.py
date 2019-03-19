from django.shortcuts import render, HttpResponse, redirect
from blog import models
from geetest import GeetestLib
from blog import myforms
from django.db.models import Count
import json
from blog.templatetags.my_tags import get_func_list

# Create your views here.


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理请求滑动验证码的函数
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 登录函数
def login(request):
    if request.method == "POST":
        # 初始化登录状态字典
        ret = {'status': False, 'mes': None}

        # 获取极验所需验证信息
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        # 判断验证码是否正确
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        # 如果验证码正确,获取用户数据
        if result:
            # print(request.POST.get('username'))
            # print(request.POST.get('userpass'))
            userinfo = myforms.Login(request.POST)
            # 通过校验
            if userinfo.is_valid():
                request.session['login_user_name'] = userinfo.cleaned_data['username']
                ret['status'] = True
                ret['mes'] = '/index/'

            else:
                ret['mes'] = userinfo.errors
                # print(ret)

        return HttpResponse(json.dumps(ret))
    elif request.method == 'GET':
        form_obj = myforms.Login()
        return render(request, 'login.html', {'forms_obj': form_obj})

# 注册函数
def register(request):
    if request.method == 'GET':
        # 传入空的表单对象生成HTML标签
        form_obj = myforms.Register()
        return render(request, 'new_register.html', {'forms_obj': form_obj})

    else:
        # 创建一个form对象
        reg_obj = myforms.Register(request.POST)
        # print(reg_obj)
        # 初始化状态信息
        res = {'status': False, 'mes': None}
        # 如果通过form校验
        if reg_obj.is_valid():
            print('通过校验')
            reg_obj.cleaned_data.pop('re_password')
            avator_img = request.FILES.get('avator')
            # 在数据库创建信息
            models.UserInfo.objects.create(avator=avator_img, **reg_obj.cleaned_data)

            # 改变状态信息
            res['status'] = True
            res['mes'] = '/login/'
            return HttpResponse(json.dumps(res))
        # 未通过form验证
        else:
            print("未通过验证")
            res['mes'] = reg_obj.errors
            return HttpResponse(json.dumps(res))
# 注销函数
def logoff(request):
    if request.session.get('login_user_name'):
        del request.session['login_user_name']
    return redirect('/index/')
# 首页视图函数
def index(request):
    if request.method == 'GET':
        article_list = models.Article.objects.all()
        cate_list = models.Category.objects.all().values('title')
        print(cate_list)
        return render(request, 'index.html', {'all_art': article_list, 'cate_list': cate_list})
# 设置函数
def settings(request):
    if request.method == 'GET':
        return render(request, 'user_set.html')

    else:
        change_field = request.POST.get('change')
        data = request.POST.get('data')
        res = {'success': False, 'reason': None}
        if data and change_field:
            data= json.loads(data)
            # print(data)
            # if change_field == 'name':
            #     new_username = data.get('new_username')
            #     print(new_username)
            #     print('修改名字')
            # elif change_field == 'password':
            #     old_password = data.get('old_password')
            #     new_password = data.get('new_password')
            #     re_password = data.get('re_password')
            #     print(old_password, new_password, re_password)
            #     print('修改密码')
            # elif change_field == 'email':
            #     new_email = data.get('new_email')
            #     print(new_email)
            #     print('修改邮箱')
            set_data = myforms.Clean_Set(change_field, data)
            #返回FALSE
            if set_data.updata_data():
                res['reason'] = '修改成功'
                res['success'] = True
            else:
                res['reason'] = set_data.errors
        else:
            res['reason'] = '请输入正确数据'

        return HttpResponse(json.dumps(res))

# 个人首页函数
def personal(request, username):

    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    art_list = models.Article.objects.filter(author__username=username)
    cate_id = request.GET.get('cate_id')
    print('分类ID是', cate_id)
    if cate_id:
        art_list = art_list.filter(category_id = cate_id)

    return render(request, 'person_index.html', {'username': username,
                                                'art_list': art_list.all(),
                                                })


# 文章详情展示
def art_select(request, art_id):

    # 首先获得作者姓名
    art_obj = models.Article.objects.filter(id = art_id).first()
    username = art_obj.author
    # 获取文章具体内容
    art = models.Article.objects.filter(id = art_id).first()

    #获取文章的点赞数
    gorb_obj = models.GorB.objects.filter(art = art_obj).values('outcome').annotate(good_num = Count('id')).values('outcome', 'good_num')
    print(gorb_obj)
    #print(type(res))

    #获取全部评论
    #根评论,父评论字端为空，
    father_discuss = models.Discuss.objects.filter(article_id = art_id, father_id = None,).all()
    return render(request, 'person_article.html', {'username': username,
                                                   'art': art,
                                                   'gorb_list': gorb_obj,
                                                   'father_discuss': father_discuss,
                                                   })

#处理点赞的函数
def get_gorb(request):
    outcome = request.POST.get('outcome')
    print(outcome, type(outcome))
    #用form表单进行验证数据
    gorbinfo = myforms.GorB(request.POST)
    #创建一个字典
    res = {'status': False, 'mes': None}
    #通过
    print(gorbinfo.errors)
    if gorbinfo.is_valid():
        res['status'] = True
        user = gorbinfo.cleaned_data['username']
        art = gorbinfo.cleaned_data['article']
        outcome = gorbinfo.cleaned_data['outcome']
        #print(user, art, outcome)
        #在数据库中创建记录
        create_user = models.UserInfo.objects.filter(username = user).first()
        create_art = models.Article.objects.filter(id = art).first()
        models.GorB.objects.create(user = create_user, art = create_art, outcome = outcome)

    #未通过验证
    else:
        res['mes'] = gorbinfo.errors


    return HttpResponse(json.dumps(res))

#处理评论的函数
def get_detail(request):
    #分别获取文章ID, 评论用户ID, 评论内容, 评论的父ID
    art_id = request.POST.get('art_id')
    user_id = request.POST.get('user_id')
    content = request.POST.get('content')
    father_id = request.POST.get('father_id')
    #print(content)
    #print(user_id)
    #print(art_id)

    #create_user = models.UserInfo.objects.filter(id = user_id).first()
    #create_art = models.Article.objects.filter(id = art_id).first()
    #create_father = models.Discuss.objects.fileter(id = father_id).first()

    #判断是否为根评论
    if not father_id:
        models.Discuss.objects.create(user_id = user_id, article_id = art_id, comment = content,)

    else:
        models.Discuss.objects.create(user_id = user_id, article_id = art_id, comment = content, father_id = father_id)


    return HttpResponse('llllllll')


#发送该文章的全部评论函数
def comment_list(request, art_id):
    all_comment = models.Discuss.objects.filter(article_id = art_id).values('id', 'comment', 'father_id')
    ret = list(all_comment)
    ret = json.dumps(ret)
    return HttpResponse(ret)

#后台管理页面
def control_backstage(request):
    return render(request, 'control_backstage.html')

#添加文章
def add_article(request):

    #访问页面
    if request.method == 'GET':
        return render(request, 'add_article.html')
    #添加数据
    else:
        pass
    return redirect('')


# 测试函数
def test(request):
    user_pk = 2
    user_password = models.UserInfo.objects.filter(pk=user_pk).values('password').first()
    print(user_password)

    print('is False')
    return HttpResponse('ooookkkk')


