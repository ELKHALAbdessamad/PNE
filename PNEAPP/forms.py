# PNEAPP/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Matiere, Utilisateur, Note

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[('Etudiant', 'Étudiant'), ('Prof', 'Professeur'), ('Admin', 'Administrateur')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Champs UserProfile
    matricule = forms.CharField(required=False)
    classe = forms.CharField(required=False)
    ecole = forms.CharField(required=False)
    groupe = forms.CharField(required=False)
    numerocne = forms.CharField(required=False)
    sexe = forms.ChoiceField(choices=[('M', 'Masculin'), ('F', 'Féminin')], required=False)
    date_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    nationalite = forms.CharField(required=False)

    class Meta:
        model = Utilisateur
        fields = [
            'username', 'email', 'password1', 'password2', 'role',
            'matricule', 'classe', 'ecole', 'groupe', 'numerocne',
            'sexe', 'date_naissance', 'nationalite'
        ]




# Exemple : Si tu avais un formulaire pour saisir une note
from django import forms
from .models import Note, Utilisateur

# forms.py
from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['etudiant', 'matiere', 'note', 'remarque']  # Ajout du champ remarque

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remarque'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 40})



from django import forms
from .models import Matiere
from django.core.exceptions import ValidationError

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom']

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if Matiere.objects.filter(nom__iexact=nom).exists():
            raise ValidationError("Cette matière existe déjà.")
        return nom


from django import forms
from .models import Feedback
from django.contrib.auth import get_user_model

User = get_user_model()

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['etudiant', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        # Filtrer uniquement les utilisateurs ayant le rôle "étudiant"
        self.fields['etudiant'].queryset = User.objects.filter(role='etudiant')
        self.fields['etudiant'].label = "Étudiant destinataire"
        self.fields['etudiant'].widget.attrs.update({'class': 'form-select'})

        # Optionnel : Ajout d'un label ou d'une description pour le champ message
        self.fields['message'].label = "Votre message"
        self.fields['message'].help_text = "Veuillez rédiger votre message de feedback."