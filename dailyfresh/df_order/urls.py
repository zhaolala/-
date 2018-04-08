from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r'^place/$', views.show_place), # 显示提交订单页面
    url(r'^commit/$', views.order_commit), # 订单生成
]
