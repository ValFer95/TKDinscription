from django.contrib import admin
from cotisation.models import Saison, Categorie, Discipline, Tarif, MotifReduction, TauxReduction

admin.site.site_header = "Taekwondo Adhésion"
admin.site.site_url = '/accueil/'

@admin.register(Saison)
class SaisonAdmin(admin.ModelAdmin):
    list_display = ('saison', 'saison_actuelle')
    list_editable = ('saison_actuelle',)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom_catg', 'etudiant', 'age_inf_catg', 'age_sup_catg', 'ordre_affichage','saison')
    list_editable = ('ordre_affichage',)
    ordering = ('ordre_affichage',)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('nom_discipl', 'ordre_affichage','saison')
    list_editable = ('ordre_affichage',)
    ordering = ('ordre_affichage',)


@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('categorie', 'discipline', 'tarif_nouveau', 'tarif_ancien', 'saison', 'code_tarif')
    list_editable = ('tarif_nouveau','tarif_ancien')
    list_filter = ('categorie', 'discipline', 'saison',)
    ordering = ('categorie', 'discipline', 'saison',)
    list_per_page = 20


@admin.register(MotifReduction)
class MotifReductionAdmin(admin.ModelAdmin):
    list_display = ('motif_reduct', )


@admin.register(TauxReduction)
class MotifTauxReductionAdmin(admin.ModelAdmin):
    list_display = ('nom_reduct', 'motif_reduct', 'condition_reduc', 'pourcentage_reduc', 'condition_anciens', 'condition_nouveaux', 'saison')
    list_editable = ('pourcentage_reduc',)
    list_filter = ('nom_reduct', 'saison',)

