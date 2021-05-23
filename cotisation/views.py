from django.shortcuts import render
from cotisation.forms import SimulCotisForm
from cotisation.fonctions import calcul


def simul_cotisation(request):

    if request.method == 'GET':
        #print('méthode get')
        form = SimulCotisForm()
        cotis_annuelle = 0
        nb_personnes = 0
        reinscription = 0
    else :
        #print('méthode post')
        form = SimulCotisForm(request.POST)
        cotis_annuelle, nb_personnes, reinscription = calcul(request.POST)

    context = {
        'form': form,
        'nb_personnes' : nb_personnes,
        'reinscription' : reinscription,
        'cotis_annuelle' : cotis_annuelle,
    }

    return render(request, 'cotisation/simul_cotisation.html', context )
