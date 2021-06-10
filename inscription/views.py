from django.shortcuts import render
from inscription.forms import AdherentForm, GradeForm, ContactForm, DisciplineForm
from inscription.models import Contact, Adherent, Famille, Adherent_Saison, CategorieCombat, Grade, Paiement
from cotisation.models import Saison, Categorie, Discipline
from inscription.fonctions import crea_code_famille, calcul_cotis_adh
from cotisation.fonctions import reduc_famille, appliq_reduc
from django.db import transaction
from datetime import date

@transaction.atomic
def inscription(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)

    page_html_suivante = "inscription/inscription.html"
    cotis_adh = 0
    code_famille = ''
    nb_personnes = 0
    list_nom = ''
    list_discipline = ''
    list_cotisation = ''

    if request.method == 'GET':
        # affichage du fomulaire vide
        formAdh = AdherentForm()
        formGrade = GradeForm()
        formContact = ContactForm()
        formDiscipline = DisciplineForm()
        page_html_suivante = "inscription/inscription.html"

    else :
        #print('méthode post')
        formAdh = AdherentForm(request.POST)
        formGrade = GradeForm(request.POST)
        formContact = ContactForm(request.POST)
        formDiscipline = DisciplineForm(request.POST)

        if formAdh.is_valid() and formGrade.is_valid() and formContact.is_valid()\
                 and formDiscipline.is_valid():

            # comptage du nombre de membres de la famille inscrites
            nb_personnes = int(request.POST['nb_personnes']) + 1
            # enregistrement du 1er membre de la famille (bouton submit "Inscrire une autre personne"
            # ou d'une seule personne (bouton submit "Terminer l'inscription")
            if request.POST['code_famille'] == '':
                #print("création code famille")
                # création d'un code famille pour regrouper les adhérents d'une même famille
                code_famille = crea_code_famille(request.POST['nom_adh'])
                # création d'une nouvelle ligne dans la table Famille
                Famille.objects.create(nom_famille=code_famille)
                # Récupération de la ligne nouvellement insérée dans Famille
                info_famille = Famille.objects.get(nom_famille=code_famille)
            else:
                #print("code famille connu :", request.POST['code_famille'])
                code_famille = request.POST['code_famille']
                info_famille = Famille.objects.get(nom_famille=request.POST['code_famille'])

            ### à modifier car le contact peut changer pour un autre membre de la famille ####
            if request.POST['code_famille'] == '':
                # enregistrement du contact dans la base Contact
                formContact.save()
            else:
                # test pour savoir si le contact existe déjà en base
                if Contact.objects.filter(nom_contact=request.POST['nom_contact'],
                                                   prenom_contact=request.POST['prenom_contact'],
                                                       email_contact = request.POST['email_contact']).count() == 0:
                    formContact.save()

            # avant enregistrement de l'adhérent, récupération du contact associé
            newAdh = formAdh.save(commit=False)
            info_contact = Contact.objects.get(nom_contact=request.POST['nom_contact'],
                                             prenom_contact=request.POST['prenom_contact'],
                                            email_contact = request.POST['email_contact'])
            newAdh.contact = info_contact
            newAdh.famille = info_famille
            # enregistrement de l'adhérent dans la table Adhérent
            formAdh.save()

            # récupération des infos adhérent de la table Adherent
            info_adherent = Adherent.objects.get(nom_adh=request.POST['nom_adh'], prenom_adh=request.POST['prenom_adh'])

            # calcul age adhérent au 31 décembre de la saison suivante
            ddn_split = request.POST['ddn'].split('/')
            age_adherent = int((date.today().year + 1)) - int(ddn_split[2])

            # récupération de la catégorie de l'Adhérent (adulte, étudiant, enfant, ado, baby)
            categorie_adh = Categorie.objects.get(age_inf_catg__lte=age_adherent-1, age_sup_catg__gte=age_adherent-1,
                                                           etudiant=request.POST['etudiant'])

            # récupération de la catégorie de combat
            categorie_combat = CategorieCombat.objects.get(age_min__lte=age_adherent, age_max__gte=age_adherent)

            # récupération du grade
            if request.POST['couleur'] != '':
                grade = Grade.objects.get(pk=request.POST['couleur'])
            else :
                grade = False

            # récupération de la discipline choisie
            discipline = Discipline.objects.get(pk=request.POST['discipline'])

            # enregistrement des infos Adhérent en base de données Adherent_Saison
            if grade:
                Adherent_Saison.objects.create(adherent=info_adherent, saison= saison_actuelle,
                                               grade=grade, categorie=categorie_adh,
                                               categorie_combat=categorie_combat, discipline=discipline
                                               )
            else:
                Adherent_Saison.objects.create(adherent=info_adherent, saison= saison_actuelle,
                                               categorie=categorie_adh,
                                               categorie_combat=categorie_combat, discipline=discipline
                                               )

            # génération du Code Tarification qui permet d'aller chercher le tarif de l'adhérent selon son age et la discipline
            code_tarification = categorie_adh.code_catg + discipline.code_discipl
            #print('code_tarification : ', code_tarification)
            # calcul de la cotisation pour l'adhérent
            cotis_adh = calcul_cotis_adh(code_tarification, saison_actuelle, 0)

            # remplissage des listes nom des adhérents, discipline et cotsation de l'adhérent pour affichage en fin d'inscription
            list_nom = request.POST['list_nom']
            if request.POST['list_nom'] != '':
                list_nom = list_nom + ',' + request.POST['nom_adh'] + ' ' + request.POST['prenom_adh']
            else:
                list_nom = request.POST['nom_adh'] + ' ' + request.POST['prenom_adh']

            list_discipline = request.POST['list_discipline']
            if request.POST['list_discipline'] != '':
                list_discipline = list_discipline + ',' + discipline.nom_discipl
            else:
                list_discipline = discipline.nom_discipl

            list_cotisation = request.POST['list_cotisation']
            if request.POST['list_cotisation'] != '':
                list_cotisation = list_cotisation + ',' + str(cotis_adh)
            else:
                list_cotisation = str(cotis_adh)

            # addition de cotisation de l'adhérent actuel et de la cotisation de l'adhérent inscrit juste avant
            if request.POST['cotis_adh'] != '0':
                cotis_adh += int(request.POST['cotis_adh'])
            #print('cotis_adh :', cotis_adh)

            if request.POST['Enrg'] == 'Terminer':
                if request.POST['cotis_adh'] != '0':
                    # récupération du taux de réduction valable pour la famille
                    taux_reduc = reduc_famille(nb_personnes, 0, saison_actuelle)
                    #cotis_adh = cotis_adh * ((100 - int(taux_reduc))/100)
                    cotis_adh = appliq_reduc(taux_reduc, cotis_adh)
                    #print("nb_personnes :", nb_personnes)
                    #print("taux_reduc :", taux_reduc)

                    list_nom = list_nom.split(',')
                    list_discipline = list_discipline.split(',')
                    list_cotisation = list_cotisation.split(',')

                else:   # je demande à spliter sur "*" pour garder les mots ensemble
                    list_nom = list_nom.split('*')
                    list_discipline = list_discipline.split('*')
                    list_cotisation = list_cotisation.split('*')

                # enregistrement montant de la cotisation dans la table Paiement
                Paiement.objects.create(famille=info_famille, saison=saison_actuelle, montant_cotis=cotis_adh)

                page_html_suivante = "inscription/fin_inscription.html"
            else:
                page_html_suivante = "inscription/inscription.html"
                formAdh = AdherentForm(initial={"adresse":request.POST['adresse'],"cp":request.POST['cp'],
                                                "ville":request.POST['ville']})
                formGrade = GradeForm()
                formContact = ContactForm(request.POST)
                formDiscipline = DisciplineForm()

        else:
            print("formulaire non valide")


    context = {
        'saison_actuelle': saison_actuelle,
        'formAdh': formAdh,
        'formGrade': formGrade,
        'formContact' : formContact,
        'formDiscipline' : formDiscipline,
        'cotis_adh' : cotis_adh,
        'code_famille' : code_famille,
        'nb_personnes' : nb_personnes,
        'list_nom': list_nom,
        'list_discipline': list_discipline,
        'list_cotisation' : list_cotisation,
    }

    return render(request, page_html_suivante, context )


