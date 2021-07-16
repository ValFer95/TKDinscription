from django.contrib import admin
from inscription.models import Adherent, Contact, Famille, Grade, CategorieCombat, Adherent_Saison, Paiement, HistoriquePaiement

@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ('nom_adh', 'prenom_adh','ddn', 'sexe', 'taille', 'etudiant', 'adresse', 'cp', 'ville', 'nationalite',
                    'numtel_adh', 'email_adh', 'contact', 'date_crea', 'date_last_modif')
    ordering = ('nom_adh', 'prenom_adh')
    list_filter = ('famille__nom_famille',)


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
    list_display = ('nom_catg_combat', 'age_min', 'age_max', 'annee_debut')
    list_editable = ('age_min', 'age_max')
    ordering = ('age_min', 'nom_catg_combat')


@admin.register(Adherent_Saison)
class Adherent_SaisonAdmin(admin.ModelAdmin):
    list_display = ('adherent', 'saison', 'categorie', 'discipline', 'certif_med', 'photo',
                    'grade', 'categorie_combat', 'date_crea', 'date_last_modif')
    ordering = ('adherent__nom_adh', 'saison')
    list_filter = (
        ('saison',  admin.RelatedOnlyFieldListFilter),
        'adherent__nom_adh',
        'discipline__nom_discipl',
        'grade__couleur',
    )


@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
    list_display = ('nom_famille',)
    ordering = ('nom_famille', )


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('famille', 'saison', 'montant_cotis', 'paye',)
    ordering = ('famille__nom_famille', 'saison' )
    list_filter = ('saison', 'famille__nom_famille', )


@admin.register(HistoriquePaiement)
class HistoriquePaiementAdmin(admin.ModelAdmin):
    list_display = ('famille', 'saison', 'montant_regle', 'type_rglmt', 'date_rglt')
    ordering = ('famille', 'saison', )
