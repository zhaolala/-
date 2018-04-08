from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from utils.decorators import login_requird
from df_cart.models import Cart
# Create your views here.


# /cart/add/?goods_id=商品id&goods_count=商品数目
@require_GET
@login_requird
def cart_add(request):
    '''添加商品到购物车'''
    # 1.获取商品的id和商品数目
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    # 2.添加商品的购物车
    res = Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id,
                                   goods_count=int(goods_count))
    # 3.判断res返回json数据
    if res:
        # 添加成功
        return JsonResponse({'res':1})
    else:
        # 库存不足
        return JsonResponse({'res':0})


@require_GET
@login_requird
def cart_count(request):
    '''获取用户购物车中商品的总数'''
    # 1.获取登录账户的id
    passport_id = request.session.get('passport_id')
    # 2.根据passport_id查询用户购物车商品总数
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    # 3.返回json数据
    return JsonResponse({'res':res})

# /cart/
@login_requird
def cart_show(request):
    '''显示购物车页面'''
    passport_id = request.session.get('passport_id')
    # 1.获取用户购物车信息 get_cart_list_by_passport(self, passport_id)
    cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
    return render(request, 'df_cart/cart.html', {'cart_list':cart_list})


@require_GET
@login_requird
def cart_update(request):
    '''更新购物车信息'''
    # 1.接收goods_id和goods_count
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    # 2.更新购物车中商品的信息
    res = Cart.objects.update_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=int(goods_count))
    # 3.判断res并返回json数据
    if res:
        # 更新成功
        return JsonResponse({'res':1})
    else:
        # 更新失败
        return JsonResponse({'res':0})

# /cart/del/?goods_id=goods_id
@require_GET
@login_requird
def cart_del(request):
    '''删除购物车信息'''
    # 1.获取商品id
    goods_id = request.GET.get('goods_id')
    passport_id = request.session.get('passport_id')
    # 2.删除购物车信息记录 del_cart_info(self, passport_id, goods_id)
    res = Cart.objects.del_cart_info(passport_id=passport_id, goods_id=goods_id)
    # 3.判断res返回json数据
    if res:
        # 删除成功
        return JsonResponse({'res':1})
    else:
        # 删除失败
        return JsonResponse({'res':0})














