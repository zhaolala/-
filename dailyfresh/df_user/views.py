from django.shortcuts import render,redirect
from df_user.models import Passport,Address,BrowseHistory
from df_order.models import OrderBasic
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.core.mail import send_mail # 导入发送邮件函数
from django.conf import settings
from df_user.tasks import send_register_success_mail # 导入任务函数
from utils.decorators import login_requird # 导入登录装饰器具函数
import time
# Create your views here.


# /user/register/
@require_http_methods(['GET', 'POST'])
def register(request):
    '''显示注册页面'''
    if request.method == 'GET':
        # 显示用户注册页面
        return render(request, 'df_user/register.html')
    else:
        # 进行用户注册
        # 1.接收用户的注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2.保存进数据库
        Passport.objects.add_one_passport(username=username, password=password, email=email)
        # 3.celery给用户注册邮箱发邮件
        # 将任务放入任务队列
        send_register_success_mail.delay(username=username, password=password, email=email)
        # 3.跳转到登录页面 /user/login/
        return redirect('/user/login/')


# /user/register_handle/
def register_handle(request):
    '''实现用户注册'''
    # 1.接收用户的注册信息
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    # 2.保存进数据库
    Passport.objects.add_one_passport(username=username, password=password, email=email)
    # 3.给用户注册邮箱发邮件
    # message = '<h1>欢迎您成为天天生鲜注册会员</h1>请记好您的信息:<br/>用户名:'+username+'<br/>密码：'+password
    # send_mail('欢迎信息', '', settings.EMAIL_FROM, [email], html_message=message)
    # time.sleep(5)
    # 将任务放入任务队列
    send_register_success_mail.delay(username=username, password=password, email=email)
    # 3.跳转到登录页面 /user/login/
    return redirect('/user/login/')


# /user/check_user_exist/
@require_GET
def check_user_exist(request):
    '''校验用户名是否存在'''
    # 1.接收用户名
    username = request.GET.get('username')
    # 2.根据username查找账户信息 get_one_passport(username)
    passport = Passport.objects.get_one_passport(username=username)
    # 3.如果查到,返回json {'res':0} 如果查不到，返回json {'res':1}
    if passport:
        # 用户名已存在
        return JsonResponse({'res':0})
    else:
        # 用户名可用
        return JsonResponse({'res':1})


# /user/login/
def login(request):
    '''显示登录页面'''
    # 获取username cookie信息
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'df_user/login.html', {'username':username})


# /user/login_check/
def login_check(request):
    '''进行登录校验'''
    # 1.接收用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 2.根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # 3.如果查到，返回json {'res':1} 如果查不到，返回 {'res':0}
    if passport:
        # 用户名密码正确
        # 获取记录的pre_url_path
        if request.session.has_key('pre_url_path'):
            next = request.session['pre_url_path'] # /user/
            print('next:%s'%next)
        else:
            # 首页地址
            next = '/'
        jres = JsonResponse({'res':1, 'next':next})
        # 判断是否需要记住用户名
        remember = request.POST.get('remember')
        if remember == 'true':
            # 记住用户名
            jres.set_cookie('username', username, max_age=14*24*3600)
        # 记录用户登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        # 记录登录账户id
        request.session['passport_id'] = passport.id
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res':0})


# /user/logout/
def logout(request):
    '''退出用户登录'''
    # 清空用户的登录状态
    request.session.flush()
    # 跳转到首页
    return redirect('/')


# 使用模板文件时，除了代码中给模板文件传递的模板变量之外，
# django本身会把request传递给模板文件
# /user/
@login_requird
def user(request):
    '''显示用户中心－信息页'''
    # 1.获取登录用户的passport_id
    passport_id = request.session.get('passport_id')
    # 2.获取用户的默认收货地址
    addr = Address.objects.get_one_address(passport_id=passport_id)
    # todo:　获取用户的历史浏览记录
    browse_li = BrowseHistory.objects.get_browse_list_by_passport(passport_id=passport_id,limit=5)
    return render(request, 'df_user/user_center_info.html', {'addr':addr, 'page':'user', 'browse_li':browse_li})


# /user/address/
@require_http_methods(['GET','POST'])
@login_requird
def address(request):
    '''用户中心-地址页'''
    # 获取登录账户passport_id
    passport_id = request.session.get('passport_id')
    if request.method == 'GET':
        # 显示地址页面
        # 获取用户默认收货地址
        addr = Address.objects.get_one_address(passport_id=passport_id)
        return render(request, 'df_user/user_center_site.html', {'addr':addr, 'page':'addr'})
    else:
        # 添加用户收货地址
        # 1.获取用户输入的收件地址信息
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')
        # 2.添加进数据库
        Address.objects.add_one_address(passport_id=passport_id, recipient_name=recipient_name,
                                        recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                                        zip_code=zip_code)
        # 3.刷新address页面，重定向
        return redirect('/user/address/') # 访问方式是get


# /user/order/
@login_requird
def order(request):
    '''用户中心-订单页'''
    # 查询用户的订单信息
    passport_id = request.session.get('passport_id')
    order_basic_list = OrderBasic.objects.get_order_basic_info_by_passport(passport_id=passport_id)
    # todo: 分页

    # todo: 控制页码列表
    # 1.如果总页数<=5
    # 2.如果当前页是前3页
    # 3.如果当前页是后3页,
    # 4.既不是前3页，也不是后3页

    return render(request, 'df_user/user_center_order.html', {'page': 'order','order_basic_list':order_basic_list})