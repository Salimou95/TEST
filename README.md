# E-Shop — Site e-commerce Django

Un site e-commerce complet construit avec Django 5+, Bootstrap 5, et une base de données SQLite.

## Fonctionnalités

- **Authentification** : inscription, connexion, déconnexion, profil utilisateur
- **Produits** : liste avec pagination, détail, recherche et filtre par catégorie
- **Panier** : ajout/suppression/modification de quantités, calcul automatique du total (stocké en session)
- **Commandes** : récapitulatif, simulation de paiement, historique
- **Admin Django** : gestion complète produits / commandes / utilisateurs
- **Interface** Bootstrap 5 responsive avec navbar dynamique (badge panier)

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend   | Django 5+ (Python 3.12) |
| Frontend  | Bootstrap 5 + Bootstrap Icons |
| Base de données | SQLite (défaut Django) |
| Images    | Pillow + MEDIA_URL |

## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd TEST
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. (Optionnel) Charger les données de démonstration

```bash
python manage.py populate_demo
```

Cela crée :
- 5 catégories (Électronique, Vêtements, Livres, Sport, Maison)
- 12 produits d'exemple
- Un superutilisateur `admin` / mot de passe `admin123`

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application est accessible sur **http://127.0.0.1:8000/**

L'interface d'administration est sur **http://127.0.0.1:8000/admin/**

## Structure du projet

```
TEST/
├── ecommerce/          # Configuration du projet Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/              # Application produits
│   ├── models.py       # Category, Product
│   ├── views.py        # Liste, détail, recherche
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/populate_demo.py
├── cart/               # Application panier (session)
│   ├── cart.py         # Classe Cart
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── context_processors.py
├── orders/             # Application commandes
│   ├── models.py       # Order, OrderItem
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── accounts/           # Application utilisateurs
│   ├── models.py       # UserProfile
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── templates/          # Templates HTML (Bootstrap 5)
│   ├── base.html
│   ├── store/
│   ├── cart/
│   ├── orders/
│   └── accounts/
├── static/             # Fichiers statiques (CSS, JS, images)
├── media/              # Fichiers uploadés (images produits)
├── requirements.txt
└── README.md
```

## URLs

| URL | Description |
|-----|-------------|
| `/` | Liste des produits |
| `/category/<slug>/` | Produits par catégorie |
| `/product/<id>/<slug>/` | Détail d'un produit |
| `/cart/` | Panier |
| `/orders/create/` | Passer une commande |
| `/orders/my-orders/` | Historique des commandes |
| `/accounts/register/` | Inscription |
| `/accounts/login/` | Connexion |
| `/accounts/profile/` | Profil utilisateur |
| `/admin/` | Interface d'administration |

## Créer un superutilisateur manuellement

```bash
python manage.py createsuperuser
```
