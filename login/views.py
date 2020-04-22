from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AccountSerializer
from utils.base_response import BaseResponse
from course.models import Account
import uuid


# Create your views here.


# 注册接口
class RegisterView(APIView):
    def post(self, request):
        # 用户注册传用户名和密码，相当于给用户表新增数据
        ser_obj = AccountSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.data)
        return Response(ser_obj.errors)


# 登录接口
class LoginView(APIView):
    def post(self, request):
        ret = BaseResponse()
        # 获取用户名和密码
        username = request.data.get("username", "")
        if not username:
            ret.code = 1010
            ret.error = "用户名不能为空"
        pwd = request.data.get("pwd", "")
        if not pwd:
            ret.code = 1011
            ret.error = "密码不能为空"

        # 判断是否有这个对象
        try:
            user_obj = Account.objects.filter(username=username, pwd=pwd).first()
            if user_obj:
                # 生成token
                user_obj.token = uuid.uuid4()
                user_obj.save()
                ret.data = "登录成功"
                ret.code = 1012
                ret.token = user_obj.token

            else:
                ret.error = "用户名或密码错误"

        except Exception as e:
            ret.code = 1013
            ret.error = "登录失败"
        return Response(ret.dict)
