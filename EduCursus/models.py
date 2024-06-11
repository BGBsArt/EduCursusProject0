from django.db import models
import django.utils.timezone

# Dans AbstractUser se trouve le champ 'last_login' (qui permet de tracer l'historique de connexion réussie)
from django.contrib.auth.models import Group, Permission, AbstractUser


# Create your models here.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Table qui stocke les informations des utilisateurs (apprenants, enseignants, parents, tout individu)
class User(models.Model):
    username = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Table qui stocke les informations des différents établissements
class AdminRegister(models.Model):
    etablissement = models.CharField(max_length=100)
    codeid = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    commune = models.CharField(max_length=50)
    school = models.CharField(max_length=50)

    # Nous ajoutons ces champs au lieu d'hériter les methodes de la classe 'AbstractUser' de "django.contrib.auth.models" pour des raisons spécifiques
    # 'AbstractUser' nous fournira par exemple le username, first et last, password qui ne sont pas nécessaire ici.
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    date_joined = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')

    """ Nous ajoutons ces deux chmaps pour tenter de regler le probleme des probables conflits entre les relations ManyToMany des
        modeles User et AdminRegister. Ces relations permettent à un utilisateur d'appartenir à plusieurs groupes et d'avoir plusieurs permissions.
    """
    groups = models.ManyToManyField(Group, related_name="adminregister_set")
    user_permissions = models.ManyToManyField(Permission, related_name="adminregister_set")

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Table qui stocke l'inscription des apprenants de chaque établissement
class Administrateur(models.Model):
    matricule = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    entite = models.CharField(max_length=50)
    filiere = models.CharField(max_length=50)
    mesApprenants = models.ForeignKey(AdminRegister, on_delete=models.CASCADE, related_name="adminstra")

    # On aura la creation de du fichier administrateur_set par django à cause de la clé étrangère

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Table qui stocke le cursus de chaque apprenant dans chaque établissement
class Cursus(models.Model):
    filiereEnCours = models.CharField(max_length=30)
    annee = models.CharField(max_length=9)
    note = models.DecimalField(max_digits=4, decimal_places=2)
    mention = models.CharField(max_length=10)
    administrateurs = models.ManyToManyField(Administrateur, related_name='cursus') 
    letablissement = models.ForeignKey(AdminRegister, on_delete=models.SET_NULL, null=True, related_name="cet_etablissement")

# Ce champ est une clé étrangère référent au modele 'Administrateur'

"""
"ForeignKey" est une relation avec le modele 'Administrateur'
Cette relation est de type "many-to-one", signifiant qu'un apprenant d 'Administrateur'
peut avoir plusieurs 'Cursus', mais chaque 'Cursus' appartient à un 'Administrateur' (ici le modele quoi).

on_delete=models.CASCADE ---> permet de supprimer le 'Cursus' si un apprenant est delete dans 'Administrateur'
A cet effet, django crée un attribut 'cursus_set' pour 'Administrateur'. Il permet d'acceder à tous les Cursus
associé à un apprenant dans la table 'Administrateur'.
"""

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Table intermédiaire pour gerer les associations du cadre de ManyToMany. Nous creeons cette classe pour pouvoir vérifier l'existance
#  d'une association spécifique, l'exemple de 'annee' qui represente techniquement ici 'année Académique ou Scolaire'.

class AddAssociation(models.Model) :
    administrateur = models.ForeignKey(Administrateur, on_delete=models.CASCADE)
    cursus = models.ForeignKey(Cursus, on_delete=models.CASCADE)
    annee = models.CharField(max_length=9)

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
    
    
    
    
              
              
