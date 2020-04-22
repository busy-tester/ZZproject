from rest_framework import serializers
from course.models import Account
import hashlib


# 注册
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["username","pwd"]

    # 前端密码不加密，后端加密
    def create(self, validated_data):
        username = validated_data["username"]
        pwd = validated_data["pwd"]
        hash_pwd = hashlib.md5(pwd.encode()).hexdigest()
        user_obj = Account.objects.create(username=username, pwd=hash_pwd)
        return user_obj