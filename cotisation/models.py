from django.db import models
from django.core.validators import MinValueValidator

class Saison(models.Model):
    saison = models.CharField(max_length=12, verbose_name="Saison")
    saison_actuelle = models.BooleanField(default=False)
    saison_prochaine = models.BooleanField(default=False)

    def __str__(self):
        return self.saison


class Categorie(models.Model):
    nom_catg = models.CharField(max_length=15, verbose_name="Catégorie")
    code_catg = models.CharField(max_length=6, verbose_name="Code catégorie")
    age_inf_catg = models.IntegerField(validators=[MinValueValidator(3)], verbose_name="Age plancher")
    age_sup_catg = models.IntegerField(verbose_name="Age plafond",blank=True, null=True)
    etudiant = models.BooleanField(default=0)
    ordre_affichage = models.IntegerField(blank=True, verbose_name="Ordre d'affichage")
    saison = models.ForeignKey('Saison', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} à {} ans '.format(self.nom_catg, self.age_inf_catg, self.age_sup_catg)


class Discipline(models.Model):
    nom_discipl = models.CharField(max_length=20, verbose_name="Discipline")
    code_discipl = models.CharField(max_length=10, verbose_name="Code discipline")
    ordre_affichage = models.IntegerField(blank=True, verbose_name="Ordre d'affichage")
    saison = models.ForeignKey('Saison', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_discipl


class Tarif(models.Model):
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)
    code_tarif = models.CharField(max_length=20, verbose_name="Code Tarification")
    saison = models.ForeignKey('Saison', on_delete=models.CASCADE)
    tarif_nouveau = models.IntegerField(blank=True, null=True, verbose_name="Tarif nouvel adhérent")
    tarif_ancien = models.IntegerField(blank=True, null=True, verbose_name="Tarif ancien adhérent")

    def __str__(self):
        return '{} - {} - saison {}: tarif nouvel adhérent {} / tarif ancien adhérent {}'.format(self.categorie, self.discipline, self.saison, self.tarif_nouveau, self.tarif_ancien)


class MotifReduction(models.Model):
    motif_reduct = models.CharField(max_length=50, verbose_name="Motif réduction")

    def __str__(self):
        return self.motif_reduct


class TauxReduction(models.Model):
    nom_reduct = models.CharField(max_length=50, verbose_name="Nom réduction", blank=True, null=True)
    motif_reduct = models.ForeignKey('MotifReduction', verbose_name="Motif réduction", on_delete=models.CASCADE, blank=True, null=True)
    condition_reduc = models.CharField(max_length=12, verbose_name="Conditions à remplir", blank=True, null=True)
    condition_anciens = models.BooleanField(verbose_name="Applicable aux anciens adhérents", default=False)
    condition_nouveaux = models.BooleanField(verbose_name="Applicable aux nouveaux adhérents", default=False)
    pourcentage_reduc = models.IntegerField(verbose_name="Réduction en %")
    saison = models.ForeignKey('Saison', on_delete=models.CASCADE)

    def __str__(self):
        return ' - {}% pour {} - saison {}'.format(self.pourcentage_reduc, self.nom_reduct, self.saison)

