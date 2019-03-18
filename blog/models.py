from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


#用户表
class UserInfo(AbstractUser):
    """
    username: 账户名
    userpass: 密码
    avator: 头像图片
    create_time: 创建用户时间
    blog: 用户的博客ID
    """
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    create_time = models.DateTimeField(auto_now_add = True)
    avator = models.FileField(upload_to = "avators_pic/", default = "avators_pic/111.png", verbose_name = '头像')
    blog = models.OneToOneField(to = "Blog",to_field="id", null = True, on_delete = models.CASCADE)


    def __str__(self):
        return self.username

#博客信息表
class Blog(models.Model):
    """
    title: 标签页名字
    site: 博客标签分类
    theme: 主题风格
    """
    title = models.CharField(max_length = 30, )
    site = models.CharField(max_length = 50, unique = True)
    theme = models.CharField(max_length = 40, )

    def __str__(self):

        return self.title



#文章表
class Article(models.Model):
    """
    title: 文章标题
    write_time: 创作时间
    desc: 文章简介
    author: 文章作者
    categort: 文章的分类，一个类别对应多个文章
    tag: 文章与标签的关系为多对多，即一个文章不止有一个标签
    """
    title = models.CharField(max_length = 90, null = False)
    write_time = models.DateTimeField(auto_now_add = True)
    desc = models.CharField(max_length = 200)
    author = models.ForeignKey('UserInfo', on_delete = models.CASCADE)
    category = models.ForeignKey(to = 'Category', null = True, on_delete = models.CASCADE)
    tag = models.ManyToManyField(to = 'Tag')



#评论表
class Discuss(models.Model):
    """
    user: 评论用户的ID
    time: 评论时间
    comment: 评论内容
    art: 被评论的文章
    father: 有无父评论，即是否为回复别人的评论
    """
    user = models.ForeignKey('UserInfo', on_delete = models.CASCADE)
    article = models.ForeignKey('Article', on_delete = models.CASCADE)
    create_time = models.DateField(auto_now_add = True)
    comment = models.CharField(max_length = 300, null = False)
    father = models.ForeignKey('self', null = True ,on_delete = models.CASCADE)


#文章的标签
class Tag(models.Model):
    """
    tag_name: 标签名
    blog: 属于某个博客的标签
    """
    tag_name = models.CharField(max_length = 60)
    blog = models.ForeignKey('Blog', on_delete = models.CASCADE)


#文章的分类
class Category(models.Model):
    """
    title: 分类的名称
    blog: 属于某个博客的分类名
    """
    title = models.CharField(max_length = 60)
    blog = models.ForeignKey('Blog', on_delete = models.CASCADE)



#文章详情表
class ArtDetail(models.Model):
    """
    art: 文章的ID
    detail: 文章的全文
    """
    art = models.OneToOneField(to = 'Article', on_delete = models.CASCADE)
    detail = models.TextField()


#点赞表
class GorB(models.Model):
    """
    outcome: 点赞还是差评, True or False
    art: 被评价的文章ID
    user: 评价的用户ID
    """
    outcome = models.BooleanField(default = False)
    art = models.ForeignKey('Article', null = True, on_delete = models.CASCADE)
    user = models.ForeignKey('UserInfo', null = True, on_delete = models.CASCADE)


    class Meta:
        unique_together = ('art', 'user')
