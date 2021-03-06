# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('recipient_name', models.CharField(max_length=24, verbose_name='收件人')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='收件地址')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮政编码')),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
                ('passport', models.ForeignKey(verbose_name='所属账户', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
