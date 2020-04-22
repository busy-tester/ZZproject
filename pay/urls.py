from django.urls import path
from .views import ShoppingCarView


urlpatterns = [
    path(r'shopping_car', ShoppingCarView.as_view()),

]
