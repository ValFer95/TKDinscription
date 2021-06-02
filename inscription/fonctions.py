from random import choice, randrange
from cotisation.fonctions import tarif_calcul, reduc_une_personne, reduc_famille

suffixe = ['&', '#', '@', '*', '-', '$', '%']

# CREATION D'UN CODE FAMILLE QUI SERA LA CLEF DE GROUPEMENT DES ADHERENTS D'UNE MEME FAMILLE
def crea_code_famille(nom_adh):
    code_famille = nom_adh + choice(suffixe) + str(randrange(1,99))
    return code_famille


# CALCUL DE LA COTISATION ANNUELLE POUR L'ADHERENT
def calcul_cotis_adh(code_tarif, saison, reinscription):
    tarif = tarif_calcul(code_tarif, saison, reinscription)
    taux_reduc = reduc_une_personne(saison, reinscription)

    return tarif * taux_reduc
