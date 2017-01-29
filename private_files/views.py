import mimetypes
import os
import posixpath
import re
from urllib.parse import unquote

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotModified
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.views.static import was_modified_since
from django.utils.http import http_date, parse_http_date
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

from private_files.signals import pre_download

if not getattr(settings, 'FILE_PROTECTION_METHOD', False):
    raise ImproperlyConfigured('You need to set FILE_PROTECTION_METHOD in your project settings')


def _handle_basic(request, instance, field_name):
    field_file = getattr(instance, field_name)

    mimetype, encoding = mimetypes.guess_type(field_file.path)
    mimetype = mimetype or 'application/octet-stream'
    statobj = os.stat(field_file.path)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified(content_type=mimetype)
    basename = os.path.basename(field_file.path)
    field_file.open()
    response = HttpResponse(field_file.file.read(), content_type=mimetype)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    response["Content-Length"] = statobj.st_size
    if field_file.attachment:
        response['Content-Disposition'] = 'attachment; filename=%s' % basename
    if encoding:
        response["Content-Encoding"] = encoding
    field_file.close()
    return response


def _handle_nginx(request, instance, field_name):
    field_file = getattr(instance, field_name)
    basename = os.path.basename(field_file.path)
    mimetype, encoding = mimetypes.guess_type(field_file.path)
    mimetype = mimetype or 'application/octet-stream'
    statobj = os.stat(field_file.path)
    response = HttpResponse()
    response['Content-Type'] = mimetype
    if field_file.attachment:
        response['Content-Disposition'] = 'attachment; filename=%s' % basename
    response["X-Accel-Redirect"] = "/%s" % unicode(field_file)
    response['Content-Length'] = statobj.st_size
    return response


def _handle_xsendfile(request, instance, field_name):
    field_file = getattr(instance, field_name)
    basename = os.path.basename(field_file.path)
    mimetype, encoding = mimetypes.guess_type(field_file.path)
    mimetype = mimetype or 'application/octet-stream'
    statobj = os.stat(field_file.path)
    response = HttpResponse()
    response['Content-Type'] = mimetype
    if field_file.attachment:
        response['Content-Disposition'] = 'attachment; filename=%s' % basename
    response["X-Sendfile"] = field_file.path
    response['Content-Length'] = statobj.st_size
    return response


METHODS = {
    'basic': _handle_basic,
    'nginx': _handle_nginx,
    'xsendfile': _handle_xsendfile
}

try:
    METHOD = METHODS[settings.FILE_PROTECTION_METHOD]
except KeyError:
    raise ImproperlyConfigured(
        'FILE_PROTECTION_METHOD in your project settings needs to be set to one of %s' % (METHODS.keys()))


def get_file(request, app_label, model_name, field_name, object_id, filename):
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
        return METHOD(request, instance, field_name)
    else:
        raise PermissionDenied()
