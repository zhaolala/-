from django.shortcuts import render
from django.core.paginator import Paginator
from df_goods.models import Goods,Image
from df_user.models import BrowseHistory
from df_goods.enums import *
# Create your views here.


# http://127.0.0.1:8001/
def home_list_page(request):
    '''显示首页内容'''
    # 查询水果，按照默认排序方式查出4个,新品查出3个
    fruits = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=4)
    fruits_new = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=3, sort='new')
    seafood = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=4)
    seafood_new = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')
    meats = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=4)
    meats_new = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=3, sort='new')
    eggs = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=4)
    eggs_new = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=3, sort='new')
    vegetables = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=4)
    vegetables_new = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')
    frozen = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=4)
    frozen_new = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=3, sort='new')
    # 组织上下文数据
    context = {'fruits':fruits, 'fruits_new':fruits_new,
               'seafood':seafood, 'seafood_new':seafood_new,
               'meats':meats, 'meats_new':meats_new,
               'eggs':eggs, 'eggs_new':eggs_new,
               'vegetables':vegetables, 'vegetables_new':vegetables_new,
               'frozen':frozen, 'frozen_new':frozen_new}
    return render(request, 'df_goods/index.html', context)


# /goods/商品id/
def goods_detail1(request, goods_id):
    '''显示商品的详情页面'''
    # 1.根据商品id查询商品信息
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    # 2.根据商品id查询出一张商品的详情图片
    images = Image.objects.get_image_by_goods_id(goods_id=goods_id)
    # goods = Goods.objects.get_goods_by_id_with_image(goods_id=goods_id)
    # 2.查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 2.使用模板文件detail.html
    return render(request, 'df_goods/detail.html', {'goods': goods,
                                                    'goods_new': goods_new,
                                                    'images':images})


def goods_detail2(request, goods_id):
    # 1.根据商品id查询商品信息
    goods = Goods.objects.get_goods_by_id_with_image(goods_id=goods_id)
    # 2.查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 2.使用模板文件detail.html
    return render(request, 'df_goods/detail.html', {'goods': goods,
                                                    'goods_new': goods_new})


def goods_detail(request, goods_id):
    '''显示商品的详情页面'''
    # 1.根据商品id查询商品信息，包含商品的详情图片信息 goods.img_url
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    # 2.查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 3.获取商品类型标题
    type_title = GOODS_TYPE[goods.goods_type_id]

    # todo: 添加历史浏览记录
    # 如果用户没有登录，不需要记录历史浏览信息
    if request.session.has_key('islogin'):
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=goods_id)

    # 3.使用模板文件detail.html
    return render(request, 'df_goods/detail.html', {'goods':goods,
                                                    'goods_new':goods_new,
                                                    'type_title':type_title})


# /list/类型id/页码/?sort=排序方式
# sort='price' 按照价格排序
# sort='hot' 按照人气进排序
def goods_list(request, goods_type_id, pindex):
    '''显示商品列表页面'''
    # 获取排序方式
    sort = request.GET.get('sort', 'default')
    # 根据商品类型id查询商品信息
    goods_li = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, sort=sort)
    # 2.查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, limit=2, sort='new')
    # 进行分页
    paginator = Paginator(goods_li, 1)
    # 取第pindex页的内容
    pindex = int(pindex)
    goods_li = paginator.page(pindex)
    # todo: 进行页码控制
    # 获取总页数
    num_pages = paginator.num_pages
    '''
    0.如果不足5页,显示全部页码
    1.当前页是前三页,显示1-5页
    2.当前页是后三页,显示后5页
    3.既不是前3页,也不是后3页,显示当前页，当前页前2页，后2页
    '''
    if num_pages < 5:
        pages = range(1, num_pages+1)
    elif pindex <= 3:
        pages = range(1, 6)
    elif num_pages - pindex <= 2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(pindex-2, pindex+3)
    return render(request, 'df_goods/list.html', {'goods_li':goods_li,
                                                  'goods_new':goods_new,
                                                  'type_id':goods_type_id,
                                                  'type_title':GOODS_TYPE[int(goods_type_id)],
                                                  'sort':sort,
                                                  'pages':pages})