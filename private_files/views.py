try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from django.conf import settings
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from private_files.signals import pre_download


try:
    from django.urls.utils import get_callable
except ImportError:
    from django.core.urlresolvers import get_callable


def get_file(request, app_label, model_name, field_name, object_id, filename):
    handler = get_callable(getattr(settings, 'PRIVATE_DOWNLOAD_HANDLER', 'private_files.handlers.basic'))
    model = apps.get_model(app_label, model_name)
    instance = get_object_or_404(model, pk=unquote(object_id))
    condition = getattr(instance, field_name).condition
    single_use = getattr(instance, field_name).single_use
    if single_use:
        value = cache.get(request.GET.get('access-key', 'no-access-key'), None)
        cache.delete(request.GET.get('access-key', 'no-access-key'))
        if value != '%s-%s-%s-%s-%s' % (app_label, model_name, field_name, object_id, filename):
            raise PermissionDenied()
    if not model:
        raise Http404("")
    if not hasattr(instance, field_name):
        raise Http404("")
    if condition(request, instance):
        pre_download.send(sender=model, instance=instance, field_name=field_name, request=request)
        return handler(request, instance, field_name)
    else:
        raise PermissionDenied()
