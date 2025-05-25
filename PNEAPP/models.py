# PNEAPP/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLES = [
        ('Prof', 'Professeur'),
        ('Etudiant', 'Étudiant'),
        ('Admin', 'Administrateur')
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='Etudiant')


# Ajoutez ce modèle UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profile')
    matricule = models.CharField(max_length=20, blank=True, null=True)
    classe = models.CharField(max_length=50, blank=True, null=True)
    ecole = models.CharField(max_length=100, blank=True, null=True)
    groupe = models.CharField(max_length=50, blank=True, null=True)
    numerocne = models.CharField(max_length=20, blank=True, null=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    nationalite = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"


# Modèle Image (si vous voulez gérer des images dans votre projet)
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description



from django.db import models
from django.utils import timezone

# Modèle Matiere
class Matiere(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# models.py
class Note(models.Model):
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='notes')
    note = models.FloatField()
    remarque = models.TextField(blank=True, null=True)  # Nouveau champ pour les remarques

   
    @property
    def mention(self):
        if self.note >= 16:
            return "Très bien"
        elif self.note >= 14:
            return "Bien"
        elif self.note >= 12:
            return "Assez bien"
        elif self.note >= 10:
            return "Passable"
        else:
            return "Insuffisant"

    def __str__(self):
        return f"{self.etudiant} - {self.matiere}: {self.valeur} ({self.remarque})"
    
from django.db import models
from django.conf import settings

class Feedback(models.Model):
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    prof = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks_given')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lu = models.BooleanField(default=False)  # Champ pour savoir si le feedback a été lu

    def __str__(self):
        # Affichage plus détaillé du feedback
        return f"Feedback de {self.prof} à {self.etudiant} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"