from django.contrib import admin
from staff.models import MailingRelance

# Register your models here.
@admin.register(MailingRelance)
class MailingRelanceAdmin(admin.ModelAdmin):
    list_display = ('famille', 'saison', 'nature_relance', 'date_crea', 'date_last_modif',)
    #list_editable = ('',)
    ordering = ('famille',)
    list_filter = ('famille', 'saison',)