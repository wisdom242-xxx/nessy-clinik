from django.shortcuts import redirect
from django.urls import reverse

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Liste des URL protégées et les permissions nécessaires
        protected_urls = {
            reverse('liste_patients'): 'clinik.can_view_patient',
            reverse('liste_utilisateurs'): 'clinik.can_view_user',
            reverse('liste_vente'): 'clinik.can_view_sales',
            reverse('affiche_produits'): 'clinik.can_view_product',
            reverse('ajout_produit'): 'clinik.can_add_product',
            reverse('ajout_patient'): 'clinik.can_add_patient',
            reverse('vendre_produit'): 'clinik.can_sell_product',
            reverse('rapport_mensuel'): 'clinik.can_view_report',
        }

        # Vérifie si l'URL actuelle est protégée
        if request.path in protected_urls:
            required_permission = protected_urls[request.path]
            if not request.user.is_authenticated:
                return redirect('login')  # Redirige vers la page de connexion
            if not request.user.has_perm(required_permission):
                return redirect('accueil')  # Redirige vers la page d'accueil ou une page d'erreur
        else:
            return None  # Autorise l'accès à toutes les autres URLs

        return None
