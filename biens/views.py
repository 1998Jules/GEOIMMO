from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from collections import Counter
from .models import Article
from django.core.paginator import Paginator

from .forms import BienImmobilierForm, ContactAnnonceurForm
from .models import MediaBien, BienImmobilier, Message ,GaleriePhoto # Assure-toi d’avoir un modèle Message


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
        # ✅ Image principale → Galerie
            if bien.image_principale:
                GaleriePhoto.objects.create(bien=bien, image=bien.image_principale)

            # ✅ Plan du terrain → Galerie
            if bien.plan_terrain:
                GaleriePhoto.objects.create(bien=bien, image=bien.plan_terrain)

            # ✅ Images supplémentaires → MediaBien + Galerie
            for fichier in fichiers:
                media = MediaBien.objects.create(bien=bien, image=fichier)
                GaleriePhoto.objects.create(bien=bien, image=fichier)
        
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



from django.contrib.auth.models import User
from .models import Profile

# biens/views.py
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nom_complet = request.POST.get('nom_complet')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')

        if password1 != password2:
            return render(request, 'registration/signup.html', {'error': 'Les mots de passe ne correspondent pas.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/signup.html', {'error': 'Ce nom d’utilisateur existe déjà.'})

        user = User.objects.create_user(username=username, password=password1, email=email)
        user.is_active = False  # désactiver jusqu’à validation
        user.save()

        # Création du lien d’activation
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://{current_site.domain}{reverse('activer_compte', kwargs={'uidb64': uid, 'token': token})}"

        # Envoi du mail
        sujet = "Activez votre compte GeoImmoTech"
        message = render_to_string('registration/activation_email.html', {
            'user': user,
            'activation_link': activation_link
        })
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return render(request, 'registration/confirmation_envoyee.html', {'email': email})

    return render(request, 'registration/signup.html')




from .models import DemandeContact

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def contacter_annonceur(request, bien_id):
    bien = get_object_or_404(BienImmobilier, id=bien_id)
    if request.method == 'POST':
        form = ContactAnnonceurForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom_prenom']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            message = form.cleaned_data['message']

            contact = DemandeContact.objects.create(
                bien=bien,
                vendeur=bien.proprietaire,
                nom_prenom=nom,
                email=email,
                telephone=telephone,
                message=message,
            )

            # 📨 Préparer l’email
            subject = f"Nouveau message pour votre bien '{bien.titre}'"
            html_message = render_to_string('biens/nouveau_message.html', {
                'bien': bien,
                'vendeur': bien.proprietaire,
                'nom': nom,
                'email': email,
                'telephone': telephone,
                'message': message,
            })

            email_msg = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[bien.proprietaire.email],
            )
            email_msg.content_subtype = 'html'  # pour envoyer du HTML
            email_msg.send(fail_silently=False)

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
def galerie_photo(request):
    photos = GaleriePhoto.objects.filter(bien__proprietaire=request.user).order_by('-date_ajout')
    return render(request, 'biens/galerie.html', {'photos': photos})
# biens/views.py
from django.utils.encoding import force_str

def activer_compte(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_reussie.html')
    else:
        return render(request, 'registration/activation_invalide.html')
