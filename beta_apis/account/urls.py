from django.urls import include, path
from .views import UserRegisterAPIView

urlpatterns = [
    path('register', UserRegisterAPIView.as_view()),
]
