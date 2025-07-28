#!/usr/bin/env python
"""
Script pour insérer tous les rôles métiers dans la base de données MySQL
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from roles_permissions.models import Role

def insert_roles():
    """Insère tous les rôles métiers dans la base de données"""
    
    roles_data = [
        {
            'nom_role': 'Comptable',
            'description': 'Responsable des activités liées au poste de comptable, incluant la saisie comptable, la tenue des journaux, la gestion des états financiers, les rapprochements et les déclarations fiscales.',
            'slug': 'comptable'
        },
        {
            'nom_role': 'Assistant(e) Comptable',
            'description': 'Assiste le/la comptable dans ses tâches quotidiennes : saisie des écritures, classement des pièces, rapprochements bancaires, états comptables et préparation des audits.',
            'slug': 'assistant-comptable'
        },
        {
            'nom_role': 'Responsable RH',
            'description': 'Supervise la gestion du personnel, les recrutements, la paie, les contrats, les congés, les formations et les obligations sociales de l\'institution.',
            'slug': 'responsable-rh'
        },
        {
            'nom_role': 'Assistant(e) Responsable RH',
            'description': 'Appuie le/la responsable RH dans la gestion administrative du personnel, les congés, le classement des dossiers, le suivi des absences et les plannings.',
            'slug': 'assistant-responsable-rh'
        },
        {
            'nom_role': 'Caissier',
            'description': 'Gère les transactions journalières de caisse, les retraits, les dépôts, la clôture de caisse et la conservation des bordereaux.',
            'slug': 'caissier'
        },
        {
            'nom_role': 'Assistant(e) Caissier',
            'description': 'Aide le caissier dans la saisie des transactions, le classement des pièces justificatives et la gestion du fonds de caisse.',
            'slug': 'assistant-caissier'
        },
        {
            'nom_role': 'Agent de crédit',
            'description': 'Étudie, propose et suit les demandes de crédit. Il simule les échéanciers et assure un accompagnement jusqu\'au remboursement final.',
            'slug': 'agent-credit'
        },
        {
            'nom_role': 'Assistant(e) Agent de crédit',
            'description': 'Prépare les dossiers de crédit, assiste à la simulation des échéanciers et assure le suivi documentaire des prêts.',
            'slug': 'assistant-agent-credit'
        },
        {
            'nom_role': 'Chef crédit',
            'description': 'Supervise l\'ensemble des activités de crédit, valide ou rejette les demandes, débloque les fonds et gère les risques liés aux prêts.',
            'slug': 'chef-credit'
        },
        {
            'nom_role': 'Assistant(e) Chef crédit',
            'description': 'Apporte un appui administratif au chef crédit dans l\'analyse des demandes, la constitution des dossiers et la coordination des équipes.',
            'slug': 'assistant-chef-credit'
        },
        {
            'nom_role': 'Agent de recouvrement',
            'description': 'Suit les impayés, contacte les clients en défaut, planifie les relances et les visites pour recouvrer les créances.',
            'slug': 'agent-recouvrement'
        },
        {
            'nom_role': 'Assistant(e) Agent de recouvrement',
            'description': 'Gère les relances téléphoniques et documentaires, met à jour les suivis de promesses de paiement et appuie les visites de terrain.',
            'slug': 'assistant-agent-recouvrement'
        },
        {
            'nom_role': 'Agent de collecte',
            'description': 'Se déplace pour collecter les remboursements physiques et les enregistre dans le système.',
            'slug': 'agent-collecte'
        },
        {
            'nom_role': 'Assistant(e) Agent de collecte',
            'description': 'Prépare les bordereaux, accompagne les agents sur le terrain et effectue les saisies de collecte au retour.',
            'slug': 'assistant-agent-collecte'
        },
        {
            'nom_role': 'Auditeur',
            'description': 'Contrôle les opérations de l\'institution, détecte les anomalies et rédige les rapports d\'audit pour la direction.',
            'slug': 'auditeur'
        },
        {
            'nom_role': 'Assistant(e) Auditeur',
            'description': 'Aide à la collecte des données, à l\'analyse documentaire et à la préparation des rapports d\'audit.',
            'slug': 'assistant-auditeur'
        },
        {
            'nom_role': 'Chargé de clientèle',
            'description': 'Crée et gère les dossiers clients, collecte les informations KYC, initie les demandes de crédit et assure la satisfaction client.',
            'slug': 'charge-clientele'
        },
        {
            'nom_role': 'Assistant(e) Chargé de clientèle',
            'description': 'Accueille les clients, met à jour les fiches client, prépare les dossiers d\'ouverture de comptes et crédits.',
            'slug': 'assistant-charge-clientele'
        },
        {
            'nom_role': 'Responsable IT',
            'description': 'Supervise le parc informatique, la sécurité des données, les mises à jour systèmes et le support utilisateur.',
            'slug': 'responsable-it'
        },
        {
            'nom_role': 'Assistant(e) Responsable IT',
            'description': 'Aide à la maintenance des équipements, à la gestion des incidents et au suivi des tickets support.',
            'slug': 'assistant-responsable-it'
        },
        {
            'nom_role': 'Administrateur base de données',
            'description': 'Gère la base de données de l\'institution, optimise les performances et assure la sécurité des données.',
            'slug': 'administrateur-bdd'
        },
        {
            'nom_role': 'Assistant(e) Administrateur base de données',
            'description': 'Participe à la sauvegarde, la restauration et au monitoring des bases SQL. Apporte un soutien technique.',
            'slug': 'assistant-administrateur-bdd'
        },
        {
            'nom_role': 'Contrôleur de gestion',
            'description': 'Analyse les performances financières, suit les indicateurs clés (KPI), et propose des optimisations de rentabilité.',
            'slug': 'controleur-gestion'
        },
        {
            'nom_role': 'Assistant(e) Contrôleur de gestion',
            'description': 'Collecte et prépare les données analytiques, contribue aux tableaux de bord et analyses de coûts.',
            'slug': 'assistant-controleur-gestion'
        },
        {
            'nom_role': 'Juridique / Contentieux',
            'description': 'Gère les litiges avec les clients, les contentieux judiciaires et prépare les dossiers de mise en demeure.',
            'slug': 'juridique-contentieux'
        },
        {
            'nom_role': 'Assistant(e) Juridique / Contentieux',
            'description': 'Suit les correspondances légales, archive les documents juridiques et appuie les procédures contentieuses.',
            'slug': 'assistant-juridique-contentieux'
        },
        {
            'nom_role': 'Contrôle interne',
            'description': 'Vérifie la conformité des processus internes, détecte les fraudes et propose des mesures correctives.',
            'slug': 'controle-interne'
        },
        {
            'nom_role': 'Assistant(e) Contrôle interne',
            'description': 'Contribue aux contrôles, met à jour les grilles de conformité et appuie la rédaction des rapports de non-conformité.',
            'slug': 'assistant-controle-interne'
        },
        {
            'nom_role': 'Agent mobile',
            'description': 'Travaille sur le terrain pour collecter les données clients, les remboursements et effectuer les inscriptions.',
            'slug': 'agent-mobile'
        },
        {
            'nom_role': 'Assistant(e) Agent mobile',
            'description': 'Prépare les fiches terrain, accompagne les tournées et collecte les documents KYC des clients.',
            'slug': 'assistant-agent-mobile'
        },
        {
            'nom_role': 'Formateur interne',
            'description': 'Conçoit et dispense les formations internes aux agents de crédit, de caisse et recouvrement.',
            'slug': 'formateur-interne'
        },
        {
            'nom_role': 'Assistant(e) Formateur interne',
            'description': 'Prépare le matériel de formation, assiste pendant les sessions et compile les résultats d\'évaluation.',
            'slug': 'assistant-formateur-interne'
        },
        {
            'nom_role': 'Responsable des risques',
            'description': 'Analyse les risques opérationnels et financiers, suit les indicateurs de risque et élabore des plans d\'atténuation.',
            'slug': 'responsable-risques'
        },
        {
            'nom_role': 'Assistant(e) Responsable des risques',
            'description': 'Met à jour les tableaux de suivi de risque, prépare les rapports d\'exposition et effectue des pré-analyses.',
            'slug': 'assistant-responsable-risques'
        },
        {
            'nom_role': 'Archiviste',
            'description': 'Gère l\'archivage physique et numérique de tous les documents administratifs, comptables et RH.',
            'slug': 'archiviste'
        },
        {
            'nom_role': 'Assistant(e) Archiviste',
            'description': 'Trie, étiquette et numérise les documents pour le système d\'archivage centralisé.',
            'slug': 'assistant-archiviste'
        },
        {
            'nom_role': 'Community Manager',
            'description': 'Gère les réseaux sociaux, anime la communauté en ligne et améliore la visibilité numérique de l\'institution.',
            'slug': 'community-manager'
        },
        {
            'nom_role': 'Assistant(e) Community Manager',
            'description': 'Programme les publications, modère les commentaires et prépare les visuels numériques.',
            'slug': 'assistant-community-manager'
        },
        {
            'nom_role': 'Responsable de la communication',
            'description': 'Supervise la stratégie de communication interne et externe, les supports et événements institutionnels.',
            'slug': 'responsable-communication'
        },
        {
            'nom_role': 'Assistant(e) Responsable de la communication',
            'description': 'Rédige les contenus, gère les supports de communication et assure le relais avec les prestataires.',
            'slug': 'assistant-responsable-communication'
        },
        {
            'nom_role': 'Administrateur Système',
            'description': 'Gère l\'ensemble de l\'infrastructure informatique, supervise les serveurs, la gestion des utilisateurs, les sauvegardes, la configuration des réseaux et assure la disponibilité et la performance du système d\'information.',
            'slug': 'administrateur-systeme'
        },
        {
            'nom_role': 'Sécurité Informatique',
            'description': 'Met en œuvre et surveille les politiques de sécurité informatique, protège les données sensibles, détecte les menaces, gère les accès, effectue les audits de sécurité et répond aux incidents.',
            'slug': 'securite-informatique'
        },
        {
            'nom_role': 'Assistant(e) Sécurité Informatique',
            'description': 'Appuie le responsable sécurité informatique dans la surveillance des journaux système, l\'analyse des alertes, le déploiement des correctifs et la mise en œuvre des protocoles de cybersécurité.',
            'slug': 'assistant-securite-informatique'
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    print("🚀 Insertion des rôles métiers dans la base de données")
    print("=" * 60)
    
    for role_data in roles_data:
        try:
            # Vérifier si le rôle existe déjà
            role, created = Role.objects.get_or_create(
                slug=role_data['slug'],
                defaults={
                    'nom_role': role_data['nom_role'],
                    'description': role_data['description']
                }
            )
            
            if created:
                print(f"✅ Créé: {role_data['nom_role']}")
                created_count += 1
            else:
                # Mettre à jour si nécessaire
                if role.nom_role != role_data['nom_role'] or role.description != role_data['description']:
                    role.nom_role = role_data['nom_role']
                    role.description = role_data['description']
                    role.save()
                    print(f"🔄 Mis à jour: {role_data['nom_role']}")
                    updated_count += 1
                else:
                    print(f"⏭️  Existe déjà: {role_data['nom_role']}")
                    
        except Exception as e:
            print(f"❌ Erreur pour {role_data['nom_role']}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Résumé:")
    print(f"   ✅ Rôles créés: {created_count}")
    print(f"   🔄 Rôles mis à jour: {updated_count}")
    print(f"   📋 Total rôles traités: {len(roles_data)}")
    print(f"   📈 Total rôles en base: {Role.objects.count()}")
    
    print("\n🎯 Vous pouvez maintenant voir tous les rôles dans:")
    print("   - Admin Django: http://127.0.0.1:8000/admin/roles_permissions/role/")
    print("   - phpMyAdmin: Table 'roles_permissions_role'")

if __name__ == "__main__":
    insert_roles()
