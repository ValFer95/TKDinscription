from random import choice, randrange
from cotisation.fonctions import tarif_calcul, reduc_une_personne, reduc_famille, appliq_reduc

suffixe = ['&', '#', '@', '*', '-', '$', '%']

# CREATION D'UN CODE FAMILLE QUI SERA LA CLEF DE GROUPEMENT DES ADHERENTS D'UNE MEME FAMILLE
def crea_code_famille(nom_adh):
    code_famille = nom_adh + choice(suffixe) + str(randrange(1,99))
    return code_famille


# CALCUL DE LA COTISATION ANNUELLE POUR L'ADHERENT
def calcul_cotis_adh(code_tarif, saison, reinscription):
    tarif = tarif_calcul(code_tarif, saison, reinscription)
    taux_reduc = reduc_une_personne(saison, reinscription)
    cotis_annuelle = appliq_reduc(taux_reduc, tarif)

    print("dans la fonction, tarif :", tarif)
    print("dans la fonction, taux_reduc :", taux_reduc)

    return cotis_annuelle
