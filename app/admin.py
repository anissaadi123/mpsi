from django.contrib import admin
from .models import Eleve,Enseignant,Classe,grp,Travail,Commentaire
# Register your models here.
admin.site.register(Eleve)
admin.site.register(Enseignant)
admin.site.register(Classe)
admin.site.register(grp)

admin.site.register(Travail)
admin.site.register(Commentaire)
