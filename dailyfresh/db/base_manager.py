# 定义抽象模型管理器基类
from django.db import models
import copy


class BaseManager(models.Manager):
    '''抽象模型管理器基类'''
    def get_all_valid_fields(self):
        '''获取self所在模型类的有效属性的字符串列表'''
        # self所在的模型类
        model_class = self.model
        # 获取models_class的属性元组
        attr_tuple = model_class._meta.get_fields()
        attr_str_list = []
        for attr in attr_tuple:
            if isinstance(attr, models.ForeignKey):
                attr_name = '%s_id'%attr.name
            else:
                attr_name = attr.name
            attr_str_list.append(attr_name)
        return attr_str_list

    def get_one_object(self, **filters):
        '''根据filets查询信息'''
        # {'username':username, 'password':password}
        try:
            # self.get(username=username, password=password)
            obj = self.get(**filters)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def create_one_object(self, **kwargs):
        '''创建一个self所在模型类的对象，并添加到数据库中'''
        # 获取self所在模型类的有效属性的列表
        valid_fields = self.get_all_valid_fields()
        # 拷贝kwargs
        kws = copy.copy(kwargs)
        # 去除kwargs字典中不在valid_fields中的元素
        for key in kws:
            if key not in valid_fields:
                kwargs.pop(key)
        # 获取self所在的模型类
        model_class = self.model
        # 创建一个model_class类对象
        obj = model_class(**kwargs)
        # 添加进数据库
        obj.save()
        # 返回obj
        return obj
    # filters = {'goods_type_id':goods_type_id, order_by=order_by)
    def get_object_list(self, filters={}, order_by=('-pk',)):
        '''根据条件获取查询集并排序'''
        # self.filter(goods_type_id=goods_type_id).order('-pk',)
        object_list = self.filter(**filters).order_by(*order_by)
        return object_list