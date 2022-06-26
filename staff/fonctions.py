from django.db import connection
from django.core.mail import send_mail
from inscription.fonctions import calcul_age_adh, liste_dest_mail
import datetime


def calcul_nb_cotis_dues(niv_paiement):

    requete = "SELECT COUNT(DISTINCT ifa.id) as id_famille, COUNT(DISTINCT ia.id) as id_adh \
                FROM inscription_adherent_saison ias \
                JOIN inscription_adherent ia ON ia.id = ias.adherent_id \
                JOIN cotisation_saison cs ON ias.saison_id = cs.id \
                JOIN inscription_famille ifa ON ia.famille_id = ifa.id \
                JOIN inscription_paiement ip ON ip.famille_id = ifa.id \
                JOIN inscription_contact ic ON ic.id = ia.contact_id \
                WHERE cs.saison_actuelle = 1 \
                AND ip.paye = " + str(niv_paiement)

    with connection.cursor() as cursor:
        cursor.execute(requete)
        row = cursor.fetchone()

    return row[0], row[1]


def info_famille_cotis_non_payee(niv_paiement):
    infos_famille = []

    requete =  "SELECT ia.nom_adh || ' ' || ia.prenom_adh as 'Nom adhérent', ia.ddn, ia.sexe, ifa.id as id_famille, "

    if niv_paiement == 0:
        requete += "ip.montant_cotis,"
    else :
        requete += "ip.montant_cotis - SUM(ihp.montant_regle) as cotis_restante, "

    requete += "ia.email_adh as 'mail adhérent', ic.email_contact as 'mail_contact', \
                CASE WHEN ip.paye = 0 THEN 'Cotisation non réglée' \
                WHEN ip.paye = 1 THEN 'Cotisation partiellement réglée' \
                ELSE 'Cotisation réglée' \
                END AS Cotisation \
                FROM inscription_adherent_saison ias \
                JOIN inscription_adherent ia ON ia.id = ias.adherent_id \
                JOIN cotisation_saison cs ON ias.saison_id = cs.id \
                JOIN inscription_famille ifa ON ia.famille_id = ifa.id \
                JOIN inscription_paiement ip ON (ip.famille_id = ifa.id	AND ip.saison_id = cs.id) \
                JOIN inscription_contact ic ON ic.id = ia.contact_id "

    if niv_paiement == 1:
        requete += "JOIN inscription_historiquepaiement ihp ON (ihp.famille_id = ifa.id AND ihp.saison_id = cs.id) "

    requete += "WHERE cs.saison_actuelle = 1 \
                AND ip.paye = " + str(niv_paiement) + " "

    if niv_paiement == 1:
        requete += "GROUP BY ia.nom_adh || ' ' || ia.prenom_adh "

    requete += "order by ip.paye DESC, ifa.id, ia.nom_adh || ' ' || ia.prenom_adh;"

    with connection.cursor() as cursor:
        cursor.execute(requete)
        rows = cursor.fetchall()
        # print("nb de lignes :" , len(rows))
        # row[0] -> nom prénom adhérent, row[1] -> ddn, row[2] -> sexe, row[3] -> id_famille,
        # row[4] -> cotisation à payer pour la famille, row[5] -> mail adher, row[6] -> mail contact
        id_famille_before = 0
        i = 0  # incrément pour le tableau infos_famille
        for row in rows:
            if row[3] != id_famille_before:         # pour regrouper les adhérents d'une même famille

                if row[5] is not None:
                    email = liste_dest_mail('', calcul_age_adh(row[1].strftime("%d/%m/%Y"), 'reel'), row[5], row[6])
                else:
                    email = liste_dest_mail('', calcul_age_adh(row[1].strftime("%d/%m/%Y"), 'reel'), row[6], row[6])

                infos_famille.append([ [row[0]], [row[2]], row[4], email, row[3]])
                id_famille_before = row[3]
                i += 1
            else:       # pour ajouter le nom prénom de l'adhérent dans la ligne de la famille
                infos_famille[i - 1][0].insert(0, row[0])
                infos_famille[i - 1][1].insert(0, row[2])

    # print(infos_famille)
    connection.close()
    return infos_famille


