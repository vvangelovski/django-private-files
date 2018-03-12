import mimetypes
import os

import six
from django.http import HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.views.static import was_modified_since


def basic(request, instance, field_name):
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


def x_accel_redirect(request, instance, field_name):
    field_file = getattr(instance, field_name)
    basename = os.path.basename(field_file.path)
    mimetype, encoding = mimetypes.guess_type(field_file.path)
    mimetype = mimetype or 'application/octet-stream'
    statobj = os.stat(field_file.path)
    response = HttpResponse()
    response['Content-Type'] = mimetype
    if field_file.attachment:
        response['Content-Disposition'] = 'attachment; filename=%s' % basename
    response["X-Accel-Redirect"] = "/%s" % six.text_type(field_file)
    response['Content-Length'] = statobj.st_size
    return response


def x_sendfile(request, instance, field_name):
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