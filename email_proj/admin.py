from django.contrib import admin
from email_proj.models import E_mail
# Register your models here.

@admin.register(E_mail)
class E_mailAdmin(admin.ModelAdmin):
    list_display = ('text', 'time_stamp', 'time_to_send', 'sent')
