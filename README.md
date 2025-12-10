# ⚡ EDF SEI Corse - Suivi des Concentrateurs CPL

Une solution moderne et performante pour le suivi du cycle de vie des concentrateurs CPL en Corse. Conçue pour le **Hackathon EDF 2025**.

---

## 🛠️ Stack Technique ("The Winning Stack")

Choix technologiques orientés **rapidité de développement**, **performance** et **expérience utilisateur**.

### 🔙 Backend (High Performance)
*   **[FastAPI](https://fastapi.tiangolo.com/)** : API Python ultra-rapide, validation automatique des données (Pydantic) et documentation auto-générée (Swagger UI).
*   **[SQLAlchemy](https://www.sqlalchemy.org/)** : ORM robuste pour la gestion de la base de données.
*   **[SQLite](https://www.sqlite.org/index.html)** : Base de données légère, sans configuration serveur ("Serverless"), idéale pour le déploiement rapide et le mode hors-ligne.

### 🔜 Frontend (Modern & Responsive)
*   **[Vue.js 3](https://vuejs.org/)** : Framework JS progressif et réactif.
*   **[Vite](https://vitejs.dev/)** : Build tool de nouvelle génération (Hot Module Replacement instantané).
*   **[Tailwind CSS](https://tailwindcss.com/)** : Framework CSS "Utility-first" pour un design sur-mesure rapide.
*   **[DaisyUI](https://daisyui.com/)** : Composants UI (basés sur Tailwind) pour un look "Premium" immédiat.

### 📱 "Smart Features"
*   **html5-qrcode** : Scan de codes-barres/QR Codes directement dans le navigateur (Mobile compatible).
*   **Chart.js / ApexCharts** : Visualisation de données pour le Dashboard de supervision.
*   **PWA (Progressive Web App)** : (Bonus) Support hors-ligne pour les techniciens sur le terrain.

---

## 📂 Architecture

Structure modulaire respectant les meilleures pratiques ("Separation of Concerns").

```text
PROJET_EDF_HACKATHON/
├── backend/             # API REST
│   ├── app/
│   │   ├── main.py      # Entry point
│   │   ├── models.py    # Database Models (SQLAlchemy)
│   │   ├── schemas.py   # Data Validation (Pydantic)
│   │   ├── database.py  # SQLite Connection
│   │   └── routers/     # API Endpoints Modules
│   └── edf_track.db     # Base de données locale
│
└── frontend/            # Interface Utilisateur (SPA)
    ├── src/
    │   ├── components/  # Composants réutilisables (Scanner, Charts...)
    │   ├── views/       # Pages (Home, Admin, Dashboard...)
    │   └── services/    # Appels API (Axios)
```

---

## 🚀 Installation & Démarrage

### Pré-requis
*   Python 3.9+
*   Node.js 16+

### 1. Démarrer le Backend
```bash
cd backend
python3 -m venv venv           # Créer l'environnement virtuel
source venv/bin/activate       # Activer (Linux/Mac)
pip install -r requirements.txt # Installer les dépendances
uvicorn app.main:app --reload  # Lancer le serveur
pytest tests/                  # Lancer les tests
```
> L'API sera accessible sur : `http://localhost:8000`  
> Documentation interactive : `http://localhost:8000/docs`

### 2. Démarrer le Frontend
```bash
cd frontend
npm install                    # Installer les dépendances
npm run dev                    # Lancer le serveur de dev
```
> L'application sera accessible sur : `http://localhost:5173`

---

## 🎯 Fonctionnalités Clés

1.  **Traçabilité Complète** : Historique de chaque mouvement (Réception, Pose, Dépose, Transfert).
2.  **Scan Mobile** : Utilisation de la caméra du smartphone pour identifier les appareils.
3.  **Dashboard Supervision** : Vue globale des stocks par localisation en temps réel.
4.  **Mode Déconnecté** : Capacité de travailler sans réseau (Sync ultérieure).