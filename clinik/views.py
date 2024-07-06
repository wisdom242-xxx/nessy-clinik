from django.shortcuts import render, get_object_or_404, redirect  # POUR LES REDIRECTIONS DES PAGES
from django.utils import timezone  # Pour obtenir la date actuelle
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum # pour les calculs (du bénefice )
from datetime import datetime # pour importer la date et l'heure actuelle
from django.contrib.auth.hashers import check_password # pour la verification es mots de passe
from django.http import HttpResponseNotFound, HttpResponse  # Ajoutez cette ligne pour importer HttpResponse
from .models import Utilisateur, Patient, Salle,Service, Examen, Produit, Vente, RapportMensuel #IMPORTATION DE NOS MODELS

from django.contrib.auth import logout

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Remplacez 'accueil' par l'URL nommée de votre choix



# NOTRE PAGE D'ACCUEIL
def base(request):
    return render(request, 'base.html')

def accueil(request):
    return render(request, 'accueil.html')


def consulter_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'consulter_patient.html', {'patient': patient})

# notre fonction pour l'ajout des patients
def ajout_patients(request):
    services = Service.objects.all()  # Récupérer tous les services

    if request.method == 'POST':
        nom = request.POST['nom']
        a_consulte = request.POST.get('a_consulte') == 'on'
        est_hospitalise = request.POST.get('est_hospitalise') == 'on'
        est_examine = request.POST.get('est_examine') == 'on'
        # Vérification : un patient ne peut être hospitalisé que s'il a été consulté
        if est_hospitalise and not a_consulte:
            return HttpResponse("<h1>Désolé,Un patient ne peut être hospitalisé que s'il a été consulté.</h1>")

        
        # Assurez-vous que 'service' est bien présent dans request.POST
        if 'service' in request.POST:
            service_id = request.POST['service']
            
            # Vérifiez si le service avec l'ID spécifié existe
            try:
                service = Service.objects.get(pk=service_id)
            except Service.DoesNotExist:
                return HttpResponseNotFound("Service not found")

            # Enregistrez le patient dans la base de données
            patient = Patient.objects.create(
                nom=nom,
                a_consulte=a_consulte,
                est_hospitalise=est_hospitalise,
                est_examine=est_examine,
                service=service
            )

            # Redirection ou affichage d'un message de succès, selon vos besoins
            return redirect('liste_patients')

    return render(request, 'ajout_patient.html', {'services': services})

# pour afficher la liste des patients dans la base de donnée
def liste_patients(request):
    patients = Patient.objects.all()
    return render(request, 'liste_patients.html', {'patients': patients})

# suppression des patients dans la base de donnée
def supprimer_patient(request,id_patient):
    data=Patient.objects.get(id_patient = id_patient)
    if request.method == 'POST':
        data.delete()
        return redirect('liste_patients')

    return render(request, 'supprimer_patient.html', {'data': data})

# modification des infos d'un patient déjà enregistré  
def modifier_patient(request, id_patient):
    patient = get_object_or_404(Patient, id_patient=id_patient)

    if request.method == 'POST':
        # Traitement du formulaire en cas de soumission
        patient.nom = request.POST.get('nom')
        patient.a_consulte = 'a_consulte' in request.POST
        patient.est_hospitalise = 'est_hospitalise' in request.POST
        patient.est_examine = 'est_examine' in request.POST
        patient.service_id = request.POST.get('service')
        patient.save()
        return redirect('liste_patients')
    else:
        # Affichage du formulaire
        services = Service.objects.all()
        return render(request, 'modifier_patient.html', {'patient': patient, 'services': services})


# pour voir la liste des produits
def affiche_produits(request):
    produits = Produit.objects.all()
    return render(request, 'affiche_produits.html', {'produits': produits})

# pour la suppression des pproduits
def supprimer_produit(request, id_produit):
    produit = get_object_or_404(Produit, id_produit=id_produit)

    if request.method == 'POST':
        produit.delete()
        return redirect('affiche_produits')

    return render(request, 'supprimer_produit.html', {'produit': produit})

# pour la modification des produits
def modifier_produit(request, id_produit):
    produit = get_object_or_404(Produit, id_produit=id_produit)

    if request.method == 'POST':
        # Récupérer les données du formulaire directement depuis la requête
        produit.designation = request.POST.get('designation')
        produit.quantite = request.POST.get('quantite')
        produit.prix_unitaire = request.POST.get('prix_unitaire')
        produit.save()

        return redirect('affiche_produits')

    return render(request, 'modifier_produit.html', {'produit': produit})

