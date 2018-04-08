from django.db import models
from db.base_model import BaseModel # 导入抽象模型类
from db.base_manager import BaseManager # 导入抽象模型管理器基类
from utils.get_hash import get_hash
# Create your models here.


class PassportManager(BaseManager):
    '''账户模型管理器类'''
    def add_one_passport(self, username, password, email):
        '''添加一个注册用户信息'''
        obj = self.create_one_object(username=username, password=get_hash(password), email=email)
        # 返回对象
        return obj

    def get_one_passport(self, username, password=None):
        '''查找账户信息'''
        if password is None:
            # 根据用户名查找账户信息
            obj = self.get_one_object(username=username)
        else:
            # 根据用户名和密码查找账户信息
            obj = self.get_one_object(username=username, password=get_hash(password))
        return obj


class Passport(BaseModel):
    '''账户模型类'''
    username = models.CharField(max_length=20, verbose_name='账户名称')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PassportManager() # 自定义模型管理器类对象

    class Meta:
        db_table = 's_user_account'


class AddressManager(BaseManager):
    '''地址模型管理器类'''
    def get_one_address(self, passport_id):
        '''根据用户的passport_id查询其默认收货地址'''
        addr = self.get_one_object(passport_id=passport_id, is_default=True)
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, recipient_phone,
                        zip_code):
        '''添加一个收货地址'''
        addr = self.get_one_address(passport_id=passport_id)
        is_default = False
        if addr is None:
            # 没有默认收货地址
            is_default = True
        addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name,
                                        recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                                        zip_code=zip_code, is_default=is_default)
        # 返回addr
        return addr


class Address(BaseModel):
    '''地址模型类'''
    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    recipient_name = models.CharField(max_length=24, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'


class BrowseHistoryManager(BaseManager):
    '''
    历史浏览模型管理器类
    '''
    def get_one_history(self, passport_id, goods_id):
        '''
        查询用户是否浏览过某个商品
        '''
        # todo: 代码实现
        browsed = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def add_one_history(self, passport_id, goods_id):
        '''
        添加用户的一条浏览记录
        '''
        # 1.去查找用户是否浏览过该商品 self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        browsed = self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        # 2.如果用户浏览过该商品，则更新update_time，否则插入一条新的浏览记录
        if browsed:
            # 调用browsed.save方法会自动更新update_time
            # print('update')
            browsed.save()
        else:
            browsed = self.create_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def get_browse_list_by_passport(self, passport_id, limit=None):
        '''
        根据passport_id获取对应用户的浏览记录
        '''
        # 1.根据用户id获取用户的历史浏览记录,browsed_li为一个查询集
        browsed_li = self.get_object_list(filters={'passport_id':passport_id}, order_by=('-update_time',))
        # 2.对查询结果集进行限制
        if limit:
            browsed_li = browsed_li[:limit]
        return browsed_li


class BrowseHistory(BaseModel):
    '''
    历史浏览模型类
    '''
    # todo: 模型类设计
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')

    objects = BrowseHistoryManager()

    class Meta:
        db_table = 's_browse_history'















