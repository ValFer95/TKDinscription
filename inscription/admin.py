from django.contrib import admin
from inscription.models import Adherent, Contact, Famille, Grade, CategorieCombat, Adherent_Saison

@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ('nom_adh', 'prenom_adh','ddn', 'sexe', 'adresse', 'cp', 'ville', 'nationalite', 'numtel_adh',
                    'email_adh', 'contact', 'date_crea', 'date_last_modif')
    ordering = ('nom_adh', 'prenom_adh')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom_contact', 'prenom_contact','numtel_contact1', 'numtel_contact2', 'numtel_contact3',
                    'email_contact', 'date_crea', 'date_last_modif')
    ordering = ('nom_contact', 'prenom_contact')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('couleur', 'keup')
    list_editable = ('keup',)
    ordering = ('-keup',)


@admin.register(CategorieCombat)
class CategorieCombatAdmin(admin.ModelAdmin):
    list_display = ('nom_catg_combat', 'annee_debut')