#pour l'ajout des nouveaux produits
def ajout_produits(request):
    if request.method == 'POST':
        # Traitement du formulaire soumis
        designation = request.POST['designation']
        quantite = request.POST['quantite']
        prix_unitaire = request.POST['prix_unitaire']

        # Vérification si le produit existe déjà
        if Produit.objects.filter(designation=designation).exists():
            # Produit existe déjà, afficher un message d'erreur
            messages.error(request, "Ce produit existe déjà dans la base de données.")
        else:
            # Enregistrement du produit dans la base de données
            produit = Produit.objects.create(
                designation=designation,
                quantite=quantite,
                prix_unitaire=prix_unitaire,
            )
            # Affichage d'un message de succès
            messages.success(request, "Le produit a été ajouté avec succès.")

    return render(request, 'ajout_produit.html')

# pour la vente des produits
def vendre_produit(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite_vente = int(request.POST.get('quantite', 0))
        prix_de_vente = request.POST['prix_de_vente']


        if quantite_vente <= 0:
            return HttpResponse("La quantité de vente doit être supérieure à zéro.")

        try:
            produit = Produit.objects.get(id_produit=produit_id)
        except Produit.DoesNotExist:
            return HttpResponse("Le produit sélectionné n'existe pas.")

        if quantite_vente > produit.quantite:
            return HttpResponse("Quantité insuffisante en stock.")

        prix_unitaire = produit.prix_unitaire
        date_vente = timezone.now()

        # Créer la vente
        vente = Vente(produit=produit, quantite=quantite_vente, prix_unitaire=prix_unitaire,prix_de_vente=prix_de_vente, date_vente=date_vente)
        vente.save()

        # Mettre à jour la quantité du produit en stock
        produit.quantite -= quantite_vente
        produit.save()

        return redirect('liste_vente')  # Rediriger vers la liste des produits après la vente

    # Si la méthode n'est pas POST, c'est probablement la première fois qu'on accède à la page
    produits = Produit.objects.all()
    return render(request, 'vendre_produit.html', {'produits': produits})

# pour voir la liste des ventes
def liste_vente(request):
    ventes = Vente.objects.all()
    return render(request, 'liste_vente.html', {'ventes': ventes})

def enregistrer_utilisateur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        adresse = request.POST.get('adresse')
        num_tel = request.POST.get('num_tel')
        password = request.POST.get('password')

         # Nettoyer les espaces autour du mot de passe
        password = password.strip()

        # Création d'une nouvelle instance de l'utilisateur et enregistrement dans la base de données
        utilisateur = Utilisateur(nom=nom, prenom=prenom, adresse=adresse, num_tel=num_tel, password=password)
        utilisateur.save()

        return redirect('login')  # Rediriger vers une vue qui affiche la liste des utilisateurs

    return render(request, 'enregistrer_utilisateur.html')
    
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})

def login(request):
    noms_utilisateurs = Utilisateur.objects.values_list('nom', flat=True)

    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')

         # Nettoyer les espaces autour du mot de passe
        password = password.strip()

        print(f"Nom reçu : {nom}")
        print(f"Mot de passe reçu : {password}")

        utilisateur = Utilisateur.objects.filter(nom=nom).first()

        if utilisateur is not None and check_password(password, utilisateur.password):
            # Authentification réussie, rediriger vers la page souhaitée
            return redirect('accueil')
        else:
            # Authentification échouée, afficher un message d'erreur
            erreur = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'login.html', {'erreur': erreur, 'noms_utilisateurs': noms_utilisateurs, 'nom_pre_rempli': nom})

    return render(request, 'login.html', {'noms_utilisateurs': noms_utilisateurs})

# pour la suppression des utilisateur
def supprimer_utilisateur(request, utilisateur_id):
    # Récupérer l'utilisateur à supprimer
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)

    if request.method == 'POST':
        # Supprimer l'utilisateur et rediriger vers une page appropriée
        utilisateur.delete()
        return redirect('liste_utilisateurs')  # Assurez-vous d'avoir une URL nommée 'liste_utilisateurs'

    # Afficher la confirmation de la suppression
    return render(request, 'supprimer_utilisateur.html', {'utilisateur': utilisateur})



def rapport_mensuel(request):
    rapport, mois = RapportMensuel.generer_rapport()
    return render(request, 'rapport_mensuel.html', {'rapport': rapport, 'mois': mois})

    
    
# print(rapports)   Ajoutez ceci pour voir les données dans la console
