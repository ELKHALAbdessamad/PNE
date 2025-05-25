from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, NoteForm
from .models import UserProfile, Note
from pathlib import Path

Utilisateur = get_user_model()
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if hasattr(user, 'role'):
                if user.role == 'Prof':
                    return redirect('dashboard_professeur')
                elif user.role == 'Etudiant':
                    return redirect('dashboard_student')
            return redirect('home')
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
    return render(request, 'registration/login.html')  # ou ton propre template de connexion



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Créer l'utilisateur sans sauvegarder immédiatement
                user = form.save(commit=False)
                user.role = form.cleaned_data['role']
                user.save()

                # Créer le profil lié
                UserProfile.objects.create(
                    user=user,
                    matricule=form.cleaned_data.get('matricule'),
                    classe=form.cleaned_data.get('classe'),
                    ecole=form.cleaned_data.get('ecole'),
                    groupe=form.cleaned_data.get('groupe'),
                    numerocne=form.cleaned_data.get('numerocne'),
                    sexe=form.cleaned_data.get('sexe'),
                    date_naissance=form.cleaned_data.get('date_naissance'),
                    nationalite=form.cleaned_data.get('nationalite'),
                )

                # Connexion automatique de l'utilisateur
                login(request, user)
                messages.success(request, "Inscription réussie ! Bienvenue sur la plateforme.")
                return redirect('login')  # ou vers un tableau de bord
            except Exception as e:
                if user.pk:
                    user.delete()
                messages.error(request, f"Erreur lors de l'inscription : {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth import get_user_model

@login_required
def dashboard(request):
    Utilisateur = get_user_model()  # Récupérer le modèle utilisateur personnalisé

    # Filtrer par rôle dans le modèle Utilisateur
    students_count = Utilisateur.objects.filter(role="Etudiant").count()
    teachers_count = Utilisateur.objects.filter(role="Prof").count()
    admins_count = Utilisateur.objects.filter(role="Admin").count()

    return render(request, "dashboard.html", {
        "students_count": students_count,
        "teachers_count": teachers_count,
        "admins_count": admins_count,
    })


# Profil utilisateur
@login_required
def profile_view(request):
    return render(request, "profile.html")

# Accueil utilisateur
@login_required
def accueil_utilisateur(request):
    return render(request, 'accueil.html')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NoteForm

@login_required
def add_note(request):
    if request.user.role != 'Prof':
        messages.error(request, "Seuls les professeurs peuvent ajouter des notes.")
        return redirect('access_denied')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, 'Note et remarque ajoutées avec succès!')
            return redirect('list_notes')
    else:
        form = NoteForm()

    return render(request, 'notes/add_note.html', {'form': form})


# views.py
@login_required
def list_notes(request):
    if request.user.role == 'Prof':
        notes = Note.objects.all()
    else:
        notes = Note.objects.filter(etudiant=request.user)

    return render(request, 'notes/list_notes.html', {'notes': notes})


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm
from .models import Note

@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.user.role == 'Etudiant' and note.etudiant != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette note.")
        return redirect('access_denied')

    if request.user.role == 'Prof':
        if request.method == 'POST':
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                messages.success(request, 'Note et remarque mises à jour avec succès!')
                return redirect('list_notes')
        else:
            form = NoteForm(instance=note)

        return render(request, 'notes/update_note.html', {'form': form, 'note': note})

    messages.error(request, "Accès refusé.")
    return redirect('access_denied')
    
    # Si l'utilisateur n'est pas autorisé (étudiant ou autre)
    messages.error(request, "Accès refusé. Vous n'avez pas les autorisations nécessaires.")
    return redirect('access_denied')  # Rediriger vers la page d'accès refusé

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    # Si l'utilisateur est un étudiant, il ne peut supprimer que ses propres notes
    if request.user.role == 'Etudiant' and note.etudiant != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette note.")
        return redirect('access_denied')  # Rediriger vers la page d'accès refusé
    
    # Si l'utilisateur est un professeur, il peut supprimer toutes les notes
    if request.user.role == 'Prof':
        note.delete()
        messages.success(request, 'Note supprimée avec succès!')
        return redirect('list_notes')
    
    # Si l'utilisateur n'est ni professeur ni étudiant autorisé, on le redirige vers la page d'accès refusé
    messages.error(request, "Accès refusé. Vous n'avez pas les autorisations nécessaires.")
    return redirect('access_denied')  # Rediriger vers la page d'accès refusé

