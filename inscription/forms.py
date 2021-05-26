from django import forms
from inscription.models import Adherent, Grade, Contact, Famille
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
    couleur = forms.ModelChoiceField(queryset=Grade.objects.all().order_by('-keup'))
    class Meta:
        model = Grade
        fields =  ['couleur',]


class CategorieForm(forms.ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all().order_by('ordre_affichage'))

    class Meta:
        model = Categorie
        fields = ['categorie', ]


class DisciplineForm(forms.ModelForm):
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all().order_by('ordre_affichage'))

    class Meta:
        model = Discipline
        fields = ['discipline', ]


