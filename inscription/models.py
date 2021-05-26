from django.db import models
from django.core.validators import MinValueValidator
from cotisation.models import Saison, Categorie, Discipline


class Adherent(models.Model):
    SEXE_CHOICES = (
        ('F', 'Féminin'),
        ('M', 'Masculin'),
    )

    nom_adh = models.CharField(max_length=50, verbose_name="Nom adhérent")
    prenom_adh = models.CharField(max_length=50, verbose_name="Prénom adhérent")
    ddn = models.DateField(verbose_name="Date de naissance")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    adresse = models.CharField(max_length=100)
    cp = models.CharField(max_length=5, verbose_name="Code postal")
    ville = models.CharField(max_length=35)
    nationalite = models.CharField(max_length=40, verbose_name="Nationalité")
    numtel_adh = models.CharField(max_length=10, blank=True, null=True, verbose_name="Numéro téléphone")
    #numtel_adh2 = models.RegexField(regex=r'^\+?1?\d{9,15}$', error_message=("nope"))
    email_adh = models.EmailField(max_length=200, blank=True, null=True, verbose_name="E-mail adhérent")
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, blank=True, null=True)
    famille = models.ForeignKey('Famille', on_delete=models.CASCADE, blank=True, null=True)
    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} '.format(self.nom_adh, self.prenom_adh)


class Grade(models.Model):
    couleur = models.CharField(max_length=20)
    keup = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.couleur


class CategorieCombat(models.Model):
    nom_catg_combat = models.CharField(max_length=50, verbose_name="Catégorie combat")
    annee_debut = models.IntegerField(validators=[MinValueValidator(2021)], verbose_name="Année validité catégorie combat")

    def __str__(self):
        return self.nom_catg_combat


class Contact(models.Model):
    nom_contact = models.CharField(max_length=50, verbose_name="Nom contact")
    prenom_contact = models.CharField(max_length=50, verbose_name="Prénom contact")
    numtel_contact1 = models.CharField(max_length=10, verbose_name="Numéro téléphone 1")
    numtel_contact2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="Numéro téléphone 2")
    numtel_contact3 = models.CharField(max_length=10, blank=True, null=True, verbose_name="Numéro téléphone 3")
    email_contact = models.EmailField(max_length=200, verbose_name="E-mail contact")
    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} '.format(self.nom_contact, self.prenom_contact)


class Famille(models.Model):
    nom_famille = models.CharField(max_length=80, verbose_name="Nom de la famille")
    date_crea = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_famille


class Adherent_Saison(models.Model):
    CERTIF_MED_CHOICES = (
        ('0', 'Non'),
        ('1', 'Oui'),
    )
    PHOTO_CHOICES = (
        ('0', 'Fournie'),
        ('1', 'Non fournie'),
    )

    certif_med = models.CharField(max_length=1, choices=CERTIF_MED_CHOICES, default=0, verbose_name="Certificat médical")
    photo = models.CharField(max_length=1, choices=PHOTO_CHOICES, default=0)
    adherent = models.ForeignKey('Adherent', on_delete=models.CASCADE)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    categorie_combat = models.ForeignKey('CategorieCombat', on_delete=models.CASCADE)
    saison = models.ForeignKey('cotisation.Saison', on_delete=models.CASCADE)
    discipline = models.ForeignKey('cotisation.Discipline', on_delete=models.CASCADE)
    categorie = models.ForeignKey('cotisation.Categorie', on_delete=models.CASCADE)
    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} - {} - sasion {} '.format(self.adherent, self.grade, self.discipline, self.saison)