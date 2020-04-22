from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.authentication import MyAuth
from utils.redis_pool import POOL
import redis
from utils.base_response import BaseResponse
from course import models
import json

# Create your views here.
SHOPPING_CAR_KEY = "shopping_car_%s_%s"
REDIS_CONN = redis.Redis(connection_pool=POOL)


# shopping_car_ %s_ %s: {
#     id: 1,
#     title: CMDB,
#     course_img: xxxxx,
#     price_policy_dict: {
#         1: {有效期1个月， 99}
#
#       }，
#     default_price_policy_id: 3
#
# }


class ShoppingCarView(APIView):
    """
    1030 加入购物车失败
    """
    authentication_classes = [MyAuth, ]

    def post(self, request):
        res = BaseResponse()
        try:
            # 1 获取前端传过来的course_id 以及price_policy_id user_id
            course_id = request.data.get("course_id", "")
            price_policy_id = request.data.get("price_policy_id", "")
            user_id = request.user.id
            # 2 验证数据的合法性
            # 2.1 验证course_id是否合法
            course_obj = models.Course.objects.filter(id=course_id).first()
            if not course_obj:
                res.code = 1031
                res.error = "课程不存在"
                return Response(res.dict)
            # 2.2 验证价格策略是否合法
            # 该课程的所有价格策略对象
            price_policy_queryset = course_obj.price_policy.all()
            # 循环获得每个价格策略的详细信息
            price_policy_dict = {}
            for price_policy_obj in price_policy_queryset:
                price_policy_dict[price_policy_obj.id] = {
                    "valid_period_text": price_policy_obj.get_valid_period_display(),
                    "price": price_policy_obj.price
                }
            # 判断价格策略是否在价格策略的字典里
            if price_policy_id not in price_policy_dict:
                res.code = 1032
                res.error = "价格策略不存在"
                return Response(res.dict)
            # 3 构建我们想要的数据结构
            course_info = {
                "id": course_id,
                "title": course_obj.title,
                "course_img": str(course_obj.course_img),
                "price_policy_dict": json.dumps(price_policy_dict, ensure_ascii=False),
                "default_policy_id": price_policy_id
            }
            # 4 写入redis
            # 4.1 先拼接购物车的key
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, course_id)
            # 4.2 写入redis
            REDIS_CONN.hmset(shopping_car_key, course_info)
            res.data = "加入购物车成功"
        except Exception as e:
            print(e)
            res.code = 1030
            res.error = "加入购物车失败"
        return Response(res.dict)

    def get(self, request):
        res = BaseResponse()
        try:
            # 1 取到user_id
            user_id = request.user.id
            # 2 拼接购物车的key
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, "*")
            # shopping_car_1_*
            # shopping_car_1_asdgnlaksdj
            # 3 去redis读取该用户的所有加入购物车的课程
            # 3.1 先去模糊匹配出所有符合要求的key
            all_keys = REDIS_CONN.scan_iter(shopping_car_key)
            print(all_keys)
            # 3.2 循环所有的keys 得到每个可以
            shopping_car_list = []
            for key in all_keys:
                course_info = REDIS_CONN.hgetall(key)
                course_info["price_policy_dict"] = json.loads(course_info["price_policy_dict"])
                shopping_car_list.append(course_info)
            res.data = shopping_car_list
        except Exception as e:
            res.code = 1033
            res.error = "获取购物车失败"
        return Response(res.dict)

    def put(self, request):
        res = BaseResponse()
        try:
            # 1 获取前端传过来的course_id 以及price_policy_id
            course_id = request.data.get("course_id", "")
            price_policy_id = request.data.get("price_policy_id", "")
            user_id = request.user.id
            # 2 校验数据的合法性
            # 2.1 校验course_id是否合法
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, course_id)
            if not REDIS_CONN.exists(shopping_car_key):
                res.code = 1035
                res.error = "课程不存在"
                return Response(res.dict)
            # 2.2 判断价格策略是否合法
            course_info = REDIS_CONN.hgetall(shopping_car_key)
            price_policy_dict = json.loads(course_info["price_policy_dict"])
            if str(price_policy_id) not in price_policy_dict:
                res.code = 1036
                res.error = "所选的价格策略不存在"
                return Response(res.dict)
            # 3 修改redis中的default_policy_id
            course_info["default_policy_id"] = price_policy_id
            # 4 修改信息后写入redis
            REDIS_CONN.hmset(shopping_car_key, course_info)
            res.data = "更新成功"
        except Exception as e:
            res.code = 1034
            res.error = "更新价格策略失败"
        return Response(res.dict)

    def delete(self, request):
        res = BaseResponse()
        try:
            # 获取前端传过来的course_id
            course_id = request.data.get("course_id", "")
            user_id = request.user.id
            # 判断课程id是否合法
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, course_id)
            if not REDIS_CONN.exists(shopping_car_key):
                res.code = 1039
                res.error = "删除的课程不存在"
                return Response(res.dict)
            # 删除redis中的数据
            REDIS_CONN.delete(shopping_car_key)
            res.data = "删除成功"
        except Exception as e:
            res.code = 1037
            res.error = "删除失败"
        return Response(res.dict)







