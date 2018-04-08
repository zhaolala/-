from django.conf.urls import url
from df_user import views

urlpatterns = [
    url('^register/$', views.register), # 显示注册页面
    # url(r'^register_handle/$', views.register_handle), # 实现用户信息的注册
    url(r'^check_user_exist/$', views.check_user_exist), # 校验用户名是否存在

    url(r'^login/$', views.login), # 显示登录页面
    url(r'^login_check/$', views.login_check), # 用户登录校验
    url(r'^logout/$', views.logout), # 退出用户登录

    url(r'^$', views.user), # 用户中心-信息页
    url(r'^address/$', views.address), # 用户中心-地址页
    url(r'^order/$', views.order), # 用户中心-订单页
]
