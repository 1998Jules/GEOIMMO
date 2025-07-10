from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ajouter_bien, liste_biens, signup, contacter_annonceur, dashboard_vendeur,a_propos,blog,Expertise,mes_annonces,changer_statut_bien, voir_bien,incrementer_vue,detail_article,form_contact,mes_demandes


urlpatterns = [
    path('biens/ajouter/', ajouter_bien, name='ajouter_bien'),
    path('', liste_biens, name='liste_biens'),
    path('biens/connexion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='connexion'),
     path('biens/deconnexion/', auth_views.LogoutView.as_view(next_page='connexion'), name='deconnexion'),
    path('biens/inscription/', signup, name='inscription'),
    path('biens/contacter/<int:bien_id>/', contacter_annonceur, name='contacter_annonceur'),
    path('biens/dashboard/', dashboard_vendeur, name='dashboard_vendeur'),
    path('biens/a-propos/', a_propos, name='a_propos'),
    path('biens/blog/', blog, name='blog'),
    path('biens/Expertise/', Expertise, name='Expertise'),
    path('biens/mes-annonces/', mes_annonces, name='mes_annonces'),
    path('biens/changer-statut/<int:bien_id>/', changer_statut_bien, name='changer_statut_bien'),
    path('biens/biens/voir/<int:bien_id>/', voir_bien, name='voir_bien'),
    path('biens/<int:bien_id>/increment_vue/', incrementer_vue, name='increment_vue'),
    path('biens/form-contact/', form_contact, name='form_contact'),  
    path('biens/blog/<slug:slug>/', detail_article, name='detail_article'),
    path('biens/mes-demandes/', mes_demandes, name='mes_demandes')
     
]
