from random import choice, randrange

suffixe = ['&', '#', '@', '*', '-', '$', '%']

def crea_code_famille(nom_adh):
    code_famille = nom_adh + choice(suffixe) + str(randrange(1,99))
    return code_famille
