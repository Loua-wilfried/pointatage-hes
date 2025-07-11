# Generated by Django 4.2.23 on 2025-06-16 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roles_permissions', '0001_initial'),
        ('agences', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_institution', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('adresse', models.TextField(blank=True, null=True)),
                ('telephone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('pays', models.CharField(max_length=100)),
                ('ville', models.CharField(max_length=100)),
                ('indicatif_pays', models.CharField(max_length=10)),
                ('statut', models.CharField(choices=[('actif', 'Actif'), ('suspendu', 'Suspendu')], default='actif', max_length=10)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanSaaS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_plan', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prix_mensuel', models.DecimalField(decimal_places=2, max_digits=10)),
                ('limite_utilisateurs', models.IntegerField()),
                ('fonctionnalites_incluses', models.JSONField(blank=True, default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin'), ('Autre', 'Autre')], max_length=10)),
                ('date_naissance', models.DateField()),
                ('lieu_naissance', models.CharField(max_length=100)),
                ('nationalite', models.CharField(max_length=50)),
                ('situation_familiale', models.CharField(choices=[('celibataire', 'Célibataire'), ('marie', 'Marié(e)'), ('divorce', 'Divorcé(e)'), ('veuf', 'Veuf(ve)'), ('autre', 'Autre')], max_length=20)),
                ('adresse', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=20)),
                ('numero_cni', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos_employes/')),
                ('date_embauche', models.DateField()),
                ('date_fin_contrat', models.DateField(blank=True, null=True)),
                ('type_contrat', models.CharField(choices=[('CDI', 'CDI'), ('CDD', 'CDD'), ('Stage', 'Stage'), ('Interim', 'Intérim'), ('Autre', 'Autre')], max_length=20)),
                ('periode_essai', models.CharField(blank=True, max_length=100, null=True)),
                ('statut', models.CharField(choices=[('actif', 'Actif'), ('inactif', 'Inactif'), ('demission', 'Démissionné'), ('licencie', 'Licencié')], default='actif', max_length=20)),
                ('horaire_travail', models.CharField(max_length=100)),
                ('matricule_interne', models.CharField(editable=False, max_length=10, unique=True)),
                ('salaire_base', models.DecimalField(decimal_places=2, max_digits=12)),
                ('primes', models.JSONField(blank=True, default=dict)),
                ('retenues', models.JSONField(blank=True, default=dict)),
                ('rib_banque', models.CharField(max_length=50)),
                ('heures_supplementaires', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('variables_paie', models.JSONField(blank=True, default=dict)),
                ('diplomes', models.JSONField(blank=True, default=list)),
                ('langues', models.JSONField(blank=True, default=list)),
                ('competences', models.JSONField(blank=True, default=list)),
                ('evaluations', models.JSONField(blank=True, default=list)),
                ('objectifs', models.JSONField(blank=True, default=list)),
                ('mobilite', models.CharField(blank=True, max_length=100, null=True)),
                ('besoins_formation', models.JSONField(blank=True, default=list)),
                ('plan_formation', models.JSONField(blank=True, default=list)),
                ('sessions_suivies', models.JSONField(blank=True, default=list)),
                ('certifications', models.JSONField(blank=True, default=list)),
                ('absences_calculees', models.IntegerField(default=0)),
                ('maladies', models.JSONField(blank=True, default=list)),
                ('accidents', models.JSONField(blank=True, default=list)),
                ('visites_medicales', models.JSONField(blank=True, default=list)),
                ('restrictions_medicales', models.JSONField(blank=True, default=list)),
                ('risques_professionnels', models.JSONField(blank=True, default=list)),
                ('representation_personnel', models.BooleanField(default=False)),
                ('reunions', models.JSONField(blank=True, default=list)),
                ('sanctions', models.JSONField(blank=True, default=list)),
                ('reclamations', models.JSONField(blank=True, default=list)),
                ('contentieux', models.JSONField(blank=True, default=list)),
                ('date_depart', models.DateField(blank=True, null=True)),
                ('motif_depart', models.CharField(blank=True, max_length=255, null=True)),
                ('solde_tout_compte', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('attestation_travail', models.FileField(blank=True, null=True, upload_to='attestations/')),
                ('entretien_sortie', models.TextField(blank=True, null=True)),
                ('droits_post_emploi', models.JSONField(blank=True, default=list)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employes', to='agences.agence')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employes', to='roles_permissions.role')),
            ],
            options={
                'verbose_name': 'Employé',
                'verbose_name_plural': 'Employés',
                'ordering': ['-date_creation'],
            },
        ),
        migrations.CreateModel(
            name='Abonnement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('statut', models.CharField(choices=[('actif', 'Actif'), ('suspendu', 'Suspendu'), ('termine', 'Terminé'), ('en_attente', 'En attente')], default='actif', max_length=20)),
                ('mode_paiement', models.CharField(max_length=50)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonnements', to='institutions.institution')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonnements', to='institutions.plansaas')),
            ],
        ),
    ]
