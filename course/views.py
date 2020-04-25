from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
from . import response_data
import uuid


# Create your views here.


# 获取分类的视图
class CourseCategoryView(APIView):
    def get(self, request):
        # 从数据库中拿所有的分类
        queryset = models.Category.objects.all()
        # 序列化所有的分类
        ser_obj = serializers.CategorySerializer(queryset, many=True)
        # 返回序列化好的数据
        return Response(ser_obj.data)


# 获取课表的视图   http://127.0.0.1:8000/api/course/?category_id=1
class CourseView(APIView):
    def get(self, request):

        # 判断token是否正确
        user_token = request.query_params.get('token', uuid.uuid4())
        if user_token != "":
            try:
                is_token = models.Account.objects.filter(token=user_token).first()
                if is_token:
                    # 判断是否有category_id
                    category_id = request.query_params.get("category_id", 0)
                    category_id = int(category_id)  # 0代表全部课程，传过来的是字符串
                    # 获取响应的分类数据
                    if not category_id:
                        queryset = models.Course.objects.all().order_by("order")  # 拿课程表里的所有数据
                    else:
                        # 在课程分类表里通过id查询
                        queryset = models.Course.objects.filter(category_id=category_id).order_by("order")
                    # 序列化数据
                    ser_obj = serializers.CourseSerializer(queryset, many=True)
                    # 返回序列化好的数据
                    return Response(ser_obj.data)
            except Exception as e:

                return Response(response_data.token_error)
        return Response(response_data.token_error)


# 课程详情的视图
class CourseDetailView(APIView):
    def get(self, request, id):
        # 获取这个课程id找到课程详情对象
        # course = models.OneToOneField(to="Course")
        # id是course表的id，但是course表和CourseDetail表是一对一的关系，所以
        # 在CourseDetail表里有个字段course_id

        course_detail_obj = models.CourseDetail.objects.filter(course_id=id).first()
        # 序列化这个课程详情对象
        ser_obj = serializers.CourseDetailSerializer(course_detail_obj)

        # 返回序列化数据
        return Response(ser_obj.data)


# 讲师的视图
class TeachersView(APIView):
    def get(self, request):
        queryset = models.Teacher.objects.all()
        ser_obj = serializers.TeacherSerializer(queryset, many=True)
        return Response(ser_obj.data)

    def post(self, request):
        # 判断token是否正确
        user_token = request.data.get('token', uuid.uuid4())
        if user_token != "":
            try:
                is_token = models.Account.objects.filter(token=user_token).first()

                if is_token:

                    # teacher表新增数据
                    ser_obj = serializers.TeacherSerializer(data=request.data)
                    if ser_obj.is_valid():
                        ser_obj.save()
                        return Response(response_data.teacher_success)
                    else:
                        return Response(ser_obj.errors)
            except Exception as e:
                return Response(response_data.token_error)
        return Response(response_data.token_error)
