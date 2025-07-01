# Script Django pour supprimer les doublons de pointage
# À lancer avec : python manage.py shell < scripts/clean_pointage_duplicates.py

from rh.models import Pointage
from django.db.models import Count

# Grouper par employé, date, type, agence, source
dups = (
    Pointage.objects.values('employe_id', 'date', 'type', 'agence_id', 'source')
    .annotate(count=Count('id'))
    .filter(count__gt=1)
)

for dup in dups:
    qs = Pointage.objects.filter(
        employe_id=dup['employe_id'],
        date=dup['date'],
        type=dup['type'],
        agence_id=dup['agence_id'],
        source=dup['source']
    ).order_by('id')
    # On garde le premier, on supprime les autres
    to_delete = qs[1:]
    print(f"Suppression de {len(to_delete)} doublons pour {dup}")
    to_delete.delete()
