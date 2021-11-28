from django.db import connection
from django.core.mail import send_mail
from inscription.fonctions import calcul_age_adh, liste_dest_mail


def calcul_nb_cotis_dues(niv_paiement):

    requete = "SELECT DISTINCT ifa.id as id_famille, \
                CASE WHEN ip.paye = 0 THEN 'Cotisation non réglée' \
                  WHEN ip.paye = 1 THEN 'Cotisation partiellement réglée' \
                ELSE 'Cotisation réglée' \
                END AS Cotisation \
                FROM inscription_adherent_saison ias \
                JOIN inscription_adherent ia ON ia.id = ias.adherent_id \
                JOIN cotisation_saison cs ON ias.saison_id = cs.id \
                JOIN inscription_famille ifa ON ia.famille_id = ifa.id \
                JOIN inscription_paiement ip ON ip.famille_id = ifa.id \
                JOIN inscription_contact ic ON ic.id = ia.contact_id \
                WHERE cs.saison_actuelle = 1 \
                AND ip.paye = " + str(niv_paiement) + " \
                order by ifa.id"

    with connection.cursor() as cursor:
        cursor.execute(requete)
        rows = cursor.fetchall()
        # print("nb de lignes :" , len(rows))
        # for row in rows:
        #     print(row[0])

    return len(rows)


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

                infos_famille.append([ [row[0]], [row[2]], row[4], email])
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

    message += "Merci d'apporter votre règlement d'un montant de " + str(infos_famille[2]) + "€ dans une une enveloppe portant vos nom et prénom dans les plus brefs délais. \n"
    message += "Vous pouvez régler en espèces, par virement ou par chèque (jusqu'à 3 fois).\n"
    message += "Les chèques seront déposés le 5 de chaque mois. \n\n"

    message += "Le Mudo Club Argenteuil \n\n"

    if statut == 'CotisNonPayee':
        message += "PS: Si vous vous êtes désisté et n'avez jamais participé au cours, merci de nous en informer par retour de mail " \
                   "en indiquant votre souhait de suppression de vos coordonnées de la base de données. Ceci évitera un prochain " \
                   "mail de relance. \n\n"

    return message, email, objet


def envoi_mail(objet, message, email):

    addr_mail = email.split(',')

    # print('objet:', objet)
    # print('addr_mail:', addr_mail)
    # print('message :' + message)

    send_mail(
        objet, # objet du mail
        message, # message
        'mudoclub@tkdinscription.vfeapps.fr', # from email (envoyeur)
        addr_mail, # to mail (destinataire),
        fail_silently = False
    )
    return 'ok'