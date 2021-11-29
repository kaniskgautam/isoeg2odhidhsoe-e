from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = "AKL : KODE - Admin Panel"
admin.site.site_title = "AKL : KODE "


class ImageUrlInline(admin.TabularInline):
    model = ImageUrl


class ProductAdmin(admin.ModelAdmin):

    def change_reviewed_to_false(self, request, queryset):
        queryset.update(reviewed=False)

    list_display = ('title', 'price', 'rating',
                    'category', 'reviewed', 'made_by')
    actions = ('change_reviewed_to_false',)
    inlines = [ImageUrlInline, ]


class MessageAdmin(admin.ModelAdmin):

    def change_responded_to_true(self, request, queryset):
        queryset.update(responded=True)

    list_display = ('subject', 'responded', 'name', 'message', 'email')
    actions = ('change_responded_to_true',)


admin.site.register(Product, ProductAdmin)  # DONE
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Message, MessageAdmin)  # DONE
admin.site.register(ImageUrl)  # DONE