# views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'Prof':
            return '/dashboard/professeur/'
        elif user.role == 'Etudiant':
            return '/dashboard/etudiant/'  # Changed from '/profile/' to '/dashboard/etudiant/'
        else:
            return 'accueil'  # page d'accueil par défaut
        
from .models import Matiere
from .forms import MatiereForm

@login_required
def list_matieres(request):
    matieres = Matiere.objects.all().distinct()
    return render(request, 'matieres/list_matieres.html', {'matieres': matieres})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MatiereForm

@login_required
def add_matiere(request):
    # Vérifier que l'utilisateur est un professeur
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas l'autorisation d'ajouter des matières.")
        return redirect('access_denied')  # Rediriger vers la page d'accès refusé
    
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière ajoutée avec succès.")
            return redirect('list_matieres')  # Redirection vers la liste des matières
    else:
        form = MatiereForm()

    return render(request, 'matieres/add_matiere.html', {'form': form})


@login_required
def update_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas l'autorisation d'ajouter des matières.")
        return redirect('access_denied')  # Redi
    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            return redirect('list_matieres')
    else:
        form = MatiereForm(instance=matiere)
    return render(request, 'matieres/add_matiere.html', {'form': form})

@login_required
def delete_matiere(request, matiere_id):
   if not hasattr(request.user, 'role') or request.user.role != 'admin':
    matiere = get_object_or_404(Matiere, id=matiere_id)
    messages.error(request, "Vous n'avez pas l'autorisation d'ajouter des matières.")
    return redirect('access_denied')  # Redi
    if request.method == 'POST':
        matiere.delete()
        return redirect('list_matieres')
    return render(request, 'matieres/confirm_delete.html', {'matiere': matiere})


def calculer_moyenne_etudiant(etudiant):
    notes = Note.objects.filter(etudiant=etudiant)
    if notes.exists():
        total = sum(note.valeur for note in notes)
        return round(total / notes.count(), 2)
    return 0



# views.py
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

@login_required
def export_bulletin_pdf(request):
    if request.user.role != 'Etudiant':
        messages.error(request, "Accès non autorisé")
        return redirect('access_denied')

    notes = Note.objects.filter(etudiant=request.user)
    template = get_template('notes/bulletin_pdf.html')

    context = {
        'notes': notes,
        'user': request.user,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bulletin.pdf"'

    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response
from django.shortcuts import render, get_object_or_404
from .models import Note, Utilisateur  # ou ton modèle utilisateur

def bulletin(request, student_id):
    student = get_object_or_404(Utilisateur, id=student_id)
    notes = Note.objects.filter(etudiant=student)
    if notes.exists():
        moyenne = sum(note.note for note in notes) / notes.count()
    else:
        moyenne = 0

    return render(request, 'notes/bulletin.html', {
        'notes': notes,
        'moyenne': moyenne,
        'user': student,  # pour afficher prénom/nom sur le bulletin
    })


import pandas as pd
from django.http import HttpResponse

@login_required
def export_notes_excel(request):
    notes = Note.objects.all().values('etudiant_username', 'matiere_nom', 'valeur')
    df = pd.DataFrame(notes)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="notes.xlsx"'
    df.to_excel(response, index=False)
    return response

import pandas as pd
from django.shortcuts import render
from .models import Note, Matiere
from django.contrib import messages

@login_required
def import_notes_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                etudiant = Utilisateur.objects.get(username=row['etudiant__username'])
                matiere = Matiere.objects.get(nom=row['matiere__nom'])

                Note.objects.create(
                    etudiant=etudiant,
                    matiere=matiere,
                    valeur=row['valeur']
                )
            messages.success(request, "Notes importées avec succès !")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'importation : {e}")
        return redirect('list_notes')

    return render(request, 'notes/import_notes.html')

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import Note

def export_bulletin_pdf(request):
    notes = Note.objects.filter(etudiant=request.user)

    def calculer_mention(note):
        if note >= 16:
            return "Très bien"
        elif note >= 14:
            return "Bien"
        elif note >= 12:
            return "Assez bien"
        elif note >= 10:
            return "Passable"
        else:
            return "Insuffisant"

    # Create notes_with_mentions list
    notes_with_mentions = []
    for note in notes:
        notes_with_mentions.append({
            'matiere': note.matiere.nom,
            'note': note.note,
            'mention': calculer_mention(note.note)
        })

    # Calculate moyenne
    moyenne = (
        sum(note.note for note in notes) / notes.count()
        if notes.exists() else 0
    )

    context = {
        'notes': notes_with_mentions,
        'user': {
            'first_name': request.user.first_name or request.user.username,
            'last_name': request.user.last_name or ''
        },
        'moyenne': moyenne
    }

    template_path = 'notes/bulletin_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bulletin.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF', status=500)
    return response


