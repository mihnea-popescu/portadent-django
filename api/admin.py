from django.utils.html import format_html
from django.contrib import admin
from core.image_processing.image import image_to_base64
from PIL import Image
from api.models import Scan, ScanPhoto, ScanProcess, ScanResult, User


class ScanPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'scan', 'type', 'image_preview')
    readonly_fields = ('image_preview', 'file')

    def image_preview(self, obj):
        if obj.file:
            try:
                with obj.file.open('rb') as f:
                    img = Image.open(f)
                    base64_str = image_to_base64(img)
                    return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', base64_str)
            except Exception as e:
                return f"Error displaying image: {e}"
        return "No Image"

    image_preview.short_description = 'Image Preview'


# Register your models here.
admin.site.register(Scan)
admin.site.register(ScanPhoto, ScanPhotoAdmin)
admin.site.register(ScanProcess)
admin.site.register(ScanResult)
admin.site.register(User)
