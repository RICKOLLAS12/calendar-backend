# Calendar Backend API

[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-blue.svg)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-Auth-orange.svg)](https://jwt.io/)
[![Swagger](https://img.shields.io/badge/Swagger-UI-red.svg)](https://swagger.io/)

Une API REST complète pour une application de calendrier avec système de collaboration, développée avec Django REST Framework.

## 🌟 Fonctionnalités

### 📅 Gestion du Calendrier
- ✅ Création, modification et suppression d'événements
- ✅ Événements personnels et tâches assignées
- ✅ Filtrage automatique par utilisateur
- ✅ Support des couleurs et lieux personnalisés

### 🤝 Système de Collaboration
- ✅ Envoi de demandes de collaboration
- ✅ Acceptation/refus des demandes
- ✅ Gestion des relations collaboratives
- ✅ Assignation de tâches aux collaborateurs

### 🔐 Authentification & Autorisation
- ✅ Authentification JWT (JSON Web Tokens)
- ✅ Inscription et connexion sécurisées
- ✅ Gestion des utilisateurs (admin)
- ✅ Changement de mot de passe

### 🛡️ Sécurité
- ✅ Rate limiting anti-abus
- ✅ Permissions strictes par endpoint
- ✅ Protection CSRF
- ✅ Logging complet des actions

### 📚 Documentation
- ✅ Documentation Swagger/OpenAPI interactive
- ✅ Tests possibles directement dans l'interface
- ✅ Exemples de requêtes pour chaque endpoint

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.2.8
- **API** : Django REST Framework 3.16.1
- **Authentification** : JWT (djangorestframework-simplejwt)
- **Documentation** : drf-spectacular (Swagger/OpenAPI)
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Internationalisation** : Support français/anglais

## 🚀 Installation & Configuration

### Prérequis
- Python 3.13+
- pip
- virtualenv (recommandé)

### 1. Clonage du projet
```bash
git clone <repository-url>
cd calendar-backend
```

### 2. Environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 4. Migration de la base de données
```bash
python manage.py migrate
```

### 5. Création d'un superutilisateur
```bash
python manage.py createsuperuser
```

### 6. Lancement du serveur
```bash
python manage.py runserver
```

L'API sera accessible sur : `http://127.0.0.1:8000/`

## 📖 API Documentation

### Endpoints Principaux

#### 🔐 Authentification
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/auth/register/` | POST | Inscription utilisateur |
| `/api/auth/login/` | POST | Connexion JWT |
| `/api/auth/change-password/` | POST | Changement mot de passe |

#### 📅 Événements
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/events/events/` | GET | Lister ses événements |
| `/api/events/events/` | POST | Créer un événement |
| `/api/events/events/{id}/` | GET | Détails d'un événement |
| `/api/events/events/{id}/` | PUT | Modifier un événement |
| `/api/events/events/{id}/` | DELETE | Supprimer un événement |

#### 🤝 Collaborations
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/collaborations/send/` | POST | Envoyer demande collab |
| `/api/collaborations/requests/` | GET | Lister demandes |
| `/api/collaborations/requests/{id}/accept/` | POST | Accepter demande |
| `/api/collaborations/requests/{id}/reject/` | POST | Refuser demande |
| `/api/collaborations/collaborators/` | GET | Lister collaborateurs |

#### 👥 Gestion Utilisateurs (Admin)
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/users/` | GET/POST | Lister/Créer utilisateurs |
| `/api/users/{id}/` | GET/PUT/DELETE | Gestion utilisateur |
| `/api/users/{id}/activate/` | POST | Activer utilisateur |
| `/api/users/{id}/deactivate/` | POST | Désactiver utilisateur |

### 📋 Documentation Interactive

Accédez à la documentation complète sur :
- **Swagger UI** : `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc** : `http://127.0.0.1:8000/api/schema/redoc/`

## 💡 Exemples d'utilisation

### 1. Inscription
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 2. Connexion
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### 3. Créer un événement
```bash
curl -X POST http://127.0.0.1:8000/api/events/events/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Réunion équipe",
    "description": "Discussion projet",
    "start_date": "2025-11-24T10:00:00Z",
    "end_date": "2025-11-24T11:00:00Z",
    "location": "Salle de réunion",
    "color": "#3788d8",
    "assigned_to": 1
  }'
```

### 4. Lister ses événements
```bash
curl -X GET http://127.0.0.1:8000/api/events/events/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🏗️ Structure du Projet

```
calendar-backend/
├── manage.py                          # Script de gestion Django
├── calendar_management/               # Configuration principale
│   ├── settings.py                    # Paramètres Django
│   ├── urls.py                        # Routes principales
│   ├── throttling.py                  # Configuration rate limiting
│   ├── logging_utils.py               # Utilitaires de logging
│   └── management/commands/           # Commandes personnalisées
│       └── view_logs.py               # Commande de visualisation logs
├── auth/                              # Application authentification
│   ├── models.py                      # Modèles auth (vide)
│   ├── views.py                       # Vues login/register
│   ├── serializers.py                 # Sérialiseurs auth
│   └── urls.py                        # Routes auth
├── events/                            # Application événements
│   ├── models.py                      # Modèle Event
│   ├── views.py                       # API événements
│   ├── serializers.py                 # Sérialiseurs événements
│   └── urls.py                        # Routes événements
├── collaborations/                    # Application collaborations
│   ├── models.py                      # Modèles CollaborationRequest/Collaboration
│   ├── views.py                       # API collaborations
│   ├── serializers.py                 # Sérialiseurs collaborations
│   └── urls.py                        # Routes collaborations
├── user/                              # Application gestion utilisateurs
│   ├── models.py                      # Modèle UserProfile
│   ├── views.py                       # API gestion users (admin)
│   ├── serializers.py                 # Sérialiseurs users
│   └── urls.py                        # Routes users
├── logs/                              # Fichiers de logs
├── locale/                            # Traductions i18n
└── README.md                          # Cette documentation
```

## 🔧 Commandes Utiles

### Gestion des logs
```bash
# Voir tous les logs
python manage.py view_logs

# Logs API seulement
python manage.py view_logs --type=api

# Logs de sécurité
python manage.py view_logs --type=security

# Rechercher dans les logs
python manage.py view_logs --grep="login"
```

### Gestion de la base de données
```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Tests et vérifications
```bash
# Vérifier la configuration
python manage.py check

# Lancer les tests
python manage.py test
```

## 🌍 Internationalisation

Le projet supporte plusieurs langues :
- 🇫🇷 Français (par défaut)
- 🇺🇸 Anglais

Les messages d'erreur et l'interface sont automatiquement traduits selon la langue du navigateur.

## 🔒 Sécurité

### Rate Limiting
- **Connexion** : 5 tentatives/minute
- **Inscription** : 3 inscriptions/heure
- **API générale** : 100/heure (anonymes), 1000/heure (connectés)

### Permissions
- **Admin seulement** : Gestion des utilisateurs
- **Utilisateur connecté** : Gestion de ses événements
- **Collaborateur** : Assignation de tâches

### Logging
- **Sécurité** : Tentatives de connexion, modifications sensibles
- **API** : Toutes les requêtes avec user/IP
- **Erreurs** : Exceptions et erreurs 500

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de code
- PEP 8 pour Python
- Docstrings pour toutes les fonctions
- Tests unitaires pour les nouvelles fonctionnalités
- Mise à jour de la documentation

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement
- Consulter la documentation Swagger

---

**Développé avec ❤️ par l'équipe Calendar Backend**