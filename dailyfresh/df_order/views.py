from django.shortcuts import render
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.db import transaction
from django.http import JsonResponse
from df_cart.models import Cart
from df_user.models import Address
from df_order.models import OrderBasic, OrderDetail
from datetime import datetime
from utils.decorators import login_requird
# Create your views here.


# /order/place/
@require_POST
@login_requird
def show_place(request):
    '''显示提交订单页面'''
    # 查询用户的默认收货地址
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_one_address(passport_id=passport_id)
    # 获取用户的选中的购物车id的列表
    cart_id_list = request.POST.getlist('cart_id_list')
    # print(cart_id_list)
    # 查询id在cart_id_list这个列表中的购物车记录信息
    cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    # 把cart_id_list转化成字符串　[1,2,3]->1,2,3
    cart_id_list = ','.join(cart_id_list)
    return render(request, 'df_order/place_order.html', {'cart_list':cart_list, 'addr':addr, 'cart_id_list':cart_id_list})

# /order/commit/
@require_POST
@login_requird
@transaction.atomic
def order_commit(request):
    '''生成订单信息'''
    # 1.接收信息
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list') # 1,2,3

    # 2.组织基本订单信息
    passport_id = request.session.get('passport_id')
    # 2.1 生成订单id 格式：20170929094611+passport_id ->2017 09 29 09 49 19 13
    order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(passport_id)
    transit_price = 10.0
    # 2.2 计算用户要购买的商品的总数和总额
    cart_id_list = cart_id_list.split(',')
    total_count,total_price = Cart.objects.get_amount_and_count_by_id_list(cart_id_list=cart_id_list)

    # 3.创建一个保存点
    sid = transaction.savepoint()
    try:
        # 4.生成基本订单记录
        OrderBasic.objects.add_one_basic_info(order_id=order_id, passport_id=passport_id, addr_id=addr_id, pay_method=pay_method, total_count=total_count, total_price=total_price, transit_price=transit_price)
        # 5.生成订单详情记录
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        # 6.遍历生成订单详情记录
        for cart_info in cart_list:
            # 6.1 组织订单详情信息
            goods_id = cart_info.goods_id
            goods_count = cart_info.goods_count
            goods_price = cart_info.goods.goods_price
            # 6.2 判断商品的库存是否充足
            if goods_count <= cart_info.goods.goods_stock:
                # 6.2.1 库存充足，添加一条订单详情记录　
                OrderDetail.objects.add_one_detail_info(order_id=order_id, goods_id=goods_id, goods_count=goods_count, goods_price=goods_price)
                # 6.2.2 更新商品的库存和销量
                cart_info.goods.goods_stock = cart_info.goods.goods_stock - goods_count
                cart_info.goods.goods_sales = cart_info.goods.goods_sales + goods_count
                cart_info.goods.save()
                # 6.2.3 删除购物车记录
                cart_info.delete()
            else:
                # 6.2.4 库存不足,进行回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res':0})
    except:
        # 进行回滚
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res':2})

    # 生成订单成功
    transaction.savepoint_commit(sid)
    return JsonResponse({'res':1})
