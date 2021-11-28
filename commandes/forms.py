from django import forms

class AuthentifForm(forms.Form):
    email_auth = forms.EmailField(label="Adresse email")
    pwd = forms.CharField(label="Mot de passe")

