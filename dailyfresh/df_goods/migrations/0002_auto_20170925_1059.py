# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('img_url', models.ImageField(upload_to='goods', verbose_name='图片路径')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
        migrations.AlterField(
            model_name='goods',
            name='goods_status',
            field=models.SmallIntegerField(default=1, choices=[(1, '上线商品'), (2, '下线商品')], verbose_name='商品状态'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='goods_type_id',
            field=models.SmallIntegerField(default=1, choices=[(1, '新鲜水果'), (2, '海鲜水产'), (3, '猪牛羊肉'), (4, '禽类蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')], verbose_name='商品类型'),
        ),
        migrations.AddField(
            model_name='image',
            name='goods',
            field=models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品'),
        ),
    ]
