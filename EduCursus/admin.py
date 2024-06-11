from django.contrib import admin
from .models import Administrateur, Cursus, AdminRegister

# Register your models here.

"""

@admin.register(Administrateur)

class AdminAjout(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'entite', 'filiere')
    # list_display = ('annee', 'note', 'mention')
"""
