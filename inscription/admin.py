from django.contrib import admin
from inscription.models import Adherent, Contact, Famille, Grade, CategorieCombat, Adherent_Saison

@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ('nom_adh', 'prenom_adh','ddn', 'sexe', 'adresse', 'cp', 'ville', 'nationalite', 'numtel_adh',
                    'email_adh', 'date_crea', 'date_last_modif')
    ordering = ('nom_adh', 'prenom_adh')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('couleur', 'grade', 'barette', 'keup')
    list_editable = ('keup',)
    ordering = ('-keup', 'couleur', 'grade')


@admin.register(CategorieCombat)
class CategorieCombatAdmin(admin.ModelAdmin):
    list_display = ('nom_catg_combat', 'annee_debut')
