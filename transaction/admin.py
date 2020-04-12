from django.contrib import admin
from transaction.models import *

class TransactionGroupAdmin(admin.ModelAdmin):
    list_display=('name','session','created_on')

class TransactionAdmin(admin.ModelAdmin):
    list_display=('sessionName','group','payer_name','payer_phone','amount')

admin.site.register(TransactionGroup,TransactionGroupAdmin)
admin.site.register(Transaction,TransactionAdmin)
