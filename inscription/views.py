from django.shortcuts import render
from inscription.forms import AdherentForm, GradeForm, ContactForm, DisciplineForm, DisciplineFormSelected, GradeFormSelected
from inscription.models import Contact, Adherent, Famille, Adherent_Saison, CategorieCombat, Grade, Paiement
from cotisation.models import Saison, Categorie, Discipline
from inscription.fonctions import crea_code_famille, calcul_cotis_adh, calcul_age_adh, envoi_mail, liste_dest_mail
from cotisation.fonctions import reduc_famille, appliq_reduc
from django.db import transaction
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

# formulaire d'aiguillage entre inscrition et réinscription
def intro_inscription(request):
    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    famille_match = True
    famille_inscrite = False
    code_famille = ""
    membres_famille = []
    page_html_suivante = "inscription/intro_inscription.html"

    # test de l'existence du code famille en base de données
    if request.method == 'POST':
        code_famille = request.POST['code_famille'].strip()

        if Famille.objects.filter(nom_famille=code_famille).count() == 1:
            famille_match = True
            # print ('famille connue')
            # si aucune ligne n'existe dans la table paiement pour la saison à venir, c'est que la famille n'estpas encore inscrite

            if Paiement.objects.filter(famille__nom_famille=code_famille, saison=saison_actuelle).count() == 0:
                # récupération des membres de la famille connue en base hors saison suf si déjà inscrite à la saison à venir
                query_set_mb_fam = Adherent.objects.values('nom_adh', 'prenom_adh', 'pk').filter(famille__nom_famille=code_famille)
                #query_set_mb_fam = Adherent.objects.filter(famille__nom_famille=code_famille)
                for mb in query_set_mb_fam:
                    # je crée un tableau père contenant des sous-tableaux fils, un sous-tableau pour chaque membre de la
                    # famille, le sous-tableau comortant le nom et l'id_adherent; le nom sera affiché et l'id_adherent
                    # sera l'id du checkbox
                    membre = []
                    membre.append(mb.get('prenom_adh').capitalize() + ' ' + mb.get('nom_adh').capitalize())
                    membre.append(str(mb.get('pk')))
                    # création du tableau père
                    membres_famille.append(membre)

                    page_html_suivante = "inscription/reinscription.html/"
            else:
                # famille déjà inscrite pour la saison à venir
                famille_inscrite = True
        else:
            famille_match = False

    context = {
        'saison_actuelle' : saison_actuelle,
        'famille_match' : famille_match,
        'famille_inscrite' : famille_inscrite,
        'code_famille' : code_famille,
        'membres_famille' : membres_famille,
    }
    return render(request, page_html_suivante, context )

