from rest_framework import serializers
from . import models


# 课程分类
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


# 课程
class CourseSerializer(serializers.ModelSerializer):
    # level字段是选择的，需要指定source，才会返回汉字
    level = serializers.CharField(source="get_level_display")
    price = serializers.SerializerMethodField()

    # 后端拼接路径返回，如果前端拼接就不需要
    course_img = serializers.SerializerMethodField()

    def get_course_img(self, obj):
        return "http://127.0.0.1:8001/media/" + str(obj.course_img)

    def get_price(self, obj):
        # price_policy = GenericRelation("PricePolicy")
        # 拿到PricePolicy表里所有的，通过price排序，拿到第一个，返回它的价格
        price_policy_obj = obj.price_policy.all().order_by("price").first()
        return price_policy_obj.price

    class Meta:
        model = models.Course
        fields = ["id", "title", "course_img", "brief", "level", "study_num", "is_free", "price"]


# 课程详情
class CourseDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()  # 和course是一对一的关系
    level = serializers.SerializerMethodField()  # choise字段
    study_num = serializers.SerializerMethodField()
    recommend_courses = serializers.SerializerMethodField()  # 多对多的关系
    teachers = serializers.SerializerMethodField()  # 多对多的关系
    outline = serializers.SerializerMethodField()
    price_policy = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.course.title

    def get_level(self, obj):
        return obj.course.get_level_display()

    def get_study_num(self, obj):
        return obj.course.study_num

    def get_recommend_courses(self, obj):  # 多对多的关系
        return [{"id": item.id, "title": item.title} for item in obj.recommend_courses.all()]

    def get_teachers(self, obj):  # 多对多的关系
        return [{"id": teacher.id, "name": teacher.name, "breif": teacher.brief} for teacher in obj.teachers.all()]

    # 课程详情和课程大纲是一对多的关系，在课程大纲里写了个反向查询
    # course_detail = models.ForeignKey(to="CourseDetail", related_name="course_outline")
    # 通过反向查询就可以查询到
    def get_outline(self, obj):
        return [{"id": item.id, "title": item.title, "content": item.content} for item in
                obj.course_outline.all().order_by("order")]

    def get_price_policy(self, obj):  # content-type查询
        return [{"id": item.id, "valid_period": item.get_valid_period_display(), "price": item.price} for item in
                obj.course.price_policy.all().order_by("price")]

    class Meta:
        model = models.CourseDetail
        exclude = ["course"]


# 讲师
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = "__all__"
