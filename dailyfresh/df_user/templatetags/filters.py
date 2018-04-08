# 自定过滤器
from django.template import Library

# 创建一个Library类的对象
register = Library()

# 自定义过滤器函数
@register.filter
def order_status(val):
    '''返回订单的状态'''
    status_dict = {1:'未支付', 2:'待发货', 3:'待收货', 4:'待评价', 5:'已完成'}
    return status_dict[val]