# réinscription des adhérents
@transaction.atomic
def reinscription(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)

    cotis_adh = 0
    list_nom = ''
    list_discipline = ''
    list_cotisation = ''
    list_email = ''
    le_code_famille_svg = ''
    page_html_suivante = "inscription/reinscription2.html"

    # person_selected est un tableau contenant les id_adherent à réinscrire
    person_selected = request.POST.getlist('person_selected')
    # conservation en variable de session du nombre de personnes dans la famille
    nb_personnes = request.session.get('nb_personnes', 0)

    id_treated_person = person_selected[0]
    # print('id_treated_person', id_treated_person)

    # pour affichage du nom de l'adhérent à l'écran
    query_set_nom_adh = Adherent.objects.values('nom_adh', 'prenom_adh').filter(pk=id_treated_person)
    for mb in query_set_nom_adh:
        nom_adherent = mb.get('prenom_adh').capitalize() + ' ' + mb.get('nom_adh').capitalize()


    if "corrige" in request.POST:   # si la key "corrige" correspondant au bouton "Corriger mes données" est présent
        enabled = 'true'
        # print ("enabled activé")
        # person_selected = request.POST['person_selected']
        # print('person_selected dans corrige', person_selected)
        # print('type - person_selected dans corrige', type(person_selected))

    elif "inscrire" in request.POST:    # pour enregistrer les modifications en BDD si l'utilisateur a cliqué sur "modifier mes données"
        # récupération des infos adherent et contact en base de données
        info_adherent = Adherent.objects.get(pk=request.POST['id_treated_person'])
        info_contact = Contact.objects.get(adherent__pk=request.POST['id_treated_person'])

        # affichage des infos adherent et contact dans le formulaire
        formAdh = AdherentForm(request.POST or None, instance=info_adherent)
        formContact = ContactForm(request.POST or None, instance=info_contact)

        if not (formAdh.is_valid() and formContact.is_valid()):
            print("pb de formulaire")

        # si le formulaire a été rendu enabled
        if formAdh.is_valid() and formContact.is_valid() :
            # édition des mises à jour dans Adherent et Contact
            # test pour savoir si un nouveau contact a été saisi
            if Contact.objects.filter(nom_contact=request.POST['nom_contact'].strip(),
                                      prenom_contact=request.POST['prenom_contact'].strip()).count() == 0:
                # on crée un nouveau contact en base, on récupère son id et on fait le lien entre l'adhérent et le nouveau contact
                Contact.objects.create(nom_contact=request.POST['nom_contact'], prenom_contact=request.POST['prenom_contact'],
                                       email_contact=request.POST['email_contact'], numtel_contact1=request.POST['numtel_contact1'],
                                       numtel_contact2=request.POST['numtel_contact2'], numtel_contact3=request.POST['numtel_contact3']
                                       )

                # avant enregistrement de l'adhérent, récupération du contact associé
                newAdh = formAdh.save(commit=False)
                info_contact = Contact.objects.get(nom_contact=request.POST['nom_contact'].strip(),
                                                   prenom_contact=request.POST['prenom_contact'].strip(),
                                                   email_contact=request.POST['email_contact'].strip())
                newAdh.contact = info_contact
                # enregistrement de l'adhérent dans la table Adhérent
                formAdh.save()

            # si le contact existe déjà, on met à jour les données (numéro téléphone..)
            else :
                formContact.save()
                formAdh.save()

            # calcul age adhérent au 31 décembre de la saison suivante
            age_adherent = calcul_age_adh(request.POST['ddn'])

            if age_adherent < 18:   # la case "étudiant" ne peut être OUI
                if request.POST['etudiant'] == '1':
                    etudiant_verif = '0'
                else:
                    etudiant_verif = request.POST['etudiant']
            else:
                etudiant_verif = request.POST['etudiant']

            # récupération de la discipline choisie
            discipline = Discipline.objects.get(pk=request.POST['discipline'])

            # récupération du grade
            if request.POST['couleur'] != '':
                grade = Grade.objects.get(pk=request.POST['couleur'])
            else:
                grade = False

        # si le formulaire n'a pas été rendu enabled
        else:
            # calcul de l'âge (en créant une fonction) et récupération de l'info étudiant
            query_set_adh = Adherent.objects.values('ddn', 'etudiant').filter(pk=request.POST['id_treated_person'])
            for mb in query_set_adh:
                ddn = mb.get('ddn')
                etudiant_verif = mb.get('etudiant')
            ddn = ddn.strftime("%d/%m/%Y") # pour mettre au format %d/%m/%Y car dans la base le format est %Y-%m-%d
            age_adherent = calcul_age_adh(ddn)

            query_set_adh_saison = Adherent_Saison.objects.values('discipline', 'grade').\
                filter(adherent__pk=request.POST['id_treated_person'])
            for ads in query_set_adh_saison:
                discipline_id = ads.get('discipline')
                grade_id = ads.get('grade')
            # récupération de la discipline choisie
            discipline = Discipline.objects.get(pk=discipline_id)

            # récupération du grade
            if grade_id != None:
                grade = Grade.objects.get(pk=grade_id)
            else:
                grade = False

        # enregistrement en base de données
        # récupération de la catégorie de l'Adhérent (adulte, étudiant, enfant, ado, baby)
        categorie_adh = Categorie.objects.get(age_inf_catg__lte=age_adherent - 1, age_sup_catg__gte=age_adherent - 1,
                                              saison=saison_actuelle, etudiant=etudiant_verif)

        # récupération de la catégorie de combat
        categorie_combat = CategorieCombat.objects.get(age_min__lte=age_adherent, age_max__gte=age_adherent)

        # création de la ligne dans la table Adherent_saison
        if grade:
            Adherent_Saison.objects.create(adherent=info_adherent, saison=saison_actuelle,
                                           grade=grade, categorie=categorie_adh,
                                           categorie_combat=categorie_combat, discipline=discipline
                                           )
        else:
            Adherent_Saison.objects.create(adherent=info_adherent, saison=saison_actuelle,
                                           categorie=categorie_adh,
                                           categorie_combat=categorie_combat, discipline=discipline
                                           )

        # génération du Code Tarification qui permet d'aller chercher le tarif de l'adhérent selon son age et la discipline
        code_tarification = categorie_adh.code_catg + discipline.code_discipl
        # calcul de la cotisation pour l'adhérent et enregistrement en variable de session
        cotis_adh = int(calcul_cotis_adh(code_tarification, saison_actuelle, '1'))
        # création de la variable de session si elle n'existe pas
        cotis_adh_sum = request.session.get('cotis_adh_sum', 0)
        request.session['cotis_adh_sum'] = cotis_adh + int(cotis_adh_sum)
        #print(request.session['cotis_adh_sum'])

        # remplissage des listes nom des adhérents, discipline et cotsation de l'adhérent pour affichage en fin d'inscription
        list_nom = request.session.get('list_nom', '')
        if list_nom != '':
            # request.session['list_nom'] = list_nom + ',' + request.POST['nom_adh'] + ' ' + request.POST['prenom_adh']
            request.session['list_nom'] = list_nom + ',' + nom_adherent
        else:
            # request.session['list_nom'] = request.POST['nom_adh'] + ' ' + request.POST['prenom_adh']
            request.session['list_nom'] = nom_adherent
        #print('list_nom:', request.session['list_nom'])

        list_discipline = request.session.get('list_discipline', '')
        if list_discipline != '':
            request.session['list_discipline'] = list_discipline + ',' + discipline.nom_discipl
        else:
            request.session['list_discipline'] = discipline.nom_discipl
        #print('list_discipline:', request.session['list_discipline'])

        list_cotisation = request.session.get('list_cotisation', '0')
        if list_cotisation != '0':
            request.session['list_cotisation'] = list_cotisation + ',' + str(cotis_adh)
        else:
            request.session['list_cotisation'] = str(cotis_adh)
        #print('list_cotisation:', request.session['list_cotisation'])

        # récupération des adresses mail si l'adhérent les a modifiées
        #print ("id_treated_person après : ", id_treated_person)
        info_adherent_maj = Adherent.objects.get(pk=request.POST['id_treated_person'])
        info_contact_maj = Contact.objects.get(adherent__pk=request.POST['id_treated_person'])
        adher_email = info_adherent_maj.email_adh
        contact_email = info_contact_maj.email_contact

        #print("adher_email {} et contact_email {}".format(adher_email, contact_email))
        #print('list_email AVANT la fonction liste_dest_mail:', list_email)

        list_email = request.session.get('list_email', '')
        request.session['list_email'] = liste_dest_mail(list_email, age_adherent, adher_email, contact_email)
        #print('list_email APRES la fonction liste_dest_mail:', request.session['list_email'])

        request.session['nb_personnes'] = nb_personnes + 1
        enabled = 'false'

        # on passe à la personne suivante à inscrire s'il en reste une
        if len(person_selected) > 1:
            person_selected.remove(request.POST['id_treated_person'])
        else:
            # on passe à la page inscription_autre_membre.html pour permettre l'inscription d'un nouveau membre de la famille
            le_code_famille_svg = request.session['le_code_famille_svg']
            page_html_suivante = "inscription/inscription_autre_membre.html"

    # arrivée sur le formulaire pour la 1ère fois (en provenance de reinscription.html def intro_inscription)
    else:
        # mise en variable de session du code famille
        le_code_famille_svg = request.session.get('le_code_famille_svg', '')
        request.session['le_code_famille_svg'] = request.POST['code_famille'].strip()
        enabled = 'false'

    # après inscription en base de données, le 1er élément du tableau person_selected a été supprimé et on passe au prochain membre de la famille
    id_treated_person = person_selected[0]
    # pour affichage du nom de l'adhérent à l'écran
    query_set_nom_adh = Adherent.objects.values('nom_adh', 'prenom_adh').filter(pk=id_treated_person)
    for mb in query_set_nom_adh:
        nom_adherent = mb.get('prenom_adh').capitalize() + ' ' + mb.get('nom_adh').capitalize()

    # récupération des infos de l'adherent
    info_adherent = Adherent.objects.get(pk=id_treated_person)
    info_contact = Contact.objects.get(adherent__pk=id_treated_person)
    info_discipline = Discipline.objects.filter(adherent_saison__adherent=id_treated_person).\
        order_by('-adherent_saison__pk')[0] # ordonner par l'identifiant de table adherent_saison permet de sélectionner
                                            # la dernière saison enregistrée et [0] pour faire un SELECT TOP 1

    try:
        if Grade.objects.filter(adherent_saison__adherent=id_treated_person).exists():
            info_grade = Grade.objects.filter(adherent_saison__adherent=id_treated_person).\
                 order_by('-adherent_saison__pk')[0] # ordonner par l'identifiant de table adherent_saison permet de sélectionner
                                               # la dernière saison enregistrée et [0] pour faire un SELECT TOP 1
        else :
            info_grade = None

    except ObjectDoesNotExist:
        info_grade = None

    # affichage du fomulaire rempli
    formAdh = AdherentForm(instance=info_adherent)
    formContact = ContactForm(instance=info_contact)
    if enabled == 'true':
        # affiche la liste déroulante avec toutes les disciplines pour que l'adhérent fasse son choix
        formDiscipline = DisciplineForm()
        # affiche la liste déroulante avec tous les grades
        formGrade = GradeForm()
    else:
        # affiche la liste déroulante avec la discipline choisie la saison passée par l'adhérent
        formDiscipline = DisciplineFormSelected(instance=info_discipline)
        if info_grade:  # si le grade a été renseigné
            # affiche la liste déroulante avec le grade de l'adhérent la saison passée
            formGrade = GradeFormSelected(instance=info_grade)
        else:
            formGrade = GradeForm()

    context = {
        'saison_actuelle' : saison_actuelle,
        'person_selected' : person_selected,
        'id_treated_person' : id_treated_person,
        'nom_adherent' : nom_adherent,
        'code_famille': le_code_famille_svg,
        'formAdh': formAdh,
        'formGrade': formGrade,
        'formContact' : formContact,
        'formDiscipline': formDiscipline,
        'enabled' : enabled,

        'cotis_adh': cotis_adh,
        'nb_personnes': nb_personnes,
        'list_nom': list_nom,
        'list_discipline': list_discipline,
        'list_cotisation': list_cotisation,
        'list_email': list_email,
    }

    return render(request, page_html_suivante, context )

