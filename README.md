# ShopDjango – Site e-commerce complet avec Django

Site e-commerce fonctionnel développé avec **Django 5+**, Bootstrap 5 et SQLite.

## Fonctionnalités

| Module | Fonctionnalités |
|---|---|
| **Authentification** | Inscription, connexion, déconnexion, profil utilisateur |
| **Produits** | Liste, détail, recherche, filtrage par catégorie, pagination |
| **Panier** | Ajout, suppression, modification des quantités, total automatique |
| **Commandes** | Création, récapitulatif, simulation de paiement, historique |
| **Interface** | Bootstrap 5, navbar dynamique, messages flash |
| **Admin** | Gestion complète produits / commandes / utilisateurs |

## Arborescence du projet

```
TEST/
├── ecommerce/          # Configuration principale du projet
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/              # App produits
│   ├── models.py       # Category, Product
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── accounts/           # App authentification & profil
│   ├── models.py       # UserProfile
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── cart/               # App panier (session)
│   ├── models.py       # Classe Cart (session-based)
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── context_processors.py
├── orders/             # App commandes
│   ├── models.py       # Order, OrderItem
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/          # Templates HTML organisés par app
│   ├── base.html
│   ├── store/
│   ├── accounts/
│   ├── cart/
│   └── orders/
├── static/             # Fichiers statiques (CSS personnalisé)
├── media/              # Images uploadées
├── manage.py
└── requirements.txt
```

## Installation

### Prérequis

- Python 3.10+
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Salimou95/TEST.git
cd TEST

# 2. Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate       # Linux / macOS
# .\venv\Scripts\activate      # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. (Optionnel) Créer un superutilisateur
python manage.py createsuperuser

# 6. Lancer le serveur de développement
python manage.py runserver
```

L'application est accessible sur **http://127.0.0.1:8000/**

## Accès

| URL | Description |
|---|---|
| `/` | Page d'accueil – liste des produits |
| `/category/<slug>/` | Produits filtrés par catégorie |
| `/product/<id>/<slug>/` | Détail d'un produit |
| `/cart/` | Panier |
| `/orders/create/` | Passer une commande |
| `/orders/history/` | Historique des commandes |
| `/accounts/register/` | Inscription |
| `/accounts/login/` | Connexion |
| `/accounts/profile/` | Profil utilisateur |
| `/admin/` | Interface d'administration Django |

## Variables de configuration importantes (`ecommerce/settings.py`)

| Variable | Valeur par défaut | Description |
|---|---|---|
| `PRODUCTS_PER_PAGE` | `8` | Nombre de produits par page |
| `CART_SESSION_ID` | `'cart'` | Clé de session du panier |
| `MEDIA_ROOT` | `BASE_DIR / 'media'` | Répertoire des images uploadées |
| `LANGUAGE_CODE` | `'fr-fr'` | Langue du projet |

## Gestion des images produits

Les images sont uploadées dans `media/products/YYYY/MM/`. Assurez-vous que le répertoire `media/` est accessible en écriture.

Pour la production, configurez `MEDIA_ROOT` et servez les médias via votre serveur web (nginx, Apache...).

## Technologies utilisées

- **Django 5+** – framework web Python
- **SQLite** – base de données (par défaut)
- **Pillow** – traitement d'images
- **Bootstrap 5** – framework CSS
- **Bootstrap Icons** – icônes

## Licence

MIT
