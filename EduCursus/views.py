from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import Administrateur, Cursus, AdminRegister, AddAssociation
# from .forms import Senregistrer
from django.db import models    # Modele où on a utilisé la requete Q
# from django.core.exceptions import ValidationError
# from socket import gaierror, getaddrinfo
from django.urls import reverse

from EduCursusProject import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage

# Create your views here.

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction qui affiche la page basique, la premiere page, la vue tout internaute
def indexhome(request) :
    # return HttpResponse("Bonjour tout le monde")
    return render(request, 'app/index.html')

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction qui affiche tous les parcours dans chaque établissement de l'apprenant recherché par l'utilisateur connecté
def lookcursus(request, nom, prenom):
    # Récupération de l'apprenant unique basé sur nom et prenom de l'administrateur (apprenant)
    try :
        apprenant = Administrateur.objects.filter(nom=nom, prenom=prenom)
    except Administrateur.DoesNotExist :
        messages.info(request, "Votre requete n'existe pas.")
        return render(request, 'app/lookCursus.html')

    return render(request, 'app/lookCursus.html', {'apprenants': apprenant})


"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction qui affiche la premiere page de connexion reussie d'un administrateur connecté
def adminconnecter(request, user_id) :
            
    return render(request, 'app/adminConnecter.html', {'user':AdminRegister.objects.get(id=user_id)})

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux administrations de renseigner le parcours d'un apprenant déja enregistré dans la BD 
def cursusInform(request, id) :
    if request.method == 'POST':
        filiereEnCours = request.POST['filiereEnCours']
        annee = request.POST['annee']
        note = request.POST['note']
        mention = request.POST['mention']

        try :
            apprenant = Administrateur.objects.get(pk=id)  # pk(primary key) Nous allons acceder à chaque apprenant via son 'id' par defaut dans la BD (l'ordre d'enregistrement)
            etablissement = apprenant.mesApprenants
        except Administrateur.DoesNotExist :
            return redirect('adminPage')
    
        # Verification de l'existence d'une association avec l'année académique associée
        if AddAssociation.objects.filter(administrateur=apprenant, cursus__annee=annee).exists() :
            messages.error(request, "Cette année Scolaire/Académique existe déjà pour cet apprenant. Vous ne pouvez plus l'ajouter.")
            return render(request, 'app/cursus.html', {'user':etablissement, 'apprenant':ap})
        
        # Dans le champs de la clé etrangère dans le modele Cursus, on défini le champ 'NULL',
        # Pour eviter ceci lors de l'ajout d'un cursus, on lui colle en meme temps l'id de l'établissement (AdminRegister)
        # letablissement = AdminRegister.objects.get(id=id)

        cursus = Cursus(filiereEnCours=filiereEnCours, annee=annee, note=note, mention=mention)
        cursus.save()

        # Assoviation du cursus à L'Adminstrateur (apprenant)
        cursus.administrateurs.add(apprenant)
        
        messages.success(request, 'Cursus ajouté avec succès !')        
        return render(request, 'app/cursus.html', {'user':etablissement, 'apprenant':apprenant.cursus.all()})

    
    apprenant = Administrateur.objects.get(pk=id)
    
    # Nous accedons a l'établissement associé à cet apprenant dans Administrateur à travers la clé étrangere 'mesApprenants'
    etablissement = apprenant.mesApprenants     # ==> 'user':AdminRegister.objects.get(id=id)

    return render(request, 'app/cursus.html', {'apprenant':apprenant.cursus.all(), 'user':etablissement})


