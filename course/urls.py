
from django.urls import path , include
from .views import CourseCategoryView, CourseView, CourseDetailView,TeachersView

urlpatterns = [
    path(r'category', CourseCategoryView.as_view()),  # 获取课程分类的接口
    path(r'', CourseView.as_view()),  # 获取课程接口
    # path(r'detail/(?P<id>\d+)', CourseDetailView.as_view()),  # 课程详情接口
    path(r'teachers', TeachersView.as_view()),  # 讲师接口

]
