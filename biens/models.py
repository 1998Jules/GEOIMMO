from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.core.serializers import serialize
import json
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)  # ✅ nouveau champ


    def __str__(self):
        return f"Profil de {self.user.username}"


class BienImmobilier(models.Model):
    TYPE_CHOIX = [
        ('terrain', 'Terrain'),
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('local', 'Local commercial'),
        ('Chambre','Chambre')
    ]

    STATUT_CHOIX = [
        ('vente', 'En vente'),
        ('location', 'En location'),
        ('vendu', 'Vendu'),
        ('loué', 'Loué'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_bien = models.CharField(max_length=20, choices=TYPE_CHOIX)
    surface = models.FloatField()
    prix = models.DecimalField(max_digits=12, decimal_places=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='vente')
    localisation = geomodels.PointField(null=True, blank=True)
    zone_geom = geomodels.PolygonField(null=True, blank=True)
    image_principale = models.ImageField(null=True, blank=True)
    plan_terrain = models.ImageField( null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biens', null=True, blank=True)
    nom_vendeur = models.CharField(max_length=100, default="Anonyme", blank=True)
    contact_vendeur = models.CharField(max_length=20, default="0000000000", blank=True)
    vues = models.PositiveIntegerField(default=0) 
    a_la_une = models.BooleanField(default=False)
    localite = models.CharField(max_length=100, blank=True,null=True)
    def zone_geom_to_geojson(self):
        if self.zone_geom:
            return self.zone_geom.geojson  # Retourne directement la chaîne GeoJSON
        return None




    def __str__(self):
        return self.titre


class MediaBien(models.Model):
    bien = models.ForeignKey(BienImmobilier, related_name='medias', on_delete=models.CASCADE)
    image = models.ImageField()
    description = models.CharField(max_length=255, blank=True, null=True)
    est_plan = models.BooleanField(default=False)  # Pour différencier photo normale / plan
    

    def __str__(self):
        return f"Media pour {self.bien.titre}"

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    expediteur = models.ForeignKey(User, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(User, related_name='messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.expediteur} à {self.destinataire} - {self.date_envoi.strftime('%d/%m/%Y')}"
    # models.py
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField()
    image = models.ImageField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    vues = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titre
    from django.db import models
from django.contrib.auth.models import User

class DemandeContact(models.Model):
    bien = models.ForeignKey('BienImmobilier', on_delete=models.CASCADE, related_name='demandes')
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_recues')
    nom_prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Demande de {self.nom_prenom} pour {self.bien.titre}"


class GaleriePhoto(models.Model):
    bien = models.ForeignKey(BienImmobilier, on_delete=models.CASCADE, related_name='galerie_photos')
    image = models.ImageField(upload_to='galerie/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo ({self.bien.titre})"