"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux administrations d'ajouter des apprenants, modifier et meme supprimer.
# Sont aussi capables d'inscrire le cursus des apprenants à travers le bouton 'cursus' (voir adminPage.html)
def adminPage(request, id):
    if request.method == "POST":
        matricule = request.POST['matricule']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        entite = request.POST['entite']
        filiere = request.POST['filiere']

        try :
            mesApprenants = AdminRegister.objects.get(pk=id)     # Nous accedons à chaque établissement
            ap = mesApprenants.adminstra.all()
        except AdminRegister.DoesNotExist :
            messages.error(request, "Cet établissement n'existe pas.")
            return redirect('adminLogin')
        
        #ap = mesApprenants.adminstra.all()
        if mesApprenants.adminstra.filter(nom=nom) and mesApprenants.adminstra.filter(prenom=prenom) or mesApprenants.adminstra.filter(matricule=matricule):
            messages.error(request, "Cet apprenant est déjà dans la base de données.")
            return render(request, 'app/adminPage.html', {'user':AdminRegister.objects.get(id=id), 'mesApprenants':ap})
        if not matricule.isdigit():
            messages.error(request, "Le numéro matricule doit contenir uniquement des chiffres ([0-9]).")
            return render(request, 'app/adminPage.html', {'user':AdminRegister.objects.get(id=id), 'mesApprenants':ap})

        # Verication des champs du formulaire
        my_user = Administrateur(matricule=matricule, nom=nom, prenom=prenom, entite=entite, filiere=filiere, mesApprenants=mesApprenants)

        my_user.save()
        messages.success(request, 'Apprenant maintenant ajouté.')

        ap = mesApprenants.adminstra.all()
        return render(request, 'app/adminPage.html', {'user':AdminRegister.objects.get(id=id), 'mesApprenants':ap})

    mesApprenants = AdminRegister.objects.get(pk=id)
    ap = mesApprenants.adminstra.all()
    
    return render(request, 'app/adminPage.html', {'user':AdminRegister.objects.get(id=id), 'mesApprenants':ap})

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux administrations de s'enregistrer 
def adminAdd(request) :
    if request.method == "POST":

        # On crée une instance du modele de la classe AdminRegister
        # adminregister = AdminRegister()

        etablissement = request.POST['etablissement']
        codeid = request.POST['codeid']
        email = request.POST['email']
        city = request.POST['city']
        commune = request.POST['commune']
        school = request.POST['school']

        # Verication des champs du formulaire
        if AdminRegister.objects.filter(codeid=codeid) :
            messages.error(request, "Cet établissement existe déjà.")
            return redirect('adminAdd')
        if not codeid.isdigit() : # numerique/chiffres
            messages.error(request, "L'ID de votre établissement doit contenir que de chiffres, entre 0 et 9).")
            return redirect('adminAdd')
        if AdminRegister.objects.filter(email=email) :
            messages.error(request, "Cet email a déjà une administration.")
            return redirect('adminAdd')

        my_user = AdminRegister(etablissement=etablissement, codeid=codeid, email=email, city=city, commune=commune, school=school)
        # Creation d'une nouvelle instance de UserAdmin
        my_user.save()
        messages.success(request, 'Votre établissement a été enregistré avec succès. Ouvrez votre messagerie Gmail, nous y avons envoyé un code de 6 chiffres.')
        return redirect('adminLogin')
        
    return render(request, 'app/adminAdd.html')

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux utilisateurs de s'inscrire à la plateforme 
def register(request) :
    # Si la requete est de type POST, recois les données
    if request.method == "POST" :
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        # Verication des champs du formulaire
        if User.objects.filter(username=username) :
            messages.error(request, "Cet nom d'utilisateur existe déjà.")
            return redirect('register')
        if User.objects.filter(email=email) :
            messages.error(request, "Cet email a déjà un compte.")
            return redirect('register')
        if not username.isalnum() : # alphanumerique
            messages.error(request, "Le nom d'utilisateur doit etre alphanumérique ([A-Z,a-z] et [0-9]).")
            return redirect('register')
        if password != password1 :
            messages.error(request, "Erreur. Entrez le meme mot de passe SVP !")
            return redirect('register')
        
        # Si tout est respecté, enregistre et stocke les données dans la BD
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname

        
        my_user.is_active = False
        my_user.save()
        messages.success(request, 'Votre compte a été crée avec succès. Ouvrez votre messagerie Gmail pour confirmer votre adresse !')
        
        try :
            # Configuration et envoie de message de bienvenu par email(info.py)
            subject = "Bienvenu sur EduCursus !"
            message = " Bienvenu Mme/M. " + my_user.first_name + " " + my_user.last_name + "\n Nous sommes heureux de vous compter parmi nous.\n\n\n Merci.\n\n ---> L'équipe EduCursus" 

            from_email = settings.EMAIL_HOST_USER
            to_list = [my_user.email]       # On peut send à plusieurs adresses, ici on spécifie l'adresse email de celui qui s'enregistre maintenant
            send_mail(subject, message, from_email, to_list, fail_silently=False)       # fail_silently=False (S'il y a une erreur, notifie la-->False)


            # Email de confirmation
            current_site = get_current_site(request)
            email_subject = "Confirmation de l'adresse email sur EduCursus"
            
            # Le message de confirmation d'email sera envoyé sous forme de fichier
            confirmMessage = render_to_string("emailConfirm.html", {
                "name" : my_user.first_name,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(my_user.pk)),
                'token' : generatorToken.make_token(my_user),
            })      # Fonction qui fait tout en fait
            
            email = EmailMessage(
                email_subject,
                confirmMessage,
                settings.EMAIL_HOST_USER,
                [my_user.email]
            )
            
            email.fail_silently = False
            email.send()
            return redirect('login')

        except(Exception) as e :
            messages.error(request, " Envoi d'email échoué. Vérifiez votre connexion internet SVP !")
            redirect('register')
        
    return render(request, 'app/register.html')


