# Remove this line as it's causing conflicts
# from django import views

from django.urls import path
from . import views  # Import views this way instead
from .views import (
    CustomLoginView,
    add_matiere,
    dashboard_professeur,
    dashboard_student,
    delete_matiere,
    export_bulletin_pdf,
    import_notes_excel,
    list_matieres,
    unauthorized_access,
    update_matiere,
    logout_view,
    profile_view,
    dashboard,
    accueil_utilisateur,
    register,
    add_note,
    delete_note,
    update_note,
    list_notes,
)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path("profile/", profile_view, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path('accueil/', accueil_utilisateur, name='accueil'),
    path("logout/", logout_view, name="logout"),
    path('notes/', list_notes, name='list_notes'),
    path('notes/add/', add_note, name='add_note'),
    path('notes/update/<int:note_id>/', update_note, name='update_note'),
    path('notes/delete/<int:note_id>/', delete_note, name='delete_note'),
    path('matieres/add/',add_matiere, name='add_matiere'),
    path('matieres/', list_matieres, name='list_matieres'),
    path('matieres/modifier/<int:matiere_id>/', update_matiere, name='update_matiere'),
    path('matieres/supprimer/<int:matiere_id>/', delete_matiere, name='delete_matiere'),
    path('bulletin/pdf/', export_bulletin_pdf, name='export_bulletin_pdf'),  # Remove views. prefix
    path('notes/import/', import_notes_excel, name='import_notes_excel'),
    path('dashboard/etudiant/', dashboard_student, name='dashboard_student'),
    path("dashboard/professeur/", dashboard_professeur, name="dashboard_professeur"),
    path('access-denied/', unauthorized_access, name='access_denied'),
    path('feedback/', views.envoyer_feedback, name='envoyer_feedback'),
    path('feedback/envoyes/', views.feedback_envoyes, name='feedback_envoyes'),
    path('merci/', views.merci_feedback, name='merci_feed'),  # Ajouter cette ligne pour la redirection
    path('feedback/modifier/<int:id>/', views.modifier_feedback, name='modifier_feedback'),
    path('feedback/confirmer-suppression/<int:id>/', views.confirmer_suppression_feedback, name='confirmer_suppression_feedback'),
    path('feedback/supprimer/<int:id>/', views.confirmer_suppression_feedback, name='supprimer_feedback_confirmé'),




]





