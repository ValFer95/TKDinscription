from django.shortcuts import render
from inscription.forms import AdherentForm, GradeForm, ContactForm, CategorieForm, DisciplineForm
from inscription.models import Contact, Adherent, Famille, Adherent_Saison, CategorieCombat, Grade
from cotisation.models import Saison, Categorie, Discipline
from inscription.fonctions import crea_code_famille
from django.db import transaction
from datetime import date


@transaction.atomic
def inscription(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)

    if request.method == 'GET':
        #print('méthode get')
        formAdh = AdherentForm()
        formGrade = GradeForm()
        formContact = ContactForm()
        # formCategorie = CategorieForm()
        formDiscipline = DisciplineForm()

    else :
        #print('méthode post')
        formAdh = AdherentForm(request.POST)
        formGrade = GradeForm(request.POST)
        formContact = ContactForm(request.POST)
        # formCategorie = CategorieForm(request.POST)
        formDiscipline = DisciplineForm(request.POST)

        if formAdh.is_valid() and formGrade.is_valid() and formContact.is_valid()\
                 and formDiscipline.is_valid():     # and formCategorie.is_valid()

            # création d'un code famille pour regrouper les adhérents d'une même famille
            code_famille = crea_code_famille(request.POST['nom_adh'])
            # création d'une nouvelle ligne dans la table Famille
            Famille.objects.create(nom_famille=code_famille)
            # Récupération de la clef de la ligne nouvellement insérée
            info_famille = Famille.objects.get(nom_famille=code_famille)

            # enregistrement du contact dans la base Contact
            formContact.save()

            # avant enregistrement de l'adhérent, récupération du contact associé
            newAdh = formAdh.save(commit=False)
            info_contact = Contact.objects.get(nom_contact=request.POST['nom_contact'],
                                             prenom_contact=request.POST['prenom_contact'], )
            newAdh.contact = info_contact
            newAdh.famille = info_famille
            # enregistrement de l'adhérent dans la table Adhérent
            formAdh.save()

            # enregistrement des infos adhérent dans la table Adherent_Saison
            info_adherent = Adherent.objects.latest('nom_adh', 'prenom_adh')

            # calcul age adhérent au 31 décembre de la saison suivante
            ddn_split = request.POST['ddn'].split('/')
            age_adherent = int((date.today().year + 1)) - int(ddn_split[2])

            # récupération de la catégorie de l'Adhérent (adulte, étudiant, enfant, ado, baby)
            categorie_adh = Categorie.objects.get(age_inf_catg__lte=age_adherent-1, age_sup_catg__gte=age_adherent-1,
                                                           etudiant=request.POST['etudiant'])

            # récupération de la catégorie de combat
            categorie_combat = CategorieCombat.objects.get(age_min__lte=age_adherent, age_max__gte=age_adherent)

            # récupération du grade
            grade = Grade.objects.get(pk=request.POST['couleur'])

            # récupération de la discipline choisie
            discipline = Discipline.objects.get(pk=request.POST['discipline'])

            # enregistrement des infos Adhérent en base de données Adherent_Saison
            Adherent_Saison.objects.create(adherent=info_adherent, saison= saison_actuelle,
                                           grade=grade, categorie=categorie_adh,
                                           categorie_combat=categorie_combat, discipline=discipline
                                           )


        else:
            print("formulaire non valide")


    context = {
        'saison_actuelle': saison_actuelle,
        'formAdh': formAdh,
        'formGrade': formGrade,
        'formContact' : formContact,
        # 'formCategorie' : formCategorie,
        'formDiscipline' : formDiscipline,
    }

    return render(request, 'inscription/inscription.html', context )
