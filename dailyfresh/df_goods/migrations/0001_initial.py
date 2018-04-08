# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('goods_type_id', models.SmallIntegerField(default=1, verbose_name='商品类型')),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_sub_title', models.CharField(max_length=128, verbose_name='商品副标题')),
                ('goods_price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('transit_price', models.DecimalField(verbose_name='商品运费', decimal_places=2, max_digits=10)),
                ('goods_unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品描述')),
                ('goods_image', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('goods_stock', models.IntegerField(default=0, verbose_name='商品库存')),
                ('goods_sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('goods_status', models.SmallIntegerField(default=1, verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
    ]