# inscription d'un autre membre de la famille et fin de réinscription
def fin_reinscription(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)
    cotis_adh = request.session["cotis_adh_sum"]
    nb_personnes = request.session['nb_personnes']

    list_nom = request.session['list_nom']
    list_discipline = request.session['list_discipline']
    list_cotisation = request.session['list_cotisation']
    le_code_famille_svg = request.session['le_code_famille_svg']
    list_email = request.session['list_email']

    # nécessaire pour afficher le formulaire d'inscription vide pour le nouveau membre
    formAdh = AdherentForm()
    formGrade = GradeForm()
    formContact = ContactForm()
    formDiscipline = DisciplineForm()

    # l'utilisateur a cliqué sur le bouton Non (pas d'inscription d'un autre membre de la famille), on passe à la
    # finalisation de l'inscription
    if "non" in request.POST:

        # récupération du taux de réduction valable pour la famille
        taux_reduc = reduc_famille(request.session['nb_personnes'], 1, saison_actuelle)
        cotis_adh = appliq_reduc(taux_reduc, request.session['cotis_adh_sum'])

        # enregistrement montant de la cotisation dans la table Paiement
        info_famille = Famille.objects.get(nom_famille=le_code_famille_svg)
        Paiement.objects.create(famille=info_famille, saison=saison_actuelle, montant_cotis=cotis_adh)

        list_nom = request.session['list_nom'].split(',')
        list_discipline = request.session['list_discipline'].split(',')
        list_cotisation = request.session['list_cotisation'].split(',')
        le_code_famille_svg = request.session['le_code_famille_svg']
        list_email = request.session['list_email'].split(',')

        # print("liste des mails envoyés par messagerie:" , list_email)
        # envoi du mail de synthèse en utilisant le mail choisi pour recevoir les infos
        envoi_mail(list_nom, list_discipline, list_cotisation, cotis_adh, le_code_famille_svg, list_email)

        page_html_suivante = "inscription/fin_inscription.html"
    else :
        # l'utilisateur veut inscrire une nouvelle personne
        page_html_suivante = "inscription/inscription.html"

    # suppression des variables de session
    del request.session['cotis_adh_sum']
    del request.session['list_nom']
    del request.session['list_discipline']
    del request.session['list_cotisation']
    del request.session['nb_personnes']
    del request.session['le_code_famille_svg']
    del request.session['list_email']

    context = {
        'saison_actuelle': saison_actuelle,
        'code_famille': le_code_famille_svg,
        'cotis_adh': cotis_adh,
        'nb_personnes': nb_personnes,
        'list_nom': list_nom,
        'list_discipline': list_discipline,
        'list_cotisation': list_cotisation,
        'list_email': list_email,

        'formAdh': formAdh,
        'formGrade': formGrade,
        'formContact': formContact,
        'formDiscipline': formDiscipline,
    }

    return render(request, page_html_suivante, context )

