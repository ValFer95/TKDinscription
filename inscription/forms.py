from django import forms
from django.http import request
from inscription.models import Adherent, Grade, Contact, Famille, Adherent_Saison
from cotisation.models import Saison, Categorie, Discipline

class AdherentForm(forms.ModelForm):
    class Meta:
        model = Adherent
        # fields = '__all__'
        exclude = ('contact', 'famille')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class GradeForm(forms.ModelForm):
    couleur = forms.ModelChoiceField(queryset=Grade.objects.all().order_by('-keup'), required=False)
    class Meta:
        model = Grade
        fields =  ['couleur',]


# pour affichage du grade de l'adhérent la saison passée (au moment de la réinscription)
class GradeFormSelected(forms.ModelForm):
    class Meta:
        model = Grade
        exclude = ('keup',)


class DisciplineForm(forms.ModelForm):
    # discipline = forms.ModelChoiceField(queryset=Discipline.objects.all().order_by('ordre_affichage').distinct())
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.filter(saison__saison_actuelle=True).order_by('ordre_affichage'))
    class Meta:
        model = Discipline
        fields = ['discipline', ]


# pour affichage de la liste déroulante avec la discipline choisie par l'adhérent la saison passée (au moment de la réinscription)
class DisciplineFormSelected(forms.ModelForm):
    class Meta:
        model = Discipline
        exclude = ('ordre_affichage', 'saison')
