from django.conf.urls import url, include

urlpatterns = [
    url(r'^private_files/', include('private_files.urls')),
]
