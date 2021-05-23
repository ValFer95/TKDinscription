from django import forms

class SimulCotisForm(forms.Form):
    CHOICES = [('0', 'Non'), ('1', 'Oui')]
    reinscription = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial=0)

    adultTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    adultBodyTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    adultFem = forms.IntegerField(required=False, min_value=0, max_value=9)

    etudTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    etudBodyTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    etudFem = forms.IntegerField(required=False, min_value=0, max_value=9)

    adoTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    adoBodyTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    adoFem = forms.IntegerField(required=False, min_value=0, max_value=9)

    enfTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
    enfBodyTKD = forms.IntegerField(required=False, min_value=0, max_value=9)

    babyTKD = forms.IntegerField(required=False, min_value=0, max_value=9)