# inscription de nouveaux adhérents
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
    list_email = ''

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
                code_famille = crea_code_famille(request.POST['nom_adh'].strip())
                # création d'une nouvelle ligne dans la table Famille
                Famille.objects.create(nom_famille=code_famille)
                # Récupération de la ligne nouvellement insérée dans Famille
                info_famille = Famille.objects.get(nom_famille=code_famille)
            else:
                #print("code famille connu :", request.POST['code_famille'])
                code_famille = request.POST['code_famille'].strip()
                info_famille = Famille.objects.get(nom_famille=request.POST['code_famille'].strip())

            # enregistrement du contact
            if request.POST['code_famille'].strip() == '':
                # enregistrement du contact dans la base Contact
                formContact.save()
            else:
                # test pour savoir si le contact existe déjà en base
                if Contact.objects.filter(nom_contact=request.POST['nom_contact'].strip(),
                                                   prenom_contact=request.POST['prenom_contact'].strip(),
                                                       email_contact = request.POST['email_contact'].strip()).count() == 0:
                    formContact.save()

            # avant enregistrement de l'adhérent, récupération du contact associé
            newAdh = formAdh.save(commit=False)
            info_contact = Contact.objects.get(nom_contact=request.POST['nom_contact'].strip(),
                                             prenom_contact=request.POST['prenom_contact'].strip(),
                                            email_contact = request.POST['email_contact'].strip())
            newAdh.contact = info_contact
            newAdh.famille = info_famille
            # enregistrement de l'adhérent dans la table Adhérent
            formAdh.save()

            # récupération des infos adhérent de la table Adherent
            info_adherent = Adherent.objects.get(nom_adh=request.POST['nom_adh'].strip(), prenom_adh=request.POST['prenom_adh'].strip())

            # calcul age adhérent au 31 décembre de la saison suivante
            ddn_split = request.POST['ddn'].split('/')
            age_adherent = int((date.today().year + 1)) - int(ddn_split[2])

            if age_adherent < 18:   # la case "étudiant" ne peut être OUI
                if request.POST['etudiant'] == '1':
                    etudiant_verif = '0'
                else:
                    etudiant_verif = request.POST['etudiant']
            else:
                etudiant_verif = request.POST['etudiant']

            # récupération de la catégorie de l'Adhérent (adulte, étudiant, enfant, ado, baby)
            categorie_adh = Categorie.objects.get(age_inf_catg__lte=age_adherent-1, age_sup_catg__gte=age_adherent-1,
                                                           saison=saison_actuelle, etudiant=request.POST['etudiant'])

            # récupération de la catégorie de combat
            categorie_combat = CategorieCombat.objects.get(age_min__lte=age_adherent, age_max__gte=age_adherent)
            #print(' categorie combat : {} et age : {} '.format(categorie_combat, age_adherent))

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
                list_nom = list_nom + ',' + request.POST['nom_adh'].strip() + ' ' + request.POST['prenom_adh'].strip()
            else:
                list_nom = request.POST['nom_adh'].strip() + ' ' + request.POST['prenom_adh'].strip()

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

            list_email = request.POST['list_email']
            list_email = liste_dest_mail(list_email, age_adherent, request.POST['email_adh'].strip(),
                                                                request.POST['email_contact'].strip())
            #print("list_email : ", list_email)

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
                    list_email = list_email.split(',')

                else:   # je demande à spliter sur "*" pour garder les mots ensemble
                    list_nom = list_nom.split('*')
                    list_discipline = list_discipline.split('*')
                    list_cotisation = list_cotisation.split('*')
                    list_email = list_email.split('*')

                # enregistrement montant de la cotisation dans la table Paiement
                Paiement.objects.create(famille=info_famille, saison=saison_actuelle, montant_cotis=cotis_adh)

                page_html_suivante = "inscription/fin_inscription.html"

                # print("list_email avant envoi des mails: ", list_email)
                # envoi du mail de synthèse en utilisant le mail choisi pour recevoir les infos
                envoi_mail(list_nom, list_discipline, list_cotisation, cotis_adh, code_famille, list_email)

            else:
                page_html_suivante = "inscription/inscription.html"
                formAdh = AdherentForm(initial={"adresse":request.POST['adresse'].strip(),"cp":request.POST['cp'].strip(),
                                                "ville":request.POST['ville'].strip()})
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
        'list_email' : list_email,
    }

    return render(request, page_html_suivante, context )


