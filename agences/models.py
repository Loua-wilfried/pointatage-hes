from django.db import models
from institutions.models import Institution

class Agence(models.Model):
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.CharField(primary_key=True, max_length=10, editable=False)
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='agences')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.id:
            dernier = Agence.objects.order_by('-id').first()
            if dernier:
                dernier_id = int(dernier.id)
                self.id = f"{dernier_id + 1:04d}"
            else:
                self.id = "0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.id})"
