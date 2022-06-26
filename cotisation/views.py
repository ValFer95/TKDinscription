from django.shortcuts import render
from cotisation.forms import SimulCotisForm
from cotisation.fonctions import calcul
from inscription.fonctions import code_maintenance
from cotisation.models import Saison, Maintenance


def simul_cotisation(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    maintenance = Maintenance.objects.get(maintenance='Maintenance')

    # blocage de l'accès des pages pour empêcher les gens qui auraient gardé les url directes en historique ou en favori \
    # d'accéder aux formulaires pendant la maintenace
    if code_maintenance(maintenance) == 1:
        page_suivante = 'accueil-maintenance.html'
    else :
        page_suivante = 'cotisation/simul_cotisation.html'

    if request.method == 'GET':
        #print('méthode get')
        form = SimulCotisForm()
        cotis_annuelle = 0
        nb_personnes = 0
        reinscription = 0
    else :
        # print('méthode post')
        form = SimulCotisForm(request.POST)
        cotis_annuelle, nb_personnes, reinscription = calcul(request.POST, saison_actuelle.saison)

        # print("cotis_annuelle :", cotis_annuelle)

    context = {
        'saison_actuelle' : saison_actuelle,
        'maintenance': code_maintenance(maintenance),
        'form': form,
        'nb_personnes' : nb_personnes,
        'reinscription' : reinscription,
        'cotis_annuelle' : cotis_annuelle,
    }

    return render(request, page_suivante, context )


def accueil(request):
    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    maintenance = Maintenance.objects.get(maintenance='Maintenance')

    if str(maintenance) == 'True' : # pour mettre le site en maintenance
        return render(request, 'accueil-maintenance.html', {'saison_actuelle' : '2022-2023', 'maintenance': code_maintenance(maintenance), })
    else :
        return render(request, 'accueil.html', {'saison_actuelle': saison_actuelle, 'maintenance': code_maintenance(maintenance), } )