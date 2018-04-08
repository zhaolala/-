from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseManager

from df_goods.models import Image
# Create your models here.


class OrderBasicManager(BaseManager):
    '''
    订单基本模型管理类
    '''

    def add_one_basic_info(self, order_id, passport_id, addr_id, pay_method, total_count, total_price, transit_price):
        '''添加一条订单信息'''
        order_basic = self.create_one_object(order_id=order_id, passport_id=passport_id, addr_id=addr_id, pay_method=pay_method, total_count=total_count, total_price=total_price, transit_price=transit_price)
        return order_basic

    def get_order_basic_info_by_passport(self, passport_id):
        '''获取用户的订单信息'''
        order_basic_list = self.get_object_list(filters={'passport_id':passport_id})
        for order_basic in order_basic_list:
            # 根据订单id获取订单的详情信息
            order_detail_list = OrderDetail.objects.get_order_detail_info_by_order_id(order_id=order_basic.order_id)
            # 给order_basic增加一个order_detail_list属性，保存其订单详情
            order_basic.order_detail_list = order_detail_list
        return order_basic_list


class OrderBasic(BaseModel):
    '''
    订单基本类
    '''
    # 2017 0808 10 11 30+用户的id
    order_id = models.CharField(max_length=64, primary_key=True, help_text='订单id')
    passport = models.ForeignKey('df_user.Passport', help_text='用户')
    addr = models.ForeignKey('df_user.Address', help_text='收件地址')
    total_count = models.IntegerField(default=1, help_text='商品总数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='商品总额')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='订单运费')
    # 1.货到付款 2.微信支付 3.支付宝支付 4.银行卡支付
    pay_method = models.IntegerField(default=1, help_text='支付方式')
    # 1.待支付 2.待发货　3.待收货 4.待评价 5.已完成
    order_status = models.IntegerField(default=1, help_text='订单状态')

    objects = OrderBasicManager()

    class Meta:
        db_table = 's_order_basic'


class OrderDetailManager(BaseManager):
    '''
    订单详情模型管理类
    '''
    def add_one_detail_info(self, order_id, goods_id, goods_count, goods_price):
        """添加一条订单详情记录"""
        order_detail = self.create_one_object(order_id=order_id, goods_id=goods_id, goods_count=goods_count, goods_price=goods_price)
        return order_detail

    def get_order_detail_info_by_order_id(self, order_id):
        '''查询订单的详情信息'''
        order_detail_list = self.get_object_list(filters={'order_id':order_id})
        return order_detail_list


class OrderDetail(BaseModel):
    '''
    订单详情类
    '''
    order = models.ForeignKey('OrderBasic', help_text='基本订单')
    goods = models.ForeignKey('df_goods.Goods', help_text='商品')
    goods_count = models.IntegerField(default=1, help_text='商品数目')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='商品价格')

    objects = OrderDetailManager()

    class Meta:
        db_table = 's_order_detail'
