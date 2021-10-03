from django import forms

class AuthentifForm(forms.Form):
    email_auth = forms.EmailField(label="Adresse email")
    code_famille = forms.CharField(label="Code famille (*)")

