from cotisation.models import Tarif, TauxReduction
from django.db.models import Max
import math


# *** CALCUL DU TAUX DE REDUCTION POUR LA FAMILLE ENTIERE SELON LE NOMBRE DE PERSONNES ***
def reduc_famille(nb_personnes, reinscription, saison):
    taux_famille = 1
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


# *** CALCUL DE LA COTISATION ANNUELLE POUR LA FAMILLE ENTIERE AVEC REDUCTION ***
def calcul(valeurs_post):
    cotis_annuelle = 0
    nb_personnes = 0
    taux_reduc = 1
    # print(valeurs_post)

    # *** CALCUL DE LA COTISATION ANNUELLE POUR LA FAMILLE ENTIERE AVANT REDUCTION ***
    for val in valeurs_post:                                        # Boucle sur le formulaire pour collecter le nombre de personnes par discipline

        if valeurs_post[val] and val != 'csrfmiddlewaretoken':      # valeurs_post[val] est le nombre de personne par discipline et val représente le couple age/discipline
            # print('Nb de personne:', val, valeurs_post[val])

            # récupération des tarifs selon la discipline/réinscription/age
            for i in Tarif.objects.filter(code_tarif=val, saison__saison='2020-2021').values():
                nb_personnes += int(valeurs_post[val])      # calcul le nombre de personnes de la famille
                # print(valeurs_post['reinscription'])
                if valeurs_post['reinscription'] == '1':    # réinscription d'un ancien adhérent
                    if i['tarif_ancien']:                   # tarif ancien adhérent
                        tarif = i['tarif_ancien']
                    else:                                   # si pas de tarif ancien proposé, on prend le tarif nouvel adhérent
                        tarif = i['tarif_nouveau']
                else:                                      # nouvel adhérent
                    tarif = i['tarif_nouveau']

                # print('tarif : ', tarif)
                cotis_annuelle += int(valeurs_post[val]) * tarif    # calcul de la cotisation annuelle pour toutes les personnes avant application réducs

    # *** APPLICATION DES REDUCTIONS ***
    if cotis_annuelle > 0:
        if valeurs_post['reinscription'] == '1':    # applique une réduction pour les anciens adhérents sans condition
            for r in TauxReduction.objects.filter(saison__saison='2020-2021',
                                                  condition_anciens=True,
                                                  condition_reduc=None).values():
                taux_reduc -= int(r['pourcentage_reduc']) / 100

        if valeurs_post['reinscription'] == '0':    # applique une réduction pour les nouveaux adhérents sans condition
            for r in TauxReduction.objects.filter(saison__saison='2020-2021',
                                                  condition_nouveaux=True,
                                                  condition_reduc=None).values():
                taux_reduc -= int(r['pourcentage_reduc']) / 100

        # print('taux_reduc special', taux_reduc)

        if nb_personnes > 1:
            taux_famille = reduc_famille(nb_personnes, valeurs_post['reinscription'], '2020-2021')
            # print('taux_famille: ', taux_famille)
            taux_reduc -= int(taux_famille) / 100

        # print('taux_reduc final', taux_reduc)
        cotis_annuelle *= taux_reduc
    return math.floor(cotis_annuelle), nb_personnes, valeurs_post['reinscription']
