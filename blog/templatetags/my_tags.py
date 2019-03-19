from django import template
from django.db.models import Count
from blog import models

register = template.Library()



#传入作者名，得到分类列表， 标签列表， 日期归档
#用装饰器使其生成HTML组件,函数返回值必须为字典,字段为传入模板的数据
@register.inclusion_tag("left_func_list.html")
def get_func_list(username):

    cate = models.Article.objects.filter(author__username=username).values('category').annotate(
        cate_num=Count("category_id"))
    # 传入前段的数据
    cate_list = []
    # 通过类别ID查询到具体名字
    for user_cate in cate:
        # 创建一个空的字典用于临时储存类别名字，及所包含的文章数量
        cate_info = {}
        cate_dict = models.Category.objects.filter(id=user_cate['category']).values('title', 'pk').first()
        # print(cate_title['title'])
        cate_info['id'] = cate_dict['pk']
        cate_info['title'] = cate_dict['title']
        cate_info['cate_num'] = user_cate['cate_num']
        # 将信息添加到传入给前端的数据列表中
        cate_list.append(cate_info)

    # 获取账号所有文章，对时间进行处理,进行分组
    date_list = models.Article.objects.filter(author__username=username).extra(
        select={"month": "date_format(write_time,'%%Y-%%m')"}
    ).values('month').annotate(date_num=Count("id")).values('month', 'date_num')
    #print(date_list)

    return {'cate_list': cate_list, 'date_list': date_list, 'username': username }