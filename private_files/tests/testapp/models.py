from django.contrib.auth import get_user_model
from django.db import models
from private_files.models.fields import PrivateFileField


def is_owner(request, instance):
    try:
        # django < 2.0
        return (not request.user.is_anonymous()) and request.user.is_authenticated and instance.owner.pk == request.user.pk
    except TypeError:
        #django >= 2.0
        return (not request.user.is_anonymous) and request.user.is_authenticated and instance.owner.pk == request.user.pk

# Create your models here.
class Document(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    attachment = PrivateFileField(upload_to='attachments', condition=is_owner)