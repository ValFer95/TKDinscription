from random import choice, randrange
from cotisation.fonctions import tarif_calcul, reduc_une_personne, reduc_famille, appliq_reduc
from datetime import date
from django.core.mail import send_mail

suffixe = ['&', '#', '@', '*', '-', '$', '%']

# CREATION D'UN CODE FAMILLE QUI SERA LA CLEF DE GROUPEMENT DES ADHERENTS D'UNE MEME FAMILLE
def crea_code_famille(nom_adh):
    code_famille = nom_adh.capitalize() + choice(suffixe) + str(randrange(1,99))
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


def envoi_mail(list_nom, list_discipline, list_cotisation, cotis_adh, code_famille, email):
    message = "Bonjour, \n Votre demande d'inscription au Mudo club Argenteuil pour la saison 2021-2022 est prise en compte : \n \n"
    for i in range(len(list_nom)):
        message += str(i+1) + '- ' + list_nom[i] + ' (' + list_discipline[i] + ') - tarif de :' + list_cotisation[i] + '€\n'

    message += "\n La cotisation annuelle à régler est de " + str(cotis_adh) + "€.\n \n"

    message += "Vous pouvez payer par chèque, virement, liquide en 3 fois.\n"
    message += "Pour terminer l'inscription, merci d'apporter au club une enveloppe portant la mention " + code_famille + " et contenant :\n"
    message += "1- Le moyen de paiement de la cotisation par chèque(s), en liquide ou l'ordre de virement effectué, \n"
    message += "2- Un certificat médical à la pratique du taekwondo pour chaque membre de la famille, \n"
    message += "3- Une photo d'identité pour chaque membre de la famille avec le nom de l'adhérent au dos. \n\n"

    message += "Les chèques seront déposés le 5 de chaque mois en cas de règlement en plusieurs chèques, \n\n"

    message += "Le Mudo Club Argenteuil"

    # print('email:', email)
    # print('message :' + message)

    send_mail(
        'Confirmation inscription taekwondo MUDO Club Argenteuil', # objet du mail
        message, # message
        'mudoclub@tkdinscription.vfeapps.fr', # from email (envoyeur)
        email, # to mail (destinataire),
        fail_silently = False
    )
    return 'ok'


# création de la liste des emails des destinataires du mail de récap des infos d'inscription
def liste_dest_mail(list_email, age_adherent, email_adh, email_contact):

    if list_email != '':
        if age_adherent >= 18 and email_adh:
            list_email = list_email + ',' + email_adh
        else:
            if list_email.count(email_contact) == 0:
                list_email = list_email + ',' + email_contact
    else :
        if age_adherent >= 18 and email_adh:
            list_email = email_adh
        else:
            list_email = email_contact

    return list_email