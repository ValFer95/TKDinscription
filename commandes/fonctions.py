from inscription.models import Paiement, Adherent, Famille
from commandes.models import CommandesDobok
from django.core.mail import send_mail
from datetime import datetime
import datetime

def authent(code_famille, email_auth, saison_actuelle):

    date_jour = datetime.date.today()
    ddn_majeur_today = datetime.datetime(date_jour.year-18,date_jour.month,date_jour.day)
    authentific = False
    retour = ''

    if Famille.objects.filter(nom_famille=code_famille).exists():
        # print("code famille existant")

        # 1- cohérence email - code famille côté Contacts
        if Adherent.objects.all().filter(famille__nom_famille=code_famille). \
                filter(adherent_saison__saison=saison_actuelle).filter(contact__email_contact=email_auth).exists():
            # print("code famille et email contact ok")
            authentific = True

        # 2- cohérence email - code famille côté adhérent majeur
        #  select f.nom_famille, a.email_adh from inscription_adherent a, inscription_famille f where
        #  f.id = a.famille_id and (date('now') - a.ddn >= 18) and a.email_adh <> '';
        if Adherent.objects.all().filter(famille__nom_famille=code_famille). \
                filter(adherent_saison__saison=saison_actuelle).filter(email_adh=email_auth). \
                filter(ddn__lte=ddn_majeur_today).exists():
            # print("code famille et email adherent majeur ok")
            authentific = True
        # for i in query_set_mails_adher_majeur:
        #     mails_du_code_famille.append(i.get('email_adh'))

        if authentific == True:
            code = 3
            retour = 'authent OK'
        else:
            code = 2
            retour = "L'adresse mail n'est pas connue ou vous n'êtes pas encore inscrit à la saison " + str(saison_actuelle)

    else:
        code = 1
        retour = 'Le code famille est inconnu.'

    return code, retour


def listing_adherents(code_famille, saison_actuelle):
    membres_famille = []

    query_set_adh = Adherent.objects.values('nom_adh', 'prenom_adh', 'taille', 'pk').filter(famille__nom_famille=code_famille).\
        filter(adherent_saison__saison=saison_actuelle)

    for mb in query_set_adh:

        membre = []
        membre.append(mb.get('prenom_adh').capitalize() + ' ' + mb.get('nom_adh').capitalize())
        membre.append(mb.get('taille'))
        membre.append(str(mb.get('pk')))

        query_set_commande = CommandesDobok.objects.values('statut_commande', 'date_crea', 'date_distribution',
                                                           'statut_paiement', 'montant_reel').\
            filter(adherent=mb.get('pk')).filter(saison__saison=saison_actuelle)

        for cmd in query_set_commande:
            # récupération des valeurs "en cours", "distribué" correspondant au statut_commande
            for index, statut in enumerate(CommandesDobok.STATUT_COMMANDE):
                if statut[0] == cmd.get('statut_commande') :
                    statut_cmd = statut[1]

            membre.append(statut_cmd)
            membre.append(cmd.get('date_crea').strftime("%d/%m/%Y"))

            if cmd.get('date_distribution') :
                membre.append(cmd.get('date_distribution').strftime("%d/%m/%Y"))
            else :
                membre.append(cmd.get('date_distribution'))

            # récupération des valeurs "en cours", "distribué" correspondant au statut_commande
            for index, statut in enumerate(CommandesDobok.STAUT_PAIEMENT):
                if statut[0] == cmd.get('statut_paiement') :
                    statut_pymt = statut[1]
            membre.append(statut_pymt)

            if cmd.get('montant_reel') :
                membre.append(cmd.get('montant_reel'))
            else :
                membre.append('0')

        # création du tableau père
        membres_famille.append(membre)

    # print("nom_adherent :", membres_famille)

    return membres_famille


def statut_paiement_cotisation(code_famille, saison_actuelle):
    query_set_paiement = Paiement.objects.values('paye').filter(famille__nom_famille=code_famille). \
        filter(saison=saison_actuelle)

    if query_set_paiement :   # s'il existe une ligne paiement pour la personne
        for pymt in query_set_paiement:
            statut_paiement = pymt.get('paye')
    else:
        statut_paiement = "0"

    return statut_paiement


def commandes_passees(id_mb):
    command_dobok = []

    query_set_adh = Adherent.objects.values('nom_adh', 'prenom_adh', 'taille', 'pk').filter(pk__in=id_mb)

    for adh in query_set_adh:
        query_set_commd = CommandesDobok.objects.values('tarif_info').filter(adherent=adh.get('pk'))

        for cmd in query_set_commd:
            command_dobok.append ([ adh.get('nom_adh') + ' ' + adh.get('prenom_adh'), adh.get('taille'),
                                 cmd.get('tarif_info') ])

    return command_dobok


def command_exist(id_adh, saison_actuelle):
    command_trouve = False

    if CommandesDobok.objects.values().filter(adherent_id=id_adh).filter(saison=saison_actuelle).exists() :
        command_trouve = True

    return command_trouve


def envoi_mail(list_info, code_famille, email):

    message = "Bonjour, \n Votre commande de dobok(s) est prise en compte pour : \n \n"
    for i in range(len(list_info)):
        message += str(i+1) + '- ' + str(list_info[i][0]) + ' (taille ' + str(list_info[i][1]) + ' cm) - tarif informatif de : ' + str(list_info[i][2]) + '€\n\n'

    message += "Le tarif est donné à titre informatif. Il pourra vous être recommandé une taille au-dessus ou en-dessous.\n"
    message += "Vous pouvez régler en espèces ou par chèque, au moment de la distribution.\n"

    message += "\n Rappel de votre code famille : " + str(code_famille) + "\n \n"

    message += "Le Mudo Club Argenteuil"

    # print('email:', email)
    # print('message :' + message)

    send_mail(
        'Confirmation inscription taekwondo MUDO Club Argenteuil', # objet du mail
        message, # message
        'mudoclub@tkdinscription.vfeapps.fr', # from email (envoyeur)
        list(email), # to mail (destinataire),
        fail_silently = False
    )
    return 'ok'