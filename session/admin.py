from django.contrib import admin

from session.models import Session, Membership

class SessionAdmin(admin.ModelAdmin):
    list_display=('name','secret_code','created_at')

class MembershipAdmin(admin.ModelAdmin):
    list_display=('sessionName','personName','date_joined')

admin.site.register(Session,SessionAdmin)
admin.site.register(Membership,MembershipAdmin)
