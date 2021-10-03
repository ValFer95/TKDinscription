from django.db import models
from inscription.models import Adherent, Saison, Famille

class CommandesDobok(models.Model):
    STATUT_COMMANDE = (
        ('1', 'En cours'),
        ('2', 'Distribuée'),
        ('3', 'Annulée'),
    )

    STAUT_PAIEMENT = (
        ('0', 'Non réglé'),
        ('1', 'Réglé'),
    )

    famille = models.ForeignKey('inscription.Famille', on_delete=models.CASCADE)
    adherent = models.ForeignKey('inscription.Adherent', on_delete=models.CASCADE)
    taille = models.IntegerField(verbose_name="Taille (cm)")
    saison = models.ForeignKey('cotisation.Saison', on_delete=models.CASCADE)
    statut_commande = models.CharField(max_length=1, default=1, choices=STATUT_COMMANDE, verbose_name="Commande")
    tarif_info = models.CharField(max_length=12, verbose_name="Tarif informatif (€)")
    date_distribution = models.DateField(blank=True, null=True, verbose_name="Date distribution")
    statut_paiement = models.CharField(max_length=1, choices=STAUT_PAIEMENT, blank=True, null=True, default=0, verbose_name="Réglement")
    montant_reel = models.IntegerField(blank=True, null=True, verbose_name="Montant réglé")

    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} saison {} - {} '.format(self.adherent, self.saison, self.statut_paiement)


class PrixDobok(models.Model):

    taille_min = models.IntegerField(verbose_name="Taille mini en cm")
    taille_max = models.IntegerField(verbose_name="Taille maxi en cm")
    prix = models.IntegerField(verbose_name="Prix")

    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.prix)