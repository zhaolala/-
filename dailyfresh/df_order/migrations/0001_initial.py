# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0003_browsehistory'),
        ('df_goods', '0002_auto_20170925_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('order_id', models.CharField(serialize=False, help_text='订单id', max_length=64, primary_key=True)),
                ('total_count', models.IntegerField(help_text='商品总数', default=1)),
                ('total_price', models.DecimalField(decimal_places=2, help_text='商品总额', max_digits=10)),
                ('transit_price', models.DecimalField(decimal_places=2, help_text='订单运费', max_digits=10)),
                ('pay_method', models.IntegerField(help_text='支付方式', default=1)),
                ('order_status', models.IntegerField(help_text='订单状态', default=1)),
                ('addr', models.ForeignKey(to='df_user.Address', help_text='收件地址')),
                ('passport', models.ForeignKey(to='df_user.Passport', help_text='用户')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('goods_count', models.IntegerField(help_text='商品数目', default=1)),
                ('goods_price', models.DecimalField(decimal_places=2, help_text='商品价格', max_digits=10)),
                ('goods', models.ForeignKey(to='df_goods.Goods', help_text='商品')),
                ('order', models.ForeignKey(to='df_order.OrderBasic', help_text='基本订单')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
