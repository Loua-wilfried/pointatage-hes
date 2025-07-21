
from django.db import models

# Import du modèle Employe depuis l'app institution
from institutions.models import Employe
from agences.models import Agence  # Import du modèle Agence (ne pas redéfinir ici)

class DocumentRh(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='documents_rh')
    type_document = models.CharField(max_length=100)
    fichier = models.FileField(upload_to='rh/documents/')
    date_upload = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employe} - {self.type_document}"

class ContratTravail(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')
    type_contrat = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    fichier_contrat = models.FileField(upload_to='rh/contrats/', blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.employe} - {self.type_contrat} ({self.date_debut})"

class HistoriquePoste(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='historiques_poste')
    poste = models.CharField(max_length=100)
    agence = models.CharField(max_length=100, blank=True, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    type_mouvement = models.CharField(max_length=50, blank=True, null=True)  # Promotion, mutation, etc.
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employe} - {self.poste} ({self.date_debut})"

class DonneeRhEmploye(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='donnees_rh')
    statut_rh = models.CharField(max_length=50, blank=True, null=True)  # Mutation, suspension, disponibilité
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employe} - {self.statut_rh}"

# --- MODULE 2 : Planification et affectation ---

class HoraireStandard(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    jours_semaine = models.CharField(max_length=50, help_text="Ex: LMMJV pour lundi à vendredi")
    def __str__(self):
        return self.nom

class HoraireEmploye(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='horaires')
    horaire = models.ForeignKey(HoraireStandard, on_delete=models.PROTECT)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.employe} - {self.horaire} ({self.date_debut})"

class AffectationEmploye(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='affectations')
    agence = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.employe} - {self.agence} ({self.date_debut})"

class JourFerie(models.Model):
    nom = models.CharField(max_length=100)
    date = models.DateField()
    recurrence = models.BooleanField(default=False, help_text="Revient chaque année")
    commentaire = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.nom} - {self.date}"

# --- MODULE 8 : Formations & compétences ---

class Formation(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    annee = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.nom} ({self.annee})"

class SessionFormation(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name='sessions')
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=200)
    theme = models.CharField(max_length=200, blank=True, null=True)
    intervenant = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return f"{self.formation} - {self.date_debut}"

class Evaluation(models.Model):
    employe = models.ForeignKey('institutions.Employe', on_delete=models.CASCADE, related_name='evaluations_formation')
    session = models.ForeignKey('SessionFormation', on_delete=models.CASCADE, related_name='evaluations')
    note = models.DecimalField(max_digits=5, decimal_places=2)
    commentaire = models.TextField(blank=True, null=True)
    date_evaluation = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.employe} - {self.session} - {self.note}"

class CertificationEmploye(models.Model):
    employe = models.ForeignKey('institutions.Employe', on_delete=models.CASCADE, related_name='certifications_formation')
    session = models.ForeignKey('SessionFormation', on_delete=models.CASCADE, related_name='certifications')
    annee = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.nom} ({self.annee})"

class SessionFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='sessions')
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=200)
    theme = models.CharField(max_length=200, blank=True, null=True)
    intervenant = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return f"{self.formation} - {self.date_debut}"

class Evaluation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='evaluations_formation')
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE, related_name='evaluations')
    note = models.DecimalField(max_digits=5, decimal_places=2)
    commentaire = models.TextField(blank=True, null=True)
    date_evaluation = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.employe} - {self.session} - {self.note}"

class CertificationEmploye(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='certifications_formation')
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE, related_name='certifications')
    certification = models.CharField(max_length=200)
    date_obtention = models.DateField()
    validee = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.employe} - {self.certification} ({self.date_obtention})"

class TypeAbsence(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nom

class AbsenceEmploye(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='absences')
    type_absence = models.ForeignKey(TypeAbsence, on_delete=models.PROTECT)
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.CharField(max_length=255, blank=True, null=True)
    statut = models.CharField(max_length=30, choices=[('en_attente', 'En attente'), ('valide', 'Validée'), ('refuse', 'Refusée')], default='en_attente')
    justificatif = models.FileField(upload_to='rh/absences/', blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.employe} - {self.type_absence} du {self.date_debut} au {self.date_fin}"

class DemandeConge(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='demandes_conge')
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_absence = models.ForeignKey(TypeAbsence, on_delete=models.PROTECT)
    statut = models.CharField(max_length=30, choices=[('en_attente', 'En attente'), ('valide', 'Validée'), ('refuse', 'Refusée')], default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.employe} - {self.type_absence} ({self.date_debut} au {self.date_fin})"


class Pointage(models.Model):
    TYPE_CHOICES = [
        ('arrivee', 'Arrivée'),
        ('depart', 'Départ'),
    ]
    SOURCE_CHOICES = [
        ('qr_code', 'QR Code'),
        ('geolocalisation', 'Geolocalisation'),
        ('manuel', 'Manuel'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='pointages')
    # Agence où le pointage est effectué
    agence = models.ForeignKey(
        Agence,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pointages',
        help_text="Agence liée au pointage",
        verbose_name="Agence de pointage"
    )
    date = models.DateField()
    heure = models.TimeField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manuel')
    commentaire = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employe', 'date', 'type'], name='unique_pointage_employe_date_type')
        ]

    def __str__(self):
        return f"{self.employe} - {self.type} {self.date} {self.heure} ({self.source})"


class Sanction(models.Model):
    TYPE_CHOICES = [
        ('avertissement', 'Avertissement'),
        ('blame', 'Blâme'),
        ('mise_a_pied', 'Mise à pied'),
        ('licenciement', 'Licenciement'),
        ('autre', 'Autre'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='sanctions_rh')
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    date = models.DateField()
    motif = models.CharField(max_length=255)
    duree = models.CharField(max_length=50, blank=True, null=True, help_text="Durée de la sanction si applicable")
    commentaire = models.TextField(blank=True, null=True)
    justificatif = models.FileField(upload_to='rh/sanctions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employe} - {self.get_type_display()} du {self.date}"
