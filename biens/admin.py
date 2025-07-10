from django.contrib import admin

from .models import BienImmobilier

admin.site.register(BienImmobilier)

from .models import Article, Categorie

from django.contrib import admin
from .models import Article, Categorie

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date_publication', 'vues')
    search_fields = ('titre', 'contenu')
    list_filter = ('categorie', 'auteur', 'date_publication')
    prepopulated_fields = {"slug": ("titre",)}  # auto-remplit le slug

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    prepopulated_fields = {"slug": ("nom",)}



# Register your models here.