# Generated by Django 2.1.4 on 2019-01-13 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20190112_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discuss',
            name='father',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Discuss'),
        ),
    ]
