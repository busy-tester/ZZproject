from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from course.models import Account
from django.utils.timezone import now  # 要用django提供的时间


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'OPTIONS':  #过滤掉options请求
            return None
        # 拿到前端传来的token，请求头的数据都在request.META里
        # 比如前端把token放在请求头里：authenticate：85ada55664sfqq6
        # django会在前面加上 HTTP_ 并转为大写，也就是 HTTP_AUTHENTICATE
        # print(request.META)
        token = request.META.get('HTTP_AUTHENTICATE', '')

        # 判断是否有这个token
        if not token:
            raise AuthenticationFailed({"code": 1020, "error": "没有token"})
        user_obj = Account.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed({"code": 1021, "error": "token不合法"})

        # 判断token是否过期
        old_time = user_obj.create_token_time  # 数据库里存的token的时间
        now_time = now()  # 用django提供获取时间的方法
        if (now_time - old_time).days > 7:
            raise AuthenticationFailed({"code": 1022, "error": "token已过期，请重新登录"})
        return (user_obj, token)
