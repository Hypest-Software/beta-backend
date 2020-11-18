from django.urls import include, path

urlpatterns = [
    path('account/', include('beta_apis.account.urls')),
]
