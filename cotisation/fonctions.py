from cotisation.models import Tarif, TauxReduction
from django.db.models import Max
import math


# *** CALCUL DU TAUX DE REDUCTION POUR LA FAMILLE ENTIERE SELON LE NOMBRE DE PERSONNES ***
def reduc_famille(nb_personnes, reinscription, saison):
    taux_famille = 0
    nb_personnnes_reduc_max = 0

    for tr in TauxReduction.objects.filter(saison__saison=saison).\
            exclude(condition_reduc=None).aggregate(Max('condition_reduc')).values():
        nb_personnnes_reduc_max = tr


    if nb_personnes >= int(nb_personnnes_reduc_max):
        nb_personnes = nb_personnnes_reduc_max

    if reinscription == '1':
        for t in TauxReduction.objects.filter(saison__saison=saison, condition_anciens=True,
                                              condition_reduc=nb_personnes).exclude(condition_reduc=None).values():
            taux_famille = t['pourcentage_reduc']
    else:
        for t in TauxReduction.objects.filter(saison__saison=saison, condition_nouveaux=True,
                                              condition_reduc=nb_personnes).exclude(condition_reduc=None).values():
            taux_famille = t['pourcentage_reduc']

    return taux_famille


# CALCUL DU TAUX DE REDUCTION POUR UNE PERSONNE ***
def reduc_une_personne(reinscription, saison):
    taux_reduc = 0
    if reinscription == '1':  # applique une réduction pour les anciens adhérents sans condition
        for r in TauxReduction.objects.filter(saison__saison=saison,
                                              condition_anciens=True,
                                              condition_reduc=None).values():
            #taux_reduc -= int(r['pourcentage_reduc']) / 100
            taux_reduc = int(r['pourcentage_reduc'])

    if reinscription == '0':  # applique une réduction pour les nouveaux adhérents sans condition
        for r in TauxReduction.objects.filter(saison__saison=saison,
                                              condition_nouveaux=True,
                                              condition_reduc=None).values():
            #taux_reduc -= int(r['pourcentage_reduc']) / 100
            taux_reduc = int(r['pourcentage_reduc'])
    return taux_reduc


# CALCUL DE LA COTISATION POUR UNE PERSONNE SELON LA DISCIPLINE ET LA SAISON
def tarif_calcul (code_tarif, saison, reinscription):
    tarif = 0
    # récupération des tarifs selon la discipline/réinscription/age
    for i in Tarif.objects.filter(code_tarif=code_tarif, saison__saison=saison).values():
        # print(valeurs_post['reinscription'])
        if reinscription == '1':  # réinscription d'un ancien adhérent
            if i['tarif_ancien']:  # tarif ancien adhérent
                tarif = i['tarif_ancien']
            else:  # si pas de tarif ancien proposé, on prend le tarif nouvel adhérent
                tarif = i['tarif_nouveau']
        else:  # nouvel adhérent
            tarif = i['tarif_nouveau']

    return tarif


# APPLICATION DE LA REDUCTION A LA COTISATION ANNUUELLE, renvoie la cotisation annuelle avec les réductions
def appliq_reduc(taux_reduc, cotis_annuelle):
    taux_reduc = (100 - int(taux_reduc))/100
    cotis_annuelle *= taux_reduc
    return math.floor(cotis_annuelle)


# *** CALCUL DE LA COTISATION ANNUELLE POUR LA FAMILLE ENTIERE AVEC REDUCTION ***
def calcul(valeurs_post, saison):
    cotis_annuelle = 0
    nb_personnes = 0
    taux_reduc = 1
    # print(valeurs_post)

    # *** CALCUL DE LA COTISATION ANNUELLE POUR LA FAMILLE ENTIERE AVANT REDUCTION ***
    for val in valeurs_post:                                        # Boucle sur le formulaire pour collecter le nombre de personnes par discipline

        if valeurs_post[val] and val != 'csrfmiddlewaretoken' and val != 'reinscription':      # valeurs_post[val] est le nombre de personne par discipline et val représente le couple age/discipline
            # print('Nb de personne:', val, valeurs_post[val])

            # récupération des tarifs selon la discipline/réinscription/age
            tarif = tarif_calcul(val, saison, valeurs_post['reinscription'])
            nb_personnes += int(valeurs_post[val])      # calcul le nombre de personnes de la famille
            cotis_annuelle += int(valeurs_post[val]) * tarif    # calcul de la cotisation annuelle pour toutes les personnes avant application réducs

    # *** APPLICATION DES REDUCTIONS ***
    if cotis_annuelle > 0:
        taux_reduc = reduc_une_personne(valeurs_post['reinscription'], saison)
        print("taux_reduc avant :", taux_reduc)

        if nb_personnes > 1:
            taux_famille = reduc_famille(nb_personnes, valeurs_post['reinscription'], saison)
            print("taux_famille :", taux_famille)
            taux_reduc += int(taux_famille)

        print("taux_reduc après:", taux_reduc)
        print("cotis_annuelle :", cotis_annuelle)

        cotis_annuelle = appliq_reduc(taux_reduc, cotis_annuelle)

    return cotis_annuelle, nb_personnes, valeurs_post['reinscription']
