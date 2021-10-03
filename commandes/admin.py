from django.contrib import admin
from commandes.models import CommandesDobok, PrixDobok

@admin.register(CommandesDobok)
class CommandesDobokAdmin(admin.ModelAdmin):
    list_display = ('adherent', 'taille', 'tarif_info', 'statut_commande', 'date_distribution', 'statut_paiement', 'montant_reel',
                    'date_crea', 'date_last_modif')
    ordering = ('adherent',)
    list_editable = ('statut_commande', 'date_distribution', 'statut_paiement', 'montant_reel',)
    list_filter = (
        ('saison',  admin.RelatedOnlyFieldListFilter),
        'statut_commande',
        ('adherent', admin.RelatedOnlyFieldListFilter),
        'statut_paiement',
    )


@admin.register(PrixDobok)
class PrixDobokAdmin(admin.ModelAdmin):
    list_display = ('taille_min', 'taille_max', 'prix', 'date_crea', 'date_last_modif')
    ordering = ('taille_min',)