from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Classe(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Enseignant(models.Model): 
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    classe = models.ManyToManyField(Classe,related_name='enseignants')

    def __str__(self):
        return self.user.last_name

class Eleve(models.Model): 
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.user.username

class grp(models.Model):
    name = models.CharField(max_length=200)
    classe = models.ManyToManyField(Classe,related_name='groupes')
    def __str__(self):
        return self.name

class Travail(models.Model): 
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    date_limite = models.DateTimeField()
    classe = models.ForeignKey(Classe,on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='fichiersens/', blank=True, null=True)

    def __str__(self):
        return self.titre
    

class Commentaire(models.Model):
    travail = models.ForeignKey(Travail, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.travail.titre}"


class TravailEtudiant(models.Model):
    travail = models.ForeignKey(Travail, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(auto_now_add=True)
    fichier = models.FileField(upload_to='fichiers/', blank=True, null=True)
    texte = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Travail de {self.etudiant.user.username} sur {self.travail.titre}"

class Fichier(models.Model):
    fichier = models.FileField(upload_to='fichiers/')

    def __str__(self):
        return self.fichier.name
