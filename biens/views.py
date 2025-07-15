from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from collections import Counter
from .models import Article
from django.core.paginator import Paginator

from .forms import BienImmobilierForm, ContactAnnonceurForm
from .models import MediaBien, BienImmobilier, Message  # Assure-toi d’avoir un modèle Message


# ➤ Tableau de bord vendeur
@login_required
def dashboard_vendeur(request):
    user = request.user
    annonces = BienImmobilier.objects.filter(proprietaire=user)
    
    nb_annonces = annonces.count()
    nb_vues = sum([b.vues if b.vues else 0 for b in annonces])  # si .vues existe
    nb_messages = DemandeContact.objects.filter(vendeur=user, lu=False).count()
    nb_favoris = user.favoris.count() if hasattr(user, 'favoris') else 0

    return render(request, 'biens/dashboard_vendeur.html', {
        'nb_annonces': nb_annonces,
        'nb_vues': nb_vues,
        'nb_messages': nb_messages,
        'nb_favoris': nb_favoris,
    })


# ➤ Ajout de bien

@login_required
def ajouter_bien(request):
    if request.method == 'POST':
        form = BienImmobilierForm(request.POST, request.FILES)
        fichiers = request.FILES.getlist('medias')

        if form.is_valid():
            bien = form.save(commit=False)
            bien.proprietaire = request.user
            bien.save()

            for f in fichiers:
                MediaBien.objects.create(
                    bien=bien,
                    image=f,
                    description=f.name
                )
            return redirect('liste_biens')
    else:
        form = BienImmobilierForm()

    return render(request, 'biens/ajouter_bien.html', {'form': form})


# ➤ Liste des biens
def liste_biens(request):
    biens = BienImmobilier.objects.all().prefetch_related('medias').order_by('-date_ajout')
    paginator = Paginator(biens, 12)
    page_number = request.GET.get('page')
    biens = paginator.get_page(page_number)
    for bien in biens:
        bien.geojson = bien.zone_geom_to_geojson()
    return render(request, 'biens/liste_biens.html', {'biens': biens})



# ➤ Inscription utilisateur
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


from .models import DemandeContact

def contacter_annonceur(request, bien_id):
    bien = get_object_or_404(BienImmobilier, id=bien_id)
    if request.method == 'POST':
        form = ContactAnnonceurForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom_prenom']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            message = form.cleaned_data['message']

            # Création de la demande de contact en base
            DemandeContact.objects.create(
                bien=bien,
                vendeur=bien.proprietaire,  # adapte selon ton champ vendeur/proprietaire
                nom_prenom=nom,
                email=email,
                telephone=telephone,
                message=message,
            )

            contenu = (
                f"Vous avez un nouveau message concernant votre bien '{bien.titre}':\n\n"
                f"Nom et prénom : {nom}\n"
                f"Email : {email}\n"
                f"Téléphone : {telephone}\n\n"
                f"Message :\n{message}"
            )

            send_mail(
                subject=f"Contact pour votre bien '{bien.titre}'",
                message=contenu,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[bien.proprietaire.email],
                fail_silently=False,
            )

            return render(request, 'biens/contact_success.html', {'bien': bien})
    else:
        form = ContactAnnonceurForm()
    return render(request, 'biens/contacter.html', {'form': form, 'bien': bien})

from django.shortcuts import render

def a_propos(request):
    return render(request, 'a_propos.html')

def blog(request):
    articles = Article.objects.order_by('-date_publication')  # Les plus récents d’abord
    return render(request, 'blog.html', {'articles': articles})
 # crée ce template avec ton contenu blog
def Expertise(request):
    return render(request, 'Expertise.html')


@login_required
def mes_annonces(request):
    biens = BienImmobilier.objects.filter(proprietaire=request.user)
    return render(request, 'biens/mes_annonces.html', {'biens': biens})
@login_required
def changer_statut_bien(request, bien_id):
    bien = get_object_or_404(BienImmobilier, id=bien_id, proprietaire=request.user)
    if request.method == "POST":
        nouveau_statut = request.POST.get('nouveau_statut')
        if nouveau_statut in dict(BienImmobilier.STATUT_CHOIX).keys():
            bien.statut = nouveau_statut
            bien.save()
    return redirect('mes_annonces')
def voir_bien(request, bien_id):
    bien = get_object_or_404(BienImmobilier, id=bien_id)
    bien.vues += 1
    bien.save(update_fields=['vues'])
    return redirect('liste_biens')  # OU une autre page plus ciblée, comme le détail
from django.http import JsonResponse



def incrementer_vue(request, bien_id):
    if request.method == "POST":
        bien = get_object_or_404(BienImmobilier, id=bien_id)
        if request.user != bien.proprietaire:
            bien.vues += 1
            bien.save(update_fields=['vues'])
        return JsonResponse({"status": "ok", "vues": bien.vues})
    return JsonResponse({"status": "error"}, status=400)
def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.vues += 1
    article.save(update_fields=["vues"])
    return render(request, 'detail_article.html', {'article': article})
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings

def form_contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        sujet = f"Nouveau message de contact de {nom}"
        corps = f"Nom : {nom}\nEmail : {email}\n\nMessage :\n{message}"

        try:
            send_mail(
                sujet,
                corps,
                settings.DEFAULT_FROM_EMAIL,  # ou email de l’expéditeur
                [settings.CONTACT_EMAIL],     # à définir dans settings.py
                fail_silently=False,
            )
            messages.success(request, "Votre message a bien été envoyé. Merci !")
        except Exception as e:
            print(e)
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")

    return redirect('liste_biens')
from django.contrib.auth.decorators import login_required

@login_required
def mes_demandes(request):
    user = request.user
    biens_vendeur = BienImmobilier.objects.filter(proprietaire=user)
    demandes = DemandeContact.objects.filter(bien__in=biens_vendeur).order_by('-date_envoi')
    return render(request, 'biens/mes_demandes.html', {'demandes': demandes})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import BienImmobilier
# biens/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import BienImmobilier
from .forms import BienImmobilierForm  # Le formulaire que tu utilises
from django.contrib.auth.decorators import login_required

from .models import MediaBien
from .forms import BienImmobilierForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import BienImmobilier, MediaBien
from .forms import BienImmobilierForm
@login_required
def modifier_bien(request, pk):
    bien = get_object_or_404(BienImmobilier, id=pk, proprietaire=request.user)

    if request.method == 'POST':
        form = BienImmobilierForm(request.POST, request.FILES, instance=bien)

        if form.is_valid():
            # ⚠️ Ne pas supprimer manuellement image_principale ici

            bien = form.save(commit=False)
            bien.proprietaire = request.user
            bien.save()

            # Supprimer et ajouter les nouvelles images complémentaires si fournies
            fichiers = request.FILES.getlist('medias')
            if fichiers:
                MediaBien.objects.filter(bien=bien).delete()
                for fichier in fichiers:
                    MediaBien.objects.create(
                        bien=bien,
                        image=fichier,
                        est_plan=False
                    )

            return redirect('mes_annonces')
    else:
        form = BienImmobilierForm(instance=bien)

    return render(request, 'biens/ajouter_bien.html', {
        'form': form,
        'bien': bien
    })
