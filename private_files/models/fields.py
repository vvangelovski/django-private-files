import os
import uuid
from django.db.models.fields.files import FileField, ImageField, ImageFieldFile, FieldFile
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy


PROTECTION_METHODS = ['basic', 'nginx', 'lighttpd', 'apache']


class PrivateFieldFile(FieldFile):
    def _get_url(self):
        self._require_file()
        app_label = self.instance._meta.app_label
        model_name = self.instance._meta.object_name.lower()
        field_name = self.field.name
        pk = self.instance.pk
        filename = os.path.basename(self.path)
        url = reverse_lazy('private_files-file', args=[app_label, model_name, field_name, pk, filename])
        if self.field.single_use:
            from django.core.cache import cache
            access_key = uuid.uuid4().hex
            cache.set(access_key, '%s-%s-%s-%s-%s' % (app_label, model_name, field_name, pk, filename), 3600)
            url += '?access-key=' + access_key
        return url

    url = property(_get_url)

    def _get_contidion(self):
        return self.field.condition
    condition = property(_get_contidion)

    def _get_attachment(self):
        return self.field.attachment
    attachment = property(_get_attachment)

    def _get_single_use(self):
        return self.field.single_use
    single_use = property(_get_single_use)


def is_user_authenticated(request, instance):
    return (not request.user.is_anonymous()) and request.user.is_authenticated


class PrivateFileField(FileField):
    attr_class = PrivateFieldFile

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, condition=is_user_authenticated,
                 attachment=True, single_use=False, **kwargs):
        super(PrivateFileField, self).__init__(verbose_name, name, upload_to, storage, **kwargs)
        self.condition = condition
        self.attachment = attachment
        self.single_use = single_use
