import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from institutions.models import Employe

User = get_user_model()

for employe in Employe.objects.all():
    if not employe.user:
        try:
            user = User.objects.get(email=employe.email)
            employe.user = user
            employe.save()
            print(f"Employé {employe.nom} lié à l'utilisateur {user.username}")
        except User.DoesNotExist:
            username = employe.email.split('@')[0]
            if employe.nom.lower() == 'roland':
                password = os.environ.get('ROLAND_PASSWORD', '12334')
            else:
                password = os.environ.get('DEFAULT_USER_PASSWORD', 'changeme123')
            user = User.objects.create_user(
                username=username,
                email=employe.email,
                password=password
            )
            employe.user = user
            employe.save()
            print(f"Utilisateur créé et lié pour {employe.nom} ({employe.email})")

print("\nTous les employés sont maintenant liés à un utilisateur. Mot de passe initial: 'changeme123' (ou '12334' pour Roland)")
print("Pense à demander à chaque utilisateur de changer son mot de passe après la première connexion!")
