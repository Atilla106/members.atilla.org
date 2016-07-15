from django.conf.urls import include, url

app_name = "accounts"
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
]
