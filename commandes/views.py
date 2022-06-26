from django.shortcuts import render
from commandes.forms import AuthentifForm
from commandes.fonctions import authent, listing_adherents, statut_paiement_cotisation, commandes_passees, command_exist, envoi_mail
from inscription.fonctions import code_maintenance
from inscription.models import Saison, Adherent, Famille
from commandes.models import CommandesDobok, PrixDobok
from cotisation.models import Maintenance
from django.db import transaction

@transaction.atomic
def commandes(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    maintenance = Maintenance.objects.get(maintenance='Maintenance')
    # blocage de l'accès des pages pour empêcher les gens qui auraient gardé les url directes en historique ou en favori \
    # d'accéder aux formulaires pendant la maintenace
    if code_maintenance(maintenance) == 1:
        print('retour à accueil')
        page_html_suivante = 'accueil-maintenance.html'
    else :
        page_html_suivante = 'commandes/authentif.html'

    message_err = ''
    membres_famille = ''
    code_famille = ''
    statut_paiement = ''
    ### variables pour personnalisation de la page d'authentification et utilisation pour un autre besoin (accès privé staff)
    titre_pageHTML = 'Commandes'    # titre de la page HTML
    placeholderEmail = 'Votre adresse email'
    placeholderPwd = 'Votre code famille (*)'
    nextDjangoURL = 'commandes'     # URL dajngo de la balise <form> de la page d'authentification
    ### Fin variables pesonnalisation


    if request.method == 'GET': # GET
        authentForm = AuthentifForm()

    else: # POST
        authentForm = AuthentifForm(request.POST)

        email_auth = request.POST['email_auth'].strip()
        code_famille = request.POST['pwd'].strip()

        code, message_err = authent(code_famille, email_auth, saison_actuelle)

        if code == 3 : # authentification OK
            # récupération des adhérents correspondant au code famille
            membres_famille = listing_adherents(code_famille, saison_actuelle)
            statut_paiement = statut_paiement_cotisation(code_famille, saison_actuelle)
            page_html_suivante = "commandes/commandes.html"

        # conservation en variable de session du code famille et du mail
        request.session['code_famille'] = code_famille
        request.session['email_auth'] = email_auth
        request.session['membres_famille'] = membres_famille

    context = {
        'authentForm': authentForm,
        'saison_actuelle' : saison_actuelle,
        'maintenance': code_maintenance(maintenance),
        'message': message_err,
        'code_famille': code_famille,
        'membres_famille': membres_famille,
        'statut_paiement' : statut_paiement,
        'titre_pageHTML' : titre_pageHTML,
        'nextDjangoURL' : nextDjangoURL,
        'placeholderEmail' : placeholderEmail,
        'placeholderPwd' : placeholderPwd
    }

    return render(request, page_html_suivante, context )

@transaction.atomic
def fin_commandes(request):
    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    maintenance = Maintenance.objects.get(maintenance='Maintenance')

    id_mb = []  # récupère les id_adherent de ceux qui commandent un dobok

    code_famille = request.session['code_famille']
    email_auth = request.session['email_auth']
    membres_famille = request.session['membres_famille']

    # enregistrement des tailles des adhérents
    for mb in membres_famille:
        # print (str(mb[0]) + ' ' + str(mb[1]) + ' ' + str(mb[2]))
        taille = request.POST.get('tailleAdh' + str(mb[2]))  # permet de récupérer la valeur du champ de formulaire taillexx (xx étant l'ID de l'adhérent)

        if taille :         # si l'input-text taille existe (il n'apparait pas si la commande est déjà passée)
            # update de la taille des adhérents en base de données
            Adherent.objects.filter(pk=mb[2]).update(taille=taille)

        statut_commande = request.POST.get('flexRadio' + str(mb[2]))   # mb[2] est l'id_adherent
        if statut_commande == '1' :   # membre de la famille qui souhaite un dobok
            if not command_exist(mb[2], saison_actuelle) :      # s'il n'existe pas de commande pour l'adherent en base
                id_mb.append(mb[2])

                # récupération du queryset correspondant au code_famille dans la table Famille
                info_code_famille = Famille.objects.get(nom_famille=code_famille)
                # récupération du queryset correspondant à l'adhérent dans la table Adherent
                info_adherent = Adherent.objects.get(pk=mb[2])

                # récupération du prix informatif du dobok
                if PrixDobok.objects.values('prix').filter(taille_min__lte=taille, taille_max__gte=taille).exists():
                    qs_prix_informatif = PrixDobok.objects.values('prix').filter(taille_min__lte=taille,
                                                                              taille_max__gte=taille)
                    for prix_info in qs_prix_informatif:
                        prix_informatif = prix_info.get('prix')
                else :
                    prix_informatif = 'à déterminer'    # quand il n'y a pas de prix en regard de la taille choisie

                # insertion d'une ligne dans la table Commande Dobok
                command = CommandesDobok()
                command.famille = info_code_famille
                command.adherent = info_adherent
                command.taille = taille
                command.saison = saison_actuelle
                command.statut_commande = '1'  # en cours
                command.tarif_info = prix_informatif
                command.save()

    # récupération infos des commandes pour affichage récapitulatif
    command_dobok = commandes_passees(id_mb)

    # envoi du mail
    envoi_mail(command_dobok, code_famille, email_auth)


    del request.session['code_famille']
    del request.session['email_auth']
    del request.session['membres_famille']

    context = {
        'saison_actuelle': saison_actuelle,
        'maintenance': code_maintenance(maintenance),
        'code_famille': code_famille,
        'email_auth': email_auth,
        'command_dobok' : command_dobok,
    }

    return render(request, 'commandes/fin_commande.html', context )

