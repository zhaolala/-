from django.db import models
from db.base_model import BaseModel # 导入抽象模型类
from utils.get_hash import get_hash
# Create your models here.


class PassportManager(models.Manager):
    '''账户模型管理器类'''
    def add_one_passport(self, username, password, email):
        '''添加一个注册用户信息'''
        # 1.获取self对象所在的模型类
        model_class = self.model
        # 2.创建一个model_class类对象
        obj = model_class(username=username, password=get_hash(password), email=email)
        # 3.保存进数据库
        obj.save()
        # 4.返回对象
        return obj

    def get_one_passport(self, username, password=None):
        '''查找账户信息'''

        try:
            if password is None:
                # 根据用户名查找账户信息
                # 获取self所在的模型类
                # model_class = self.model
                # model_class.objects.get()
                obj = self.get(username=username)
            else:
                # 根据用户名和密码查找账户信息
                obj = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            # 查不到信息
            obj = None
        return obj


class Passport(BaseModel):
    '''账户模型类'''
    username = models.CharField(max_length=20, verbose_name='账户名称')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PassportManager() # 自定义模型管理器类对象

    class Meta:
        db_table = 's_user_account'


class AddressManager(models.Manager):
    '''地址模型管理器类'''
    def get_one_address(self, passport_id):
        '''根据用户的passport_id查询其默认收货地址'''
        try:
            addr = self.get(passport_id=passport_id, is_default=True)
        except self.model.DoesNotExist:
            addr = None
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, recipient_phone,
                        zip_code):
        '''添加一个收货地址'''
        addr = self.get_one_address(passport_id=passport_id)
        # 获取self对象所在的模型类
        model_class = self.model
        if addr is None:
            # 没有默认收货地址
            addr = model_class(passport_id=passport_id, recipient_name=recipient_name,
                        recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                        zip_code=zip_code, is_default=True)
        else:
            # 有默认收货地址
            addr = model_class(passport_id=passport_id, recipient_name=recipient_name,
                               recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                               zip_code=zip_code)
        # 保存进数据库
        addr.save()
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
















