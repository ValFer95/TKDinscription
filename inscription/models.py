from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from cotisation.models import Saison, Categorie, Discipline


class Adherent(models.Model):
    SEXE_CHOICES = (
        ('F', 'Féminin'),
        ('M', 'Masculin'),
    )

    ETUDIANT_CHOICES = (
        ('0', 'Non'),
        ('1', 'Oui'),
    )

    nom_adh = models.CharField(max_length=50, verbose_name="Nom adhérent")
    prenom_adh = models.CharField(max_length=50, verbose_name="Prénom adhérent")
    ddn = models.DateField(verbose_name="Date de naissance")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    taille = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(210)], blank=True, null=True,
                                 verbose_name="Taille en cm")
    etudiant = models.CharField(max_length=1, choices=ETUDIANT_CHOICES)
    adresse = models.CharField(max_length=100)
    cp = models.CharField(max_length=5, verbose_name="Code postal")
    ville = models.CharField(max_length=35)
    nationalite = models.CharField(max_length=40, verbose_name="Nationalité")
    numtel_adh = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator("[0-9]{10}",
                                                message="Saisissez un numéro de téléphone valide.")],verbose_name="Numéro téléphone")
    email_adh = models.EmailField(max_length=200, blank=True, null=True, verbose_name="E-mail adhérent")
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    famille = models.ForeignKey('Famille', on_delete=models.CASCADE)
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
    age_min = models.IntegerField(verbose_name="âge minimum", blank=True, null=True)
    age_max = models.IntegerField(verbose_name="âge maximum", blank=True, null=True)
    annee_debut = models.IntegerField(validators=[MinValueValidator(2021)], verbose_name="Année validité catégorie combat")

    def __str__(self):
        return '{} - de {} à {}'.format(self.nom_catg_combat, self.age_min, self.age_max)


class Contact(models.Model):
    nom_contact = models.CharField(max_length=50, verbose_name="Nom contact")
    prenom_contact = models.CharField(max_length=50, verbose_name="Prénom contact")
    numtel_contact1 = models.CharField(max_length=10, validators=[RegexValidator("[0-9]{10}",
                                message="Saisissez un numéro de téléphone valide pour le contact principal.")], verbose_name="Numéro téléphone 1")
    numtel_contact2 = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator("[0-9]{10}",
                                message="Saisissez un numéro de téléphone valide pour le contact 2.")], verbose_name="Numéro téléphone 2")
    numtel_contact3 = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator("[0-9]{10}",
                                message="Saisissez un numéro de téléphone valide pour le contact 3.")], verbose_name="Numéro téléphone 3")
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
        ('0', 'Non Fourni'),
        ('1', 'Fourni'),
    )
    PHOTO_CHOICES = (
        ('0', 'Non Fournie'),
        ('1', 'Fournie'),
    )

    certif_med = models.CharField(max_length=1, choices=CERTIF_MED_CHOICES, default=0, verbose_name="Certificat médical")
    photo = models.CharField(max_length=1, choices=PHOTO_CHOICES, default=0)
    adherent = models.ForeignKey('Adherent', on_delete=models.CASCADE)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, blank=True, null=True)
    categorie_combat = models.ForeignKey('CategorieCombat', on_delete=models.CASCADE)
    saison = models.ForeignKey('cotisation.Saison', on_delete=models.CASCADE)
    discipline = models.ForeignKey('cotisation.Discipline', on_delete=models.CASCADE)
    categorie = models.ForeignKey('cotisation.Categorie', on_delete=models.CASCADE)
    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} - {} - sasion {} '.format(self.adherent, self.grade, self.discipline, self.saison)


class Paiement(models.Model):
    PAYE_CHOICES = (
        ('0', 'Non'),
        ('1', 'Partiellement'),
        ('2', 'Oui'),
    )

    famille = models.ForeignKey('Famille', on_delete=models.CASCADE)
    montant_cotis = models.IntegerField(default=0, verbose_name="Montant cotisation")
    saison = models.ForeignKey('cotisation.Saison', on_delete=models.CASCADE)
    paye = models.CharField(max_length=1, choices=PAYE_CHOICES, default=0, verbose_name="Cotisation réglée")

    def __str__(self):
        return '{} saison {} - {}€ - {} '.format(self.famille, self.saison, self.montant_cotis, self.paye)


class HistoriquePaiement(models.Model):
    TYPE_RGLT_CHOICES = (
        ('C', 'Chèque'),
        ('L', 'Liquide'),
        ('V', 'Virement'),
    )

    ENCAISSE_CHOICES = (
        ('0', 'Non'),
        ('1', 'Oui'),
    )

    famille = models.ForeignKey('Famille', on_delete=models.CASCADE)
    saison = models.ForeignKey('cotisation.Saison', on_delete=models.CASCADE)
    montant_regle = models.IntegerField(default=0, verbose_name="Montant réglé")
    type_rglmt = models.CharField(max_length=1, blank=True, null=True,
                                  choices=TYPE_RGLT_CHOICES, verbose_name="Type règlement")
    date_recept_rglmt = models.DateField(blank=True, null=True, verbose_name="Date réception")
    proprio_chq = models.CharField(max_length=50, blank=True, null=True, verbose_name="Propriétaire du chèque")
    num_chq = models.CharField(max_length=7, blank=True, null=True, verbose_name="Numéro du chèque")
    bank_chq = models.CharField(max_length=20, blank=True, null=True, verbose_name="Banque")
    date_encaissement = models.DateField(blank=True, null=True, verbose_name="Date encaissement")
    date_depot_bank = models.DateField(blank=True, null=True, verbose_name="Date dépôt à banque")
    encaisse = models.CharField(max_length=1, blank=True, null=True,
                                  choices=ENCAISSE_CHOICES, verbose_name="Chèque encaissé")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="Commentaire")
    date_saisie = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Date saisie")

    def __str__(self):
        return '{} saison {} - {}€ par {} le {} '.format(self.famille, self.saison, self.montant_regle,
                                                         self.type_rglmt, self.date_saisie)