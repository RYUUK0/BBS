from django.contrib import admin
from blog import models

# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.GorB)
admin.site.register(models.ArtDetail)
admin.site.register(models.Category)
admin.site.register(models.Discuss)
admin.site.register(models.Tag)
admin.site.register(models.Article)