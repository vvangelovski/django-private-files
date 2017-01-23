from django.conf.urls import url
from .views import get_file

urlpatterns = (
    url(r'^(.+)/(.+)/(.+)/(.+)/(.+)$', get_file, name='private_files-file'),
)
