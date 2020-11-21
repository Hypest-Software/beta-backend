from django.urls import include, path

urlpatterns = [
    path('account/', include('beta_apis.account.urls')),
    path('report/', include('beta_apis.report.urls'))
]
