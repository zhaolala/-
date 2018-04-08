from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^$', views.home_list_page), # 显示首页内容
    url(r'^goods/(?P<goods_id>\d+)/$', views.goods_detail), # 显示商品详情页面
    url(r'^list/(?P<goods_type_id>\d+)/(?P<pindex>\d+)/$', views.goods_list), # 显示商品列表页面
]
