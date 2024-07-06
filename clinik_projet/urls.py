"""
URL configuration for clinique_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinik import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('accueil/', views.accueil, name='accueil'),
    path('consulter/<int:patient_id>/', views.consulter_patient, name='consulter_patient'),
     path('ajout_patient/', views.ajout_patients, name='ajout_patient'),
     path('liste_patients/', views.liste_patients, name='liste_patients'),
     path('supprimer_patient/<id_patient>/', views.supprimer_patient, name='supprimer_patient'),
     path('modifier_patient/<id_patient>/', views.modifier_patient, name='modifier_patient'),
      path('ajout_produit/', views.ajout_produits, name='ajout_produit'),
    path('affiche_produits/', views.affiche_produits, name='affiche_produits'),
    path('supprimer_produit/<id_produit>/', views.supprimer_produit, name='supprimer_produit'),
    path('modifier_produit/<id_produit>/', views.modifier_produit, name='modifier_produit'),
    path('vendre_produit/', views.vendre_produit, name='vendre_produit'),
    path('liste_vente/', views.liste_vente, name='liste_vente'),
    path('enregistrer_utilisateur/', views.enregistrer_utilisateur, name='enregistrer_utilisateur'),
    path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('', views.login, name='login'),
    path('supprimer_utilisateur/<utilisateur_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('rapport_mensuel/', views.rapport_mensuel, name='rapport_mensuel'),
    path('logout/', views.custom_logout_view, name='logout'),
    


         
    # Ajoutez d'autres URL pour les opérations similaires
]
