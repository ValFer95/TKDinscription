from django.db import models
from inscription.models import Famille
from cotisation.models import Saison

# Create your models here.
class MailingRelance(models.Model):
    famille = models.ForeignKey('inscription.Famille', on_delete=models.CASCADE)
    saison = models.ForeignKey('cotisation.Saison', on_delete=models.CASCADE)
    nature_relance = models.CharField(max_length=20, verbose_name="Nature mail relance")
    date_crea = models.DateTimeField(auto_now_add=True)
    date_last_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - saison {} - {} '.format(self.famille, self.saison, self.nature_relance)