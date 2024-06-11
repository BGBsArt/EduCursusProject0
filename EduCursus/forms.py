from django.core import validators
from django import forms
from django.forms import fields, widgets
# from django.contrib.auth.forms import UserCreationForm
from .models import Administrateur, Cursus

"""
class Senregistrer(forms.ModelForm):
    # forms.CharField --- Chaine de caracteres
    # label --- L'etiquette du champs de mot de passe
    # strip --- Pour désactiver la supression automatique des espaces autour du mot de passe

    S'il y avait de mot de passe
        password = forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
    Le password sera forcément caché puis 'render_value=True' nous permet de voir le mot de passe
    avant de le modifier sur une page admin.

    matricule = forms.CharField(    
        label = "Matricule ",     
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Entrez le numéro matricule de l'apprenant"}),
        max_length = 30,
        required=True,
        help_text="Il est unique. Ne faites surtout pas erreur de saisi !",
    )
    nom = forms.CharField(    
        label = "Nom ",     
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Entrez son nom"}),
        max_length = 30,
        required=True,
        # help_text='required.',
    )
    prenom = forms.CharField(    
        label = "Prénoms ",     
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Entrez son prénom(s)"}),
        max_length = 30,
        required=True,
        help_text= "Saisir l'intégrlité du prénom de l'apprenant svp.",
    )
    entite = forms.CharField(    
        label = "Entité/Ecole ",     
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Sous forme de sigle"}),
        max_length = 30,
        required=True,
        help_text="(ex : EPAC/FASHS/ISM Adonai/CEG Toui)",
    )
    filiere = forms.CharField(    
        label = "Filière Générale/Classe ",     
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        max_length = 30,
        required=True,
        help_text="(ex : SI/Philsophie/Marketing/4eme/Tle)",
    )
    
    class Meta :    # Pour personnaliser les options du formulaire (On ajoute juste pw1 et pw2)
        model = Administrateur
        fields = ['matricule', 'nom', 'prenom', 'entite', 'filiere']

class CursusInform(forms.ModelForm):

    annee = forms.CharField(    
        label = "Année Scolaire/Académique ",     
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        max_length = 30,
        required=True,
        help_text="(ex : 2023-2024)",
    )
    note = forms.CharField(    
        label = "Moyenne de fin d'année",     
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        max_length = 30,
        required=True,
        help_text="(ex : 13.77)",
    )
    mention = forms.CharField(    
        label = "Mention ",     
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        max_length = 30,
        required=True,
        help_text= "(ex : Assez bien)",
    )

    class Meta :    # Pour personnaliser les options du formulaire (On ajoute juste pw1 et pw2)
        model = Cursus
        fields = ['annee', 'note', 'mention']
"""