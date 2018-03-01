from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'attachment')
    fields = (
        'title',
        'owner',
        'attachment',
    )

admin.site.register(Document, DocumentAdmin)