from PNEAPP.models import Feedback, Note
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_student(request):
    if not hasattr(request.user, 'role') or request.user.role != 'Etudiant':
        return render(request, 'unauthorized.html')

    notes = Note.objects.filter(etudiant=request.user)
    total_matieres = notes.count()
    moyenne = round(sum(note.note for note in notes) / total_matieres, 2) if total_matieres else 0
    meilleure_note = max([note.note for note in notes], default=0)
    pire_note = min([note.note for note in notes], default=0)

    feedbacks = Feedback.objects.filter(etudiant=request.user).order_by('-created_at')
    feedbacks_non_lus = feedbacks.filter(lu=False).count()

    # ➕ Marquer les feedbacks comme lus automatiquement
    feedbacks.filter(lu=False).update(lu=True)

    context = {
        "notes": notes,
        "moyenne": moyenne,
        "total_matieres": total_matieres,
        "meilleure_note": meilleure_note,
        "pire_note": pire_note,
        "feedbacks": feedbacks,
        "feedbacks_non_lus": feedbacks_non_lus,
    }
    return render(request, "dashboard_student.html", context)




from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min
from django.shortcuts import render
from .models import Utilisateur, Matiere, Note
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def dashboard_professeur(request):
    total_etudiants = User.objects.filter(role='Etudiant').count()
    total_matieres = Matiere.objects.count()
    
    moyenne_globale = Note.objects.aggregate(moy=Avg('note'))['moy'] or 0
    meilleure_note = Note.objects.aggregate(max=Max('note'))['max'] or 0
    pire_note = Note.objects.aggregate(min=Min('note'))['min'] or 0

    # Moyenne par matière
    matieres = Matiere.objects.all()
    moyennes_par_matiere = []
    for matiere in matieres:
        moyenne = Note.objects.filter(matiere=matiere).aggregate(moy=Avg('note'))['moy'] or 0
        moyennes_par_matiere.append((matiere.nom, round(moyenne, 2)))

    # Calcul des moyennes par étudiant
    etudiants = User.objects.filter(role='Etudiant')
    etudiants_moyennes = []

    for etudiant in etudiants:
        moyenne = Note.objects.filter(etudiant=etudiant).aggregate(moy=Avg('note'))['moy']
        if moyenne is not None:
            etudiants_moyennes.append({
                'nom': f"{etudiant.first_name} {etudiant.last_name}",
                'moyenne': round(moyenne, 2)
            })

    # Trier les étudiants par moyenne
    etudiants_tries = sorted(etudiants_moyennes, key=lambda x: x['moyenne'])

    # Meilleure moyenne (le dernier étudiant après tri croissant)
    meilleur_etudiant = etudiants_tries[-1] if etudiants_tries else None

    # Pire moyenne (le premier étudiant après tri croissant)
    pire_etudiant = etudiants_tries[0] if etudiants_tries else None

    # Dernière moyenne (le dernier étudiant avec la moyenne la plus basse)
    last_student = etudiants_tries[0] if etudiants_tries else None

    return render(request, 'dashboard_professeur.html', {
        'total_etudiants': total_etudiants,
        'total_matieres': total_matieres,
        'moyenne_globale': round(moyenne_globale, 2),
        'meilleure_note': meilleure_note,
        'pire_note': pire_note,
        'moyennes_par_matiere': moyennes_par_matiere,
        'meilleur_etudiant': meilleur_etudiant,
        'pire_etudiant': pire_etudiant,
        'last_student': last_student,  # Ajout de la variable last_student
    })


