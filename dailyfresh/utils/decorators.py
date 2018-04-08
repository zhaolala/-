from django.shortcuts import redirect


def login_requird(view_func):
    '''登录判断装饰器'''
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('islogin'):
            # 用户已登录
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录，跳转到登录页
            return redirect('/user/login/')
    return wrapper