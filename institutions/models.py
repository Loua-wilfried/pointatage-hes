from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class Institution(models.Model):
    class Meta:
        app_label = 'institutions'
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
    ]

    code_institution = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    nom = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    indicatif_pays = models.CharField(max_length=10)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code_institution:
            indicatif = self.indicatif_pays
            ville_code = (self.ville[:2] if self.ville else '').upper()
            # Comptage existant
            count = Institution.objects.filter(
                indicatif_pays=indicatif,
                ville__istartswith=self.ville[:2]
            ).count() + 1
            numero_ordre = str(count).zfill(4)
            self.code_institution = f"{indicatif}{ville_code}{numero_ordre}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code_institution} - {self.nom}"


class PlanSaaS(models.Model):
    class Meta:
        app_label = 'institutions'
    nom_plan = models.CharField(max_length=100)
    description = models.TextField()
    prix_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    limite_utilisateurs = models.IntegerField()
    fonctionnalites_incluses = models.JSONField(default=list, blank=True)  # Liste de fonctionnalités

    def __str__(self):
        return self.nom_plan


class Abonnement(models.Model):
    class Meta:
        app_label = 'institutions'
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('termine', 'Terminé'),
        ('en_attente', 'En attente'),
    ]
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='abonnements')
    plan = models.ForeignKey(PlanSaaS, on_delete=models.CASCADE, related_name='abonnements')
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    mode_paiement = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.institution} - {self.plan} ({self.statut})"

# =====================
# Modèle Employe (SIRH)
# =====================

from roles_permissions.models import Role

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employe')
    class Meta:
        app_label = 'institutions'
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('Autre', 'Autre'),
    ]
    SITUATION_CHOICES = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('divorce', 'Divorcé(e)'),
        ('veuf', 'Veuf(ve)'),
        ('autre', 'Autre'),
    ]
    CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Stage', 'Stage'),
        ('Interim', 'Intérim'),
        ('Autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('demission', 'Démissionné'),
        ('licencie', 'Licencié'),
    ]
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=50)
    situation_familiale = models.CharField(max_length=20, choices=SITUATION_CHOICES)
    adresse = models.TextField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    numero_cni = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos_employes/', blank=True, null=True)
    date_embauche = models.DateField()
    date_fin_contrat = models.DateField(blank=True, null=True)
    type_contrat = models.CharField(max_length=20, choices=CONTRAT_CHOICES)
    periode_essai = models.CharField(max_length=100, blank=True, null=True)
    agence = models.ForeignKey('agences.Agence', on_delete=models.PROTECT, related_name='employes')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='employes')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    horaire_travail = models.CharField(max_length=100)
    matricule_interne = models.CharField(max_length=10, unique=True, editable=False)
    salaire_base = models.DecimalField(max_digits=12, decimal_places=2)  # SENSIBLE
    primes = models.JSONField(default=dict, blank=True)
    retenues = models.JSONField(default=dict, blank=True)
    rib_banque = models.CharField(max_length=50)
    heures_supplementaires = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    variables_paie = models.JSONField(default=dict, blank=True)
    diplomes = models.JSONField(default=list, blank=True)
    langues = models.JSONField(default=list, blank=True)
    competences = models.JSONField(default=list, blank=True)
    evaluations = models.JSONField(default=list, blank=True)
    objectifs = models.JSONField(default=list, blank=True)
    mobilite = models.CharField(max_length=100, blank=True, null=True)
    besoins_formation = models.JSONField(default=list, blank=True)
    plan_formation = models.JSONField(default=list, blank=True)
    sessions_suivies = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    absences_calculees = models.IntegerField(default=0)
    maladies = models.JSONField(default=list, blank=True)
    accidents = models.JSONField(default=list, blank=True)
    visites_medicales = models.JSONField(default=list, blank=True)
    restrictions_medicales = models.JSONField(default=list, blank=True)
    risques_professionnels = models.JSONField(default=list, blank=True)
    representation_personnel = models.BooleanField(default=False)
    reunions = models.JSONField(default=list, blank=True)
    sanctions = models.JSONField(default=list, blank=True)  # SENSIBLE
    reclamations = models.JSONField(default=list, blank=True)
    contentieux = models.JSONField(default=list, blank=True)
    date_depart = models.DateField(blank=True, null=True)
    motif_depart = models.CharField(max_length=255, blank=True, null=True)
    solde_tout_compte = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # SENSIBLE
    attestation_travail = models.FileField(upload_to='attestations/', blank=True, null=True)
    entretien_sortie = models.TextField(blank=True, null=True)
    droits_post_emploi = models.JSONField(default=list, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Employé'
        verbose_name_plural = 'Employés'

    def save(self, *args, **kwargs):
        # Génération automatique du matricule interne EMP0001, EMP0002, ...
        if not self.matricule_interne:
            last = Employe.objects.order_by('-id').first()
            if last and last.matricule_interne and last.matricule_interne.startswith('EMP'):
                num = int(last.matricule_interne[3:]) + 1
            else:
                num = 1
            self.matricule_interne = f"EMP{num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule_interne})"

    # Méthodes principales à compléter dans les vues/services :
    def creerEmploye(self):
        pass  # Voir formulaire multisection

    def modifierEmploye(self, id):
        pass  # Selon permissions

    def supprimerEmploye(self, id):
        # Suppression logique
        self.statut = 'inactif'
        self.save()

    def attribuerRole(self, role_id):
        self.role_id = role_id
        self.save()

    def calculerAbsences(self):
        # À implémenter : calcul automatique depuis Pointage
        pass

    def genererBulletin(self):
        # À implémenter : génération/association bulletin de paie
        pass

    def evaluerEmploye(self):
        # À implémenter : ajout évaluation
        pass

    def planifierFormation(self):
        # À implémenter : ajout formation
        pass

    def genererAttestation(self):
        # À implémenter : génération attestation PDF
        pass