"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux utilisateurs de se connecter à l'espace utilisateur avec leur username et password
def logIn(request) :
    if request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # mon_user = User.objects.get(username=username)
        
        if user is not None :
            login(request, user)
            firstname = user.first_name
            # request.session['est_connecte'] = True
            return render(request, 'app/home.html', {'firstname' : firstname})

        # elif mon_user.is_active == False :
            # messages.error(request, "Vous n'avez pas confirmé votre adresse email. Aidez nous à savoir s'il s'agit bien de vous avant de vous connecter. Merci.") 
        
        else:
            messages.error(request, "Si vous avez un compte chez nous \n1. Soit votre nom d'utilisateur ou mot de passe est incorrect.\n\n2. Soit vous n'avez pas confirmé votre adresse email. Aidez nous à savoir s'il s'agit bien de vous avant de vous connecter. Merci.")
            return redirect('login')

    return render(request, 'app/login.html')

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux administrations de se connecter à leur espace ADMIN
def adminLogin(request) :
    if request.method == "POST" :
        email = request.POST['email']

        try :
            # Si l'email correspond, conneter l'utilisateur
            user = AdminRegister.objects.get(email=email)
            if user is not None :
                login(request, user)

                etablissement = user.id
                messages.success(request, "Connexion réussie.")
                # request.session['est_connecte'] = True
                return render(request, "app/adminConnecter.html", {'etablissement': etablissement})
            
        except AdminRegister.DoesNotExist :
            messages.error(request, "L'adresse email incorrect.")
            redirect('adminLogin')
    
    return render(request, 'app/adminLogin.html')

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux utilisateurs de se deconnecter 
def log0ut(request) :
    # pass
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('indexhome')

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux administrations de suprimer dans la BD un apprenant déja enregistré
def delecteStud(request, delete_id) :
    if request.method == 'POST':
        try :
            stud_a_supprimer = Administrateur.objects.get(pk=delete_id)  # pk(primary key) Nous allons acceder à chaque apprenant via son 'id' par defaut dans la BD (l'ordre d'enregistrement)
            stud_a_supprimer.delete()
            messages.success(request, 'Apprenant supprimé avec succès !')
        except Administrateur.DoesNotExist :
            messages.info(request, "Cet apprenant n'existe dans la base de données.")

        try:
            # Nous accedons à un l'object Administrateur (un apprenant), par son AdminRegister(un établissemnt) asoccié 
            etablissement = stud_a_supprimer.mesApprenants
        except models.DoesNotExist :
            messages.info(request, "Pas d'établissement de ce nom.")

        # Vu qu'on retourne à la page 'adminPage', on passe en argument l'id de l'établissement associé à l'apprenant
        # Ceci nous évitera l'erreur 'NoReverseMatch de django
        return redirect(reverse('adminPage', args=[etablissement.id]))

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux administrations de modifier les données dans la BD d'un apprenant déja enregistré
def updateData(request, update_id) :
    if request.method == 'POST':
        try:
            # Récupérer l'instance de l'apprenant à mettre à jour
            student_a_modifier = Administrateur.objects.get(pk=update_id)  # pk(primary key) Nous allons acceder à chaque apprenant via son 'id' par defaut dans la BD (l'ordre d'enregistrement)
            
            # Récupérer les nouvelles informations de l'apprenant à partir du formulaire
            new_matricule = request.POST.get("new_matricule")
            new_nom = request.POST.get("new_nom")
            new_prenom = request.POST.get("new_prenom")
            new_entite = request.POST.get("new_entite")
            new_filiere = request.POST.get("new_filiere")

            # Mettre à jour les informations de l'apprenant
            if new_matricule:
                student_a_modifier.matricule = new_matricule
            if new_nom:
                student_a_modifier.nom = new_nom
            if new_prenom:
                student_a_modifier.prenom = new_prenom
            if new_entite:
                student_a_modifier.entite = new_entite
            if new_filiere:
                student_a_modifier.filiere = new_filiere

            student_a_modifier.save()
            messages.success(request, 'Informations de l\'apprenant mis à jour avec succès !')

            etablissement = student_a_modifier.mesApprenants

            # Rediriger vers la page d'administration après la mise à jour
            return redirect(reverse('adminPage', args=[etablissement.id]))

        except Administrateur.DoesNotExist:
            messages.error(request, "Cet apprenant n'existe pas dans la base de données.")

    # Si la requête n'est pas une requête POST, cela signifie qu'on doit afficher le formulaire
    else:
        # On passe l'ID de l'apprenant au template pour remplir automatiquement le formulaire avec les informations actuelles
        student = Administrateur.objects.get(pk=update_id)
        
        student_a_modifier = Administrateur.objects.get(pk=update_id)
        etablissement = student_a_modifier.mesApprenants
        #return redirect(reverse('adminPage', {'user':Administrateur.objects.get(id=update_id), 'student': student}, args=[etablissement.id]))
        return render(request, 'app/updateStudent.html', {'user':Administrateur.objects.get(id=update_id), 'student': student, 'etablissement':etablissement})

    """
    if request.method == 'POST':
        modifier = Administrateur.objects.get(pk=id)  # pk(primary key) Nous allons acceder à chaque apprenant via son 'id' par defaut dans la BD (l'ordre d'enregistrement)
        fm = Senregistrer(request.POST, instance=modifier)

        if fm.is_valid():
            fm.save()
            messages.success(request, 'Informations modifiées avec succès !')
            return redirect('adminPage')
    else:
        modifier = Administrateur.objects.get(pk=id)
        fm = Senregistrer(instance=modifier)    # On recree le formulaire

    return render(request, 'app/updateStudent.html', {'form':fm, 'id':id})
    """

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux utilisateurs de rechercher un et un seul apprenant avec son et prenom(s) 
def search(request):
    nom_recherche = request.GET.get("nom")
    prenom_recherche = request.GET.get("prenom")

    q = models.Q(nom__icontains=nom_recherche) & models.Q(prenom__icontains=prenom_recherche)
    laListe = Administrateur.objects.filter(q).distinct()   # distinct() garantit l'unicité des résultats de requête
                                                            # Un apprenant peut avoir plusieurs établissements
    """
        distinct() garantit que les résultats de la requête soient uniques, 
        il agit sur la base des valeurs des clés de la table, et non sur les combinaisons de colonnes
        Il ne repondra pas forcément à nos attentes ici.
    """

    if not laListe:
        messages.info(request, "Aucun résultat trouvé pour ce nom et prénom(s). Essayez peut-etre le nom uniquement dans la barre de recherche !")
        return render(request, "app/search.html", {'apprenant': [], "laListe": []})
    """

    """
    apprenant = laListe[0]  # Sélection du premier apprenant de la liste

    # Création d'une liste de liens pour chaque apprenant trouvé
    apprenant_links = [{'name': f"{apprenant.nom} {apprenant.prenom}", 'url': reverse('lookcursus', kwargs={'nom': apprenant.nom, 'prenom': apprenant.prenom})} for apprenant in laListe]

    return render(request, "app/search.html", {"laListe": apprenant_links})

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux utilisateurs de rechercher un ou plusieurs apprenants juste avec mot clé
def searchStandard(request):
    query = request.GET.get('faisUneRecherche')

    keywords = query.split()
    q = models.Q()

    for keyword in keywords:
        q |= models.Q(nom__icontains=keyword) | models.Q(prenom__icontains=keyword)

    laListe = Administrateur.objects.filter(q).distinct()   # distinct() garantit l'unicité des résultats de requête
                                                            # Un apprenant peut avoir plusieurs établissements

    if not laListe:
        messages.info(request, "Aucun résultat trouvé.")
        return render(request, "app/search.html", {"laListe": []})

    # Création d'une liste de liens pour chaque apprenant trouvé
    apprenant_links = [{'name': f"{apprenant.nom} {apprenant.prenom}", 'url': reverse('lookcursus', kwargs={'nom': apprenant.nom, 'prenom': apprenant.prenom})} for apprenant in laListe]

    return render(request, "app/search.html", {"laListe": apprenant_links})


