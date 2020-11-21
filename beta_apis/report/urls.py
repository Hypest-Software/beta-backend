from django.urls import include, path
from .views import SendReportAPIView, UploadPhotoAPIView, ListMyReportAPIView, ListAllReportAPIView

urlpatterns = [
    path('send/', SendReportAPIView.as_view()),
    path('get-my-report/', ListMyReportAPIView.as_view()),
    path('get-all-report/', ListAllReportAPIView.as_view()),
    path('upload-photo/', UploadPhotoAPIView.as_view()),
]
