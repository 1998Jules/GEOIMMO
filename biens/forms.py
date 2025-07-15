from django import forms
from .models import BienImmobilier
from django.core.exceptions import ValidationError

class BienImmobilierForm(forms.ModelForm):
    class Meta:
        model = BienImmobilier
        fields = [
            'titre', 'description', 'type_bien', 'surface', 'prix', 'statut',
            'a_la_une', 'localisation', 'zone_geom',
            'image_principale', 'plan_terrain',
            'nom_vendeur', 'contact_vendeur','localite',
        ]
        widgets = {
            'localisation': forms.TextInput(attrs={
                'type': 'hidden',
                'id': 'id_localisation'
            }),
            'zone_geom': forms.TextInput(attrs={
                'type': 'hidden',
                'id': 'id_zone_geom'
            }),
            'localite': forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Commencez à taper une localité...',
    'autocomplete': 'on',
    'list': 'localite-suggestions',
}),
        }

    def clean(self):
        cleaned_data = super().clean()
        type_bien = cleaned_data.get('type_bien')
        localisation = cleaned_data.get('localisation')
        zone_geom = cleaned_data.get('zone_geom')

        if type_bien == 'terrain' and not zone_geom:
            raise ValidationError({'zone_geom': "Veuillez dessiner un polygone pour localiser le terrain."})

        if type_bien != 'terrain' and not localisation:
            raise ValidationError({'localisation': "Veuillez cliquer sur la carte pour définir l'emplacement."})


class ContactAnnonceurForm(forms.Form):
    nom_prenom = forms.CharField(label="Nom et prénom", max_length=100, required=True)
    email = forms.EmailField(label="Adresse email", required=True)
    telephone = forms.CharField(label="Numéro de téléphone", max_length=20, required=True)
    message = forms.CharField(label="Message", widget=forms.Textarea, required=True)
from django.forms import inlineformset_factory
from .models import MediaBien

MediaBienFormSet = inlineformset_factory(
    BienImmobilier,
    MediaBien,
    fields=('image', 'description', 'est_plan'),
    extra=1,
    can_delete=True
)
