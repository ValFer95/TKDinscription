from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from commandes.forms import AuthentifForm
from cotisation.models import Saison
from staff.fonctions import calcul_nb_cotis_dues, calcul_nb_certif_dus, message_Cotis, envoi_mail, info_famille_cotis_non_payee
from datetime import datetime
import datetime

def sommaire(request):
    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    titre_pageHTML = 'Pages réservées au staff'
    nextDjangoURL = 'sommaire_staff'
    placeholderEmail = "Saisir l'adresse email du staff"
    placeholderPwd = "Saisir le mot de passe du staff"
    message_err = ''
    page_suivante = ''
    nb_famille_sans_cotis_payee = ''
    nb_famille_avec_cotis_partiel = ''
    nb_certif_manquant = ''
    date_jour = datetime.date.today()

    if request.method == 'GET': # GET
        authentForm = AuthentifForm()
        page_suivante = 'staff/authent.html'

    else: # POST
        authentForm = AuthentifForm(request.POST)
        # vérifier que le login / mot de passe est correct en utilisant l'authentification de l'administration Django
        user = authenticate(username=request.POST['email_auth'], password=request.POST['pwd'])
        # si l'utilisateur a été reconnu
        if user is not None:
            login(request, user)
            nb_famille_sans_cotis_payee = calcul_nb_cotis_dues(0)
            nb_famille_avec_cotis_partiel = calcul_nb_cotis_dues(1)
            nb_certif_manquant = calcul_nb_certif_dus()
            page_suivante = 'staff/sommaire.html'
        # si échec de l'authentification
        else :
            message_err = "Vous n'êtes pas autorisé à entrer dans cet espace."
            page_suivante = 'staff/authent.html'

    context = {
        'saison_actuelle': saison_actuelle,
        'authentForm': authentForm,
        'message': message_err,
        'titre_pageHTML': titre_pageHTML,
        'nextDjangoURL': nextDjangoURL,
        'placeholderEmail': placeholderEmail,
        'placeholderPwd': placeholderPwd,
        'nb_famille_sans_cotis_payee' : nb_famille_sans_cotis_payee,
        'nb_famille_avec_cotis_partiel' : nb_famille_avec_cotis_partiel,
        'nb_certif_manquant' : nb_certif_manquant,
        'date_jour' : date_jour,
    }

    return render(request, page_suivante, context)


@login_required   # vérifie que l'utilisateur est bien connecté (grâce à la fonction login(request, user))
def relances(request):
    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    page_suivante = 'staff/sommaire.html'
    date_jour = datetime.date.today()
    nb_famille_sans_cotis_payee = calcul_nb_cotis_dues(0)
    nb_famille_avec_cotis_partiel = calcul_nb_cotis_dues(1)
    nb_certif_manquant = calcul_nb_certif_dus()

    if "lancerCotisPart" in request.POST :
        infos_famille = info_famille_cotis_non_payee(1)
        for i in range(len(infos_famille)):
            message, email, objet = message_Cotis("CotisPart", infos_famille[i])
            envoi_mail(objet, message, email)
    elif "lancerCotisNonPayee" in request.POST :
        infos_famille = info_famille_cotis_non_payee(0)
        for i in range(len(infos_famille)):
            message, email, objet = message_Cotis("CotisNonPayee", infos_famille[i])
            envoi_mail(objet, message, email)
    elif "lancerCertifMed" in request.POST :
        print("certificat")
        # lancer le mailing demandé
        # inscrire en base de données la date du mailing

    # déconnexion de l'utilisateur
    # logout(request)

    context = {
        'saison_actuelle': saison_actuelle,
        'nb_famille_sans_cotis_payee': nb_famille_sans_cotis_payee,
        'nb_famille_avec_cotis_partiel': nb_famille_avec_cotis_partiel,
        'nb_certif_manquant': nb_certif_manquant,
        'date_jour': date_jour,
    }

    return render(request, page_suivante, context)