"""
# Fonction permmettant aux utilisateurs de rechercher un et un seul apprenant avec son et prenom(s) 
def search(request):
    # Récupérer les termes de recherche
    nom_recherche = request.GET["nom"]
    prenom_recherche = request.GET["prenom"]

    # Construire la requête Q
    q = models.Q()
    q &= models.Q(nom__iexact=nom_recherche) and models.Q(prenom__iexact=prenom_recherche)

    # Effectuer la recherche
    laListe = Administrateur.objects.filter(q)

    # Gérer les cas où aucun résultat n'est trouvé
    if not laListe:
        messages.info(request, "Il se peut que vous n'ayiez pas entrer le nom et prénom(s) en entièreté, essayez le nom uniquement dans la barre de recherche !")
        return render(request, "app/search.html", {'apprenant':Administrateur.objects.get(id=apprenant_id), "laListe": []})

    lesEtueux = Administrateur.objects.all()       # Nous prenons tous les objects de notre table
    
    # Afficher les résultats de la recherche
    return render(request, "app/search.html", {"laListe":laListe, 'student':lesEtueux})

# Fonction permmettant aux utilisateurs de rechercher un ou plusieurs apprenants juste avec mot clé
def searchStandard(request) :
    # GET = {"nom":"bobo"}
    query = request.GET.get('faisUneRecherche')

    keywords = query.split()

    q = models.Q()

    for keyword in keywords :
        if keyword :
            q |= models.Q(nom__icontains=keyword) | models.Q(prenom__icontains=keyword)

            laListe = Administrateur.objects.filter(q)
            lesEtueux = Administrateur.objects.all()       # Nous prenons tous les objects de notre table
        
            # Afficher les résultats de la recherche
            return render(request, "app/search.html", {"laListe":laListe, 'student':lesEtueux})
        else :
            return render(request, "app/search.html", {'message' : "Aucun critère de recherche fourni."})
        if not laListe:
            messages.info(request, "Aucun résultat trouvé.")
            return render(request, "app/search.html", {"laListe": []})
    return render(request, "app/search.html")
"""

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """
# Fonction permmettant aux utilisateurs de se connecter apres avoir confirmé leur adresse email
def activate(request, uidb64, token) :
    try :
        uid = force_text(urlsafe_base64_decode(uidb64))   # On decode en 64bits pour voir cela correspond à user
        user = User.objects.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) :
        user = None 
    # Donc l'utilisateur n'est rien
    
    # On verifie les coincidences
    if user is not None and generatorToken.check_token(user, token) :
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a été activé, Félicitations. Connectez-vous !')
        return redirect('login')
    
    else :
        messages.error(request, "Activation d'email echoué, réessayez plutard !")
        return redirect('home')

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------- """


