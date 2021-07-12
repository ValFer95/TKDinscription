from django.shortcuts import render
from cotisation.forms import SimulCotisForm
from cotisation.fonctions import calcul
from cotisation.models import Saison


def simul_cotisation(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    saison_prochaine = Saison.objects.get(saison_prochaine=True)

    if request.method == 'GET':
        #print('méthode get')
        form = SimulCotisForm()
        cotis_annuelle = 0
        nb_personnes = 0
        reinscription = 0
    else :
        # print('méthode post')
        form = SimulCotisForm(request.POST)
        cotis_annuelle, nb_personnes, reinscription = calcul(request.POST, saison_prochaine.saison)

        # print("cotis_annuelle :", cotis_annuelle)

    context = {
        'saison_actuelle' : saison_actuelle,
        'saison_prochaine': saison_prochaine,
        'form': form,
        'nb_personnes' : nb_personnes,
        'reinscription' : reinscription,
        'cotis_annuelle' : cotis_annuelle,
    }

    return render(request, 'cotisation/simul_cotisation.html', context )


def accueil(request):
    # saison_actuelle = Saison.objects.get(saison_actuelle=True)
    # saison_prochaine = Saison.objects.get(saison_prochaine=True)
    saison_actuelle = request.session.get('saison_actuelle', Saison.objects.get(saison_actuelle=True))
    saison_prochaine = request.session.get('saison_prochaine', Saison.objects.get(saison_prochaine=True))
    return render(request, 'accueil.html', {'saison_actuelle':saison_actuelle, 'saison_prochaine':saison_prochaine} )