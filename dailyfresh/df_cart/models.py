from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseManager
from df_goods.models import Goods
from django.db.models import Sum # 导入Sum聚合类
# Create your models here.


class CartManager(BaseManager):
    '''购物车模型管理器类'''
    def get_one_cart_info(self, passport_id, goods_id):
        '''查询一条购物车信息'''
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        '''添加一条购物车记录'''
        # 查询用户购物中是否添加过该商品
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        if cart_info:
            # 1.商品已经添加过，更新商品数量
            total_count = cart_info.goods_count + goods_count
            if total_count <= goods.goods_stock:
                cart_info.goods_count = total_count
                cart_info.save()
                return True
            else:
                # 库存不足
                return False
        else:
            # 2.商品没有添加过，创建新记录
            if goods_count <= goods.goods_stock:
                # 库存充足
                cart_info = self.create_one_object(passport_id=passport_id, goods_id=goods_id,
                                               goods_count=goods_count)
                return True
            else:
                # 库存不足
                return False

    def get_cart_count_by_passport(self, passport_id):
        '''根据passport_id查询用户购物车中商品的总数'''
        # select sum(goods_count) from s_cart where passport_id=passport_id
        res_dict = self.filter(passport_id=passport_id).aggregate(Sum('goods_count')) # {'goods_count__sum':结果}
        # {'goods_count__sum':None}
        if res_dict['goods_count__sum'] is None:
            res = 0
        else:
            res = res_dict['goods_count__sum']
        return res

    def get_cart_list_by_passport(self, passport_id):
        '''查询用户购物车记录信息'''
        cart_list = self.get_object_list(filters={'passport_id':passport_id})
        return cart_list

    def update_cart_info(self, passport_id, goods_id, goods_count):
        '''更新购物车记录信息'''
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if goods_count <= cart_info.goods.goods_stock:
            # 库存充足
            cart_info.goods_count = goods_count
            cart_info.save()
            return True
        else:
            # 库存不足
            return False

    def del_cart_info(self, passport_id, goods_id):
        '''删除购物车记录'''
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        try:
            cart_info.delete()
            return True
        except:
            # 删除失败
            return False

    def get_cart_list_by_id_list(self, cart_id_list):
        '''查询购物车记录信息'''
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        # self.filter(id__in = cart_id_list)
        return cart_list

    def get_amount_and_count_by_id_list(self, cart_id_list):
        '''计算商品的总数目和总额'''
        total_count,total_price = 0,0
        cart_list = self.get_object_list(filters={'id__in': cart_id_list})
        # 遍历计算商品的总数目和总价格
        for cart_info in cart_list:
            total_count = total_count + cart_info.goods_count
            total_price = total_price + cart_info.goods_count*cart_info.goods.goods_price
        return total_count,total_price


class Cart(BaseModel):
    '''购物车模型类'''
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户名称')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品名称')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')

    objects = CartManager()

    class Meta:
        db_table = 's_cart'