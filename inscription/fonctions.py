from random import choice, randrange
from cotisation.fonctions import tarif_calcul, reduc_une_personne, reduc_famille, appliq_reduc
from datetime import date
from django.core.mail import send_mail

suffixe = ['&', '#', '@', '*', '-', '$', '%']

# CREATION D'UN CODE FAMILLE QUI SERA LA CLEF DE GROUPEMENT DES ADHERENTS D'UNE MEME FAMILLE
def crea_code_famille(nom_adh):
    code_famille = nom_adh + choice(suffixe) + str(randrange(1,99))
    return code_famille


# CALCUL DE LA COTISATION ANNUELLE POUR L'ADHERENT
def calcul_cotis_adh(code_tarif, saison, reinscription):
    tarif = tarif_calcul(code_tarif, saison, reinscription)
    taux_reduc = reduc_une_personne(reinscription, saison)
    cotis_annuelle = appliq_reduc(taux_reduc, tarif)

    # print("dans la fonction, tarif :", tarif)
    # print("dans la fonction, taux_reduc :", taux_reduc)

    return cotis_annuelle

def calcul_age_adh(ddn):
    ddn_split = ddn.split('/')
    age_adherent = int((date.today().year + 1)) - int(ddn_split[2])
    return age_adherent


def envoi_mail(name, email):
    message = "MUDO inscription"
    send_mail(
        'Confirmation inscription taekwondo MUDO club argenteuil', # objet du mail
        message, # message
        'sender@mudo.net', # from email (envoyeur)
        [email], # to mail (destinataire)
    )
    return 'ok'