def calcul_nb_certif_dus():
    requete = "SELECT COUNT(ias.id) as nbCertifManquant \
                FROM inscription_adherent_saison ias \
                JOIN cotisation_saison cs ON ias.saison_id = cs.id \
                WHERE cs.saison_actuelle = 1  \
                AND ias.certif_med = 0"

    with connection.cursor() as cursor:
        cursor.execute(requete)
        row = cursor.fetchone()

    return row[0]


def calcul_nb_reinscrip() :
    requete = "SELECT COUNT(DISTINCT ifa.id) as id_famille, COUNT(DISTINCT ia.id) as id_adhr \
                FROM inscription_adherent_saison ias \
                JOIN inscription_adherent ia ON ia.id = ias.adherent_id \
                JOIN cotisation_saison cs ON ias.saison_id = cs.id \
                JOIN inscription_famille ifa ON ia.famille_id = ifa.id \
                JOIN inscription_paiement ip ON ip.famille_id = ifa.id \
                WHERE cs.saison_actuelle = 1 \
                AND ip.paye IN (1,2)"

    with connection.cursor() as cursor:
        cursor.execute(requete)
        row = cursor.fetchone()

    return row[0], row[1]


def message_Cotis(statut, infos_famille):

    objet = 'Mudo Club Argenteuil - Taekwondo - Relance cotisation'

    # infos_famille[0] -> liste des noms et prénoms des adhérents
    # infos_famille[1] -> liste des sexes des adhérents
    # infos_famille[2] -> cotisation qui reste à régler
    # infos_famille[3] -> adresse email du destinataire

    sexes_adher = ", ".join(infos_famille[1])
    email = infos_famille[3]

    message = "Bonjour, \n \n"

    if len(infos_famille[0]) == 1:
        message += "".join(infos_famille[0])
        if 'M' in sexes_adher:
            message += ' est inscrit'
        else:
            message += ' est inscrite'
    else:
        for i in range(len(infos_famille[0])) :
            message += str(infos_famille[0][i])
            if i == len(infos_famille[0]) - 1:
                if 'M' in sexes_adher:
                    message += ' sont inscrits'
                else:
                    message += ' sont inscrites'
            else:
                if i == len(infos_famille[0]) - 2:
                    message += ' et '
                else :
                    message += ', '

    message += " au club de Taekwondo d'Argenteuil (MUDO Club) pour la saison 2021 - 2022. \n"

    if statut == 'CotisNonPayee':
        message += "A ce jour, la cotisation n'a pas encore été réglée.  \n\n"
    else:
        message += "A ce jour, il reste " + str(infos_famille[2]) + "€ à régler.\n\n"

    message += "Merci d'apporter votre règlement d'un montant de " + str(infos_famille[2]) + "€ dans une enveloppe portant vos nom et prénom dans les plus brefs délais. \n"
    message += "Vous pouvez régler en espèces, par virement ou par chèque (jusqu'à 3 fois).\n"
    message += "Les chèques seront déposés le 5 de chaque mois. \n\n"

    message += "Le Mudo Club Argenteuil \n\n"

    if statut == 'CotisNonPayee':
        message += "PS: Si vous vous êtes désisté et n'avez jamais participé au cours, merci de nous en informer par retour de mail " \
                   "en indiquant votre souhait de suppression de vos coordonnées de la base de données. Ceci évitera un prochain " \
                   "mail de relance. \n\n"

    return message, email, objet


def info_famille_reinscript():
    infos_famille = []
    requete = "SELECT ifa.id as id_famille, ifa.nom_famille as nom_famille, ia.ddn as ddn, ia.email_adh as 'mail adhérent', \
                ic.email_contact as 'mail_contact'  \
                FROM inscription_adherent_saison ias  \
                JOIN inscription_adherent ia ON ia.id = ias.adherent_id  \
                JOIN cotisation_saison cs ON ias.saison_id = cs.id  \
                JOIN inscription_famille ifa ON ia.famille_id = ifa.id  \
                JOIN inscription_paiement ip ON ip.famille_id = ifa.id  \
				JOIN inscription_contact ic ON ic.id = ia.contact_id \
                WHERE cs.saison_actuelle = 1  \
                AND ip.paye IN (1,2) \
				order by id_famille"

    with connection.cursor() as cursor:
        cursor.execute(requete)
        rows = cursor.fetchall()
        # row[0] -> id_famille, row[1] -> nom_famille,, row[2] -> ddn,
        # row[3] -> mail adher, row[4] -> mail contact
        id_famille_before = 0
        i = 0  # incrément pour le tableau infos_famille
        for row in rows:

            if row[0] != id_famille_before:         # pour regrouper les adhérents d'une même famille

                if row[3] is not None:
                    email = liste_dest_mail('', calcul_age_adh(row[2].strftime("%d/%m/%Y"), 'reel'), row[3], row[4])
                else:
                    email = liste_dest_mail('', calcul_age_adh(row[2].strftime("%d/%m/%Y"), 'reel'), row[4], row[4])

                id_famille_before = row[0]
                infos_famille.append([ row[1], email, row[0]])

            else:
                if row[3] is not None:
                    email = liste_dest_mail(email, calcul_age_adh(row[2].strftime("%d/%m/%Y"), 'reel'), row[3], row[4])
                else:
                    email = liste_dest_mail(email, calcul_age_adh(row[2].strftime("%d/%m/%Y"), 'reel'), row[4], row[4])

                infos_famille[i - 1][1] = email

    #print(infos_famille)
    connection.close()
    return infos_famille


def message_reinscript(infos_famille):
    date_jour = datetime.date.today()
    objet = "Mudo Club Argenteuil - Réinscription saison - " + str(date_jour.year) + "-" + str(date_jour.year + 1)

    # infos_famille[0] -> code_famille
    # infos_famille[1] -> adresse email du destinataire

    email = infos_famille[1]
    #print ('email : ' + email)

    message = 'Bonjour, \n \n'

    message += "La réinscription au Mudo Club Argenteuil saison " + str(date_jour.year) + "-" + str(date_jour.year + 1) + " est ouverte ! \n"

    message += "Nous maintenons l'application de 10% de réduction sur le montant de cotisation standard ancien adhérent (même tarif que la saison actuelle) en compensation de la situation COVID.\n\n"

    message += "Pour vous réinscrire : \n\n"
    message += "1-> rendez-vous sur la page https://tkdinscription.vfeapps.fr/q_inscription/ \n\n"
    message += "2-> Vous aurez besoin de votre code famille : " + infos_famille[0] + " \n"
    message += "Les formulaires sont préremplis avec vos données. Vérifiez que toutes les informations sont correctes et changez-les si besoin. N'oubliez pas d'indiquer le grade que vous avez obtenu cette année!"
    message += "Le récapitulatif de la réinscription sera envoyé à l'adresse mail du contact pour les adhérents mineurs. "
    message += "Si l'adhérent est majeur, le récapitulatif sera envoyé à l'adresse mail de l'adhérent si connue, sinon à l'adresse mail du contact. \n\n"

    message += "3-> le paiement ne se fait pas en ligne. Une fois l'inscription réalisée, apportez une enveloppe fermée indiquant "
    message += "votre nom et le code famille, et contenant le(s) certificat(s) médicaux et le moyen de paiement (chèque(s), espèces, "
    message += "pass' sport). Si vous avez besoin d'une attestation CE, indiquez-le moi sur l'enveloppe. "
    message += "L'enveloppe sera à déposer au gymnase du club aux horaires des entraînements. Elle sera récupérée par moi-même ou par les professeurs. \n\n"

    message += "Vous pouvez télécharger le guide de réinscription à l'adresse https://www.mudoclubargenteuil.fr/2016/10/horaires-lieu.html. \n\n"

    message += "Je vous souhaite de bonnes vacances d'été ! \n"
    message += "Valérie du Mudo Club"

    # print("message :" + message)

    return message, email, objet


def envoi_mail(objet, message, email, id_famille, nature_relance):

    addr_mail = email.split(',')

    # print('objet:', objet)
    # print('addr_mail:', addr_mail)
    # print('message :' + message)

    result = send_mail(
        objet, # objet du mail
        message, # message
        'mudoclub@tkdinscription.vfeapps.fr', # from email (envoyeur)
        addr_mail, # to mail (destinataire),
        fail_silently = False
    )

    # if result == 1 :
    #     #print('id_famille : ' + str(id_famille) + ', email : ' + email + ' : OK')
    #     # intégration dans la table relance de l'id famille, le purpose de la relonce et la date de la relance
    # else:
    #     #print('id_famille : ' + str(id_famille) + ', email : ' + email + ' : ERR')

    return 'ok'