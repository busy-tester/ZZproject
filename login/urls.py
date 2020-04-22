
from django.urls import path , include
from .views import RegisterView, LoginView

urlpatterns = [
    path(r'register', RegisterView.as_view()),
    path(r'login', LoginView.as_view()),

]
