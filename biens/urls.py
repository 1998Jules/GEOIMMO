from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ajouter_bien, liste_biens, signup, contacter_annonceur, dashboard_vendeur,a_propos,blog,Expertise,mes_annonces,changer_statut_bien, voir_bien,incrementer_vue,detail_article,form_contact,mes_demandes

from . import views
urlpatterns = [
    path('annonces/ajouter/', ajouter_bien, name='ajouter_bien'),
    path('', liste_biens, name='liste_biens'),
    path('annonces/connexion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='connexion'),
     path('annonces/deconnexion/', auth_views.LogoutView.as_view(next_page='connexion'), name='deconnexion'),
    path('annonces/inscription/', signup, name='inscription'),
    path('annonces/contacter/<int:bien_id>/', contacter_annonceur, name='contacter_annonceur'),
    path('annonces/dashboard/', dashboard_vendeur, name='dashboard_vendeur'),
    path('annonces/a-propos/', a_propos, name='a_propos'),
    path('annonces/blog/', blog, name='blog'),
    path('annonces/Expertise/', Expertise, name='Expertise'),
    path('annonces/mes-annonces/', mes_annonces, name='mes_annonces'),
    path('annonces/changer-statut/<int:bien_id>/', changer_statut_bien, name='changer_statut_bien'),
    path('annonces/annonces/voir/<int:bien_id>/', voir_bien, name='voir_bien'),
    path('annonces/<int:bien_id>/increment_vue/', incrementer_vue, name='increment_vue'),
    path('annonces/form-contact/', form_contact, name='form_contact'),  
    path('annonces/blog/<slug:slug>/', detail_article, name='detail_article'),
    path('annonces/mes-demandes/', mes_demandes, name='mes_demandes'),
   
      path('annonces/modifier/<int:pk>/', views.modifier_bien, name='modifier_bien'),
    path('annonces/galerie/', views.galerie_photo, name='galerie_photo'),
    path('activation/<uidb64>/<token>/', views.activer_compte, name='activer_compte'),
    path('blog/like/<slug:slug>/', views.like_article, name='like_article'),  # <-- important
    path('carte/', views.carte_biens, name='carte_biens'),
   
     
]
