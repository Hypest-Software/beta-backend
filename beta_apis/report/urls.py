from django.urls import include, path
from .views import SendReportAPIView, UploadPhotoAPIView

urlpatterns = [
    path('send/', SendReportAPIView.as_view()),
#    path('get-my-report/', ###),
#    path('get-all-report/', ###),
    path('upload-photo/', UploadPhotoAPIView.as_view()),
]
