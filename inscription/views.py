from django.shortcuts import render
from inscription.forms import AdherentForm, GradeForm, ContactForm, CategorieForm, DisciplineForm
from inscription.models import Contact, Adherent, Famille
from cotisation.models import Saison
from inscription.fonctions import crea_code_famille
from django.db import transaction


@transaction.atomic
def inscription(request):

    saison_actuelle = Saison.objects.get(saison_actuelle=True)

    if request.method == 'GET':
        #print('méthode get')
        formAdh = AdherentForm()
        formGrade = GradeForm()
        formContact = ContactForm()
        formCategorie = CategorieForm()
        formDiscipline = DisciplineForm()

    else :
        #print('méthode post')
        formAdh = AdherentForm(request.POST)
        formGrade = GradeForm(request.POST)
        formContact = ContactForm(request.POST)
        formCategorie = CategorieForm(request.POST)
        formDiscipline = DisciplineForm(request.POST)

        if formAdh.is_valid() and formGrade.is_valid() and formContact.is_valid()\
                and formCategorie.is_valid() and formDiscipline.is_valid():

            # création d'un code famille pour regrouper les adhérents d'une même famille
            code_famille = crea_code_famille(request.POST['nom_adh'])
            # création d'une nouvelle ligne dans la table Famille
            newFamille = Famille.objects.create(nom_famille=code_famille)
            # Récupération de la clef de la ligne nouvellement insérée
            info_famille = Famille.objects.get(nom_famille=code_famille)

            formContact.save()
            newAdh = formAdh.save(commit=False)
            info_contact = Contact.objects.get(nom_contact=request.POST['nom_contact'],
                                             prenom_contact=request.POST['prenom_contact'], )
            newAdh.contact = info_contact
            newAdh.famille = info_famille
            formAdh.save()

        else:
            print("formulaire non valide")


    context = {
        'saison_actuelle': saison_actuelle,
        'formAdh': formAdh,
        'formGrade': formGrade,
        'formContact' : formContact,
        'formCategorie' : formCategorie,
        'formDiscipline' : formDiscipline,
    }

    return render(request, 'inscription/inscription.html', context )