from django.shortcuts import render

def unauthorized_access(request):
    return render(request, 'unauthorized.html')
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'Prof':
        return redirect('dashboard_professeur')  # nom de l'URL vers la vue professeur
    elif user.role == 'Etudiant':
        return redirect('dashboard_student')     # nom de l'URL vers la vue étudiant
    elif user.role == 'Admin':
        return redirect('/dashboard/')               # ou redirige vers une vue admin personnalisée
    else:
        return redirect('login')  # ou une autre page d'erreur / accès refusé


@login_required
def feedback_envoyes(request):
    if not hasattr(request.user, 'role') or request.user.role != 'Prof':
        return render(request, 'unauthorized.html')

    feedbacks = Feedback.objects.filter(prof=request.user).select_related('etudiant')

    context = {
        "feedbacks": feedbacks
    }
    return render(request, "feedback_envoyes.html", context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Feedback
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

@login_required
def envoyer_feedback(request):
    if not hasattr(request.user, 'role') or request.user.role != 'Prof':
        return render(request, 'unauthorized.html')
    if request.method == 'POST':
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        destinataire_id = request.POST.get('destinataire')
        
        # Récupérer l'étudiant sélectionné
        etudiant = User.objects.get(id=destinataire_id)
        
        # Créer un objet feedback
        feedback = Feedback.objects.create(
            prof=request.user,
            etudiant=etudiant,
            message=message
        )

        # Envoyer un email
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [etudiant.email],
            fail_silently=False,
        )

        messages.success(request, 'Feedback envoyé avec succès!')
        return render(request, 'merci.html', {'etudiants': User.objects.filter(role='etudiant')})

    else:
        # Afficher le formulaire avec les étudiants
        return render(request, 'feedback.html', {'etudiants': User.objects.filter(role='etudiant')})

from django.shortcuts import render

def merci_feedback(request):
    return render(request, 'merci.html')  # Cette page affiche un message de confirmation

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def modifier_feedback(request, id):  # Accepter `id` pour récupérer le feedback spécifique
    feedback = get_object_or_404(Feedback, id=id)  # Récupérer le feedback par son ID

    # Vérification si l'utilisateur est le professeur qui a créé ce feedback
    if feedback.prof != request.user:
        return redirect('unauthorized')  # Si l'utilisateur n'est pas le professeur, rediriger vers une page d'erreur

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)  # Remplir le formulaire avec les données existantes du feedback
        if form.is_valid():
            form.save()  # Sauvegarder les modifications
            return redirect('feedback_envoyes')  # Rediriger vers la page des feedbacks envoyés après modification
    else:
        form = FeedbackForm(instance=feedback)  # Pré-remplir le formulaire avec le feedback existant

    return render(request, 'modifier_feedback.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback

@login_required
def supprimer_feedback(request, id):  # ← ici tu dois accepter `id`
    feedback = get_object_or_404(Feedback, id=id)

    if request.method == 'POST':
        feedback.delete()
        return redirect('feedback_envoyes')  # Redirection vers la liste

    return redirect('feedback_envoyes')  # Ou une page de confirmation avant suppression

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback

@login_required
def confirmer_suppression_feedback(request, id):
    # Vérifier que l'utilisateur est un professeur ou l'admin
    if request.user.role != 'Prof':
        return render(request, 'unauthorized.html')

    # Récupérer le feedback à supprimer
    feedback = get_object_or_404(Feedback, id=id)

    # Confirmer la suppression (par exemple, on affiche une page avec un bouton "Confirmer")
    if request.method == 'POST':
        # Supprimer le feedback
        feedback.delete()
        # Rediriger vers la page des feedbacks envoyés
        return redirect('feedback_envoyes')

    return render(request, 'confirmer_suppression_feedback.html', {'feedback': feedback})
