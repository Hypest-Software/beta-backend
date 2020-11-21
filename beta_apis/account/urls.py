from django.urls import include, path
from .views import UserRegisterAPIView, UserLoginAPIView, UserUpdateInfoAPIView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('update-info/', UserUpdateInfoAPIView.as_view())
]
