# Generated by Django 4.2.23 on 2025-06-17 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('rh', '0005_pointage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sanction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('avertissement', 'Avertissement'), ('blame', 'Blâme'), ('mise_a_pied', 'Mise à pied'), ('licenciement', 'Licenciement'), ('autre', 'Autre')], max_length=30)),
                ('date', models.DateField()),
                ('motif', models.CharField(max_length=255)),
                ('duree', models.CharField(blank=True, help_text='Durée de la sanction si applicable', max_length=50, null=True)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('justificatif', models.FileField(blank=True, null=True, upload_to='rh/sanctions/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sanctions_rh', to='institutions.employe')),
            ],
        ),
    ]
