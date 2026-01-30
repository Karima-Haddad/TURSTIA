# TRUSTIA — Credit Decision & Explainability Platform ✅

**Résumé:** TRUSTIA est un prototype full‑stack pour l'évaluation de dossiers de crédit basé sur des embeddings textuels et Qdrant (vector DB). Le backend orchestre des agents métier (document parsing, embedding, retrieval, fraud, risk, scenario, explanation) et expose une API FastAPI ; le frontend Angular fournit une UI pour la soumission, la visualisation (Similarity Radar) et l'explication des décisions.

---

## 🧭 Table des matières
- [Aperçu](#aperçu)
- [Architecture & composants](#architecture--composants)
- [Installation rapide](#installation-rapide)
- [Configuration (variables d'environnement)](#configuration-variables-denvironnement)
- [Démarrage local](#démarrage-local)
- [Endpoints API clés & formats](#endpoints-api-clés--formats)
- [Seeding Qdrant](#seeding-qdrant)
- [Tests & CI](#tests--ci)
- [Debug & troubleshooting](#debug--troubleshooting)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Aperçu
- Langages: **Python (backend)**, **TypeScript/Angular (frontend)**
- DB vecteurs: **Qdrant**
- Embeddings: **sentence-transformers/all-MiniLM-L6-v2**
- UI: dashboard avec `SimilarityRadar` (visualisation des cas similaires)

---

## Architecture & composants 🔧
- backend/
  - `app.py` — FastAPI server and routes
  - `agents/` — modules: embedding_agent, retrieval_agent (Qdrant), fraud_agent, risk_agent, scenario_agent, explanation_agent, supervisor_agent
  - `utils/` — helpers (e.g., `radar_builder.py`)
  - `qdrant/` — client wrappers and schema
  - `tests/` — pytest unit tests

- frontend/
  - Angular app (standalone components)
  - `similarity-radar/` — `similarity-radar.ts|html|css` (visualisation)
  - Services: communication avec l'API (submission / evaluate)

---

## Installation rapide
Prérequis: Python 3.10+, Node 18+, npm, accès à Qdrant (local ou cloud).

1) Backend
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2) Frontend
```bash
cd frontend
npm install
```

---

## Configuration (variables d'environnement) ⚙️
Les variables suivantes doivent être renseignées (ou modifiez `backend/config.py` pour le développement):

- `QDRANT_URL` — URL Qdrant (ex: https://...:6333)
- `QDRANT_API_KEY` — clef API Qdrant (si cloud)
- `QDRANT_COLLECTION` — nom collection (ex: credit_cases)
- `JWT_SECRET` / `JWT_ALGORITHM` — pour auth (si utilisé)

> Conseil: pour le développement vous pouvez définir ces variables dans votre shell ou créer un `.env` et les charger via `python-dotenv`.

---

## Démarrage local
1) Lancer le backend
```bash
uvicorn backend.app:app --reload --port 8000
```
- Swagger UI: `http://localhost:8000/docs`

2) Lancer le frontend
```bash
cd frontend
npm start
# ou
ng serve -o
```
- Frontend: `http://localhost:4200`

3) Vérifier Qdrant
- Health: `GET {QDRANT_URL}/health`

---

## Endpoints API clés & formats 📡
Les endpoints principaux se trouvent dans `backend/api/`.

- POST /submission — envoyer un dossier (payload minimal):
```json
{
  "case_id": "CASE-123",
  "applicant_form": { /* fields */ },
  "loan_request": { "loan_amount": 15000, "term_months": 24 },
  "documents": [ /* uploaded files or attachments */ ]
}
```
Réponse (extrait):
```json
{
  "case_id": "CASE-123",
  "mode": "NORMAL",
  "decision": "ACCEPT",
  "confidence": 0.82,
  "radar_points": [
    {"type": "CURRENT", "case_id": "CASE-123", "score": 1.0},
    {"type": "NORMAL",  "case_id": "CASE-111", "score": 0.72},
    {"type": "FRAUD",   "case_id": "CASE-040", "score": 0.85}
  ]
}
```

- GET /health — status du service

> Note: `radar_points` est utilisé par le frontend pour afficher le `SimilarityRadar`. Chaque point doit contenir `type` (CURRENT|NORMAL|FRAUD), `case_id` et `score` (0..1).

---

## Seeding Qdrant (notebook)
Le notebook `backend/qdrant/Seed.ipynb` :
- génère un dataset synthétique, crée des textes descriptifs, calcule des embeddings et upsert vers Qdrant.

Procédure rapide:
1. Ouvrir le notebook ou exécuter les scripts Python en local
2. Définir `QDRANT_URL` et `QDRANT_API_KEY`
3. Exécuter les cellules pour créer collection et upsert points

---

## Tests & qualité
- Backend (pytest):
```bash
pip install pytest
pytest backend/tests -q
```
- Frontend: `npm test` (exécute karma/jasmine)
- Lint/format: Prettier (frontend), (optionnel) flake8/black (backend)

---

## Debug & Troubleshooting 🐞
- Points du radar non affichés → Vérifier en console du navigateur
  - `RADAR POINTS FROM BACKEND:` (console Angular)
  - `Positioned:` (points calculés)
  - Attention: si `score` est `NaN` ou absent le point sera ignoré (vérifier `radar_builder` côté backend).
  - Si `score === 1.0` le point peut se superposer au `CURRENT` (centre). Essayez de changer temporairement la taille ou ajouter un stroke dans `similarity-radar.css`.

- Erreur Qdrant collection/dimension → Vérifier `backend/qdrant/client.py::check_collection_config()` et la dimension d'embed (384)

- Connexion Qdrant refusée → vérifier `QDRANT_URL`/`QDRANT_API_KEY` et règles réseau (firewall)

- Tests qui échouent → Exécuter `pytest -k <test_name>` pour isoler un test.

---

## Commandes utiles
| Commande | Description |
|---|---|
| `uvicorn backend.app:app --reload` | Lancer backend en dev |
| `cd frontend && npm start` | Lancer frontend |
| `pytest backend/tests` | Lancer tests backend |
| `ng test` | Lancer tests frontend |
| `python backend/qdrant/Seed.ipynb` | (ouvrir/exécuter le notebook) seed Qdrant |

---

## Contribuer 🤝
- Fork → feature branch → tests → PR
- Ajouter tests unitaires pour nouvelles fonctionnalités backend
- Mettre à jour `docs/` pour changements d'architecture

---

## Limitations connues & idées d'amélioration
- Pipeline POC : manque d'authentification fine et contrôle d'accès pour la prod
- Ajouter CI (GitHub Actions) pour tests + lint + build
- Dockerisation du backend & frontend pour déploiement reproductible
- Visualisation interactive du `SimilarityRadar` (zoom, filtre par type)

---

## Licence
MIT (ou adapter selon votre organisation)

---

## Contact
Pour questions/bugs : ouvrir une issue dans le dépôt.

> Si vous voulez, j'ajoute une section "Exemples d'API détaillés" ou des badges CI/coverage — dites-moi lesquels vous préférez. 🔧✨

## Architecture (vue d'ensemble)
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Angular SPA)                   │
│   - UI, Upload documents, Affichage résultats              │
│   - Services: api.service.ts pour communication             │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/REST
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (Python FastAPI/Flask)             │
│  - Orchestration (main.py, app.py)                         │
│  - Agents: document, embedding, retrieval, fraud, risk     │
│  - Services: parsing, règles métier                        │
│  - Logs audit (JSONL)                                       │
└────┬─────────────────────────────────────────────────┬──────┘
     │                                                  │
     ▼                                                  ▼
┌─────────────────────┐                    ┌──────────────────────┐
│   Qdrant (Vector DB)│                    │  Storage             │
│ - Embeddings        │                    │ - Documents (bruts)  │
│ - Métadonnées       │                    │ - Fichiers temp      │
│ - Recherche vect.   │                    │ - Logs audit         │
└─────────────────────┘                    └──────────────────────┘

## Fonctionnalités
- Ingestion et analyse de documents (extraction texte + signaux)
- Embeddings et indexation dans Qdrant
- Recherche vectorielle et agrégation des cas similaires
- Détection de fraude, scoring de risque, décision et explication
- Audit structuré (JSONL)
- Dashboard Angular avec visualisations (dont similarity radar)



## Pipeline
1) Soumission dossier + documents  
2) Analyse documents  
3) Fusion profil  
4) Embeddings  
5) Retrieval Qdrant  
6) Fraude  
7) Risque  
8) Scénarios  
9) Décision  
10) Explication + Audit  
11) Learning loop (post-décision)

## Flux principal de fonctionnement
1. Upload d'un document
Utilisateur envoie document via UI Angular.
API backend reçoit fichier → document_agent le traite.
document_parser extrait texte et métadonnées.

2. Indexation (embedding)
embedding_agent calcule embedding (vecteur).
Stockage dans Qdrant avec métadonnées.

3. Recherche & Décision
Utilisateur soumet requête de recherche.
retrieval_agent envoie requête vectorielle à Qdrant.
Résultats post-traités par decision_agent (règles métier, scoring).

4. Audit & Traçabilité
Chaque action critiques loggée dans backend/logs/audit_log.jsonl.
Format JSONL pour parsing et analytics.

5. Détection de fraude (optionnel)
fraud_agent analyse patterns suspects.
risk_agent scores le risque global.

## Arborescence (fichiers clés)
Project-root/
├── README.md                          # Ce fichier
├── backend/
│   ├── main.py                        # Point d'entrée / orchestration
│   ├── app.py                         # Configuration application & routes
│   ├── config.py                      # Paramètres d'environnement
│   ├── requirements.txt                # Dépendances Python
│   ├── agents/                         # Agents métier
│   │   ├── document_agent.py          # Ingestion / normalisation
│   │   ├── embedding_agent.py         # Conversion en vecteurs
│   │   ├── retrieval_agent.py         # Recherche vectorielle
│   │   ├── fraud_agent.py             # Détection fraude
│   │   ├── decision_agent.py          # Logique décision
│   │   ├── risk_agent.py              # Scoring risque
│   │   ├── audit_agent.py             # Audit & traçabilité
│   │   └── ...
│   ├── services/
│   │   ├── document_parser.py         # Extraction texte/métadonnées
│   │   └── fraud_service.py           # Orchestration fraude
│   ├── schemas/
│   │   ├── application_package.py     # DTO application
│   │   └── document_analysis.py       # DTO analyse document
│   ├── qdrant/
│   │   ├── client.py                  # Intégration Qdrant
│   │   ├── schema.py                  # Schéma vecteurs
│   │   └── Seed.py                    # Alimentation de la base
│   ├── api/
│   │   ├── evaluate.py                # Endpoint d'évaluation
│   │   └── submission.py              # Endpoint de soumission
│   ├── evaluation/
│   │   ├── latency.py                 # Mesure latence
│   │   ├── precision_k.py             # Calcul précision@K
│   │   └── umap_visualization.py      # Visualisation embeddings
│   ├── tests/                         # Suite de tests
│   │   ├── test_retrieval.py
│   │   ├── test_embedding.py
│   │   ├── test_pipeline.py
│   │   ├── test_decision_agent.py
│   │   └── ...
│   ├── logs/
│   │   └── audit_log.jsonl            # Logs d'audit
│   ├── storage/                       # Documents indexés
│   ├── tmp_docs/                      # Fichiers temporaires
│   └── utils/
│       ├── audit_logger.py            # Logging audit
│       ├── io.py                      # I/O utilitaires
│       └── timers.py                  # Mesure performances
├── frontend/
│   ├── package.json                   # Dépendances npm
│   ├── angular.json                   # Config Angular CLI
│   ├── tsconfig.json                  # Config TypeScript
│   ├── src/
│   │   ├── main.ts                    # Bootstrap app
│   │   ├── app/
│   │   │   ├── app.ts                 # Composant root
│   │   │   ├── app.routes.ts          # Routes principales
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts     # Communication backend
│   │   │   │   └── application.service.ts
│   │   │   ├── features/
│   │   │   │   └── submission/        # Feature soumission
│   │   │   ├── audit/                 # Vue audit
│   │   │   ├── outcome/               # Affichage résultats
│   │   │   └── similarity-radar/      # Visualisation
│   │   └── index.html                 # Template HTML
│   └── README.md
└── docs/
    ├── 00_Project_Vision.md           # Vision projet
    ├── 01_Architecture.md             # Architecture détaillée
    ├── 02_Data_Schema.md              # Schémas données
    └── 03_Demo_Script.md              # Script démo

## Configuration
Configurer `backend/config.py`  :
```bash
QDRANT_URL = "https://880b58fd-3475-43fb-b1d1-3d084b21b497.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.LHDHXiBzEP64sRK8XDGN81SFO_3F2CePlTTemz38KVM"
QDRANT_COLLECTION = "credit_cases"
```


## Lancement local

### 1) Démarrer le backend
```bash
uvicorn backend.app:app --reload --port 8000
```
API dispo sur `http://localhost:8000` (Swagger: `http://localhost:8000/docs`).

### 2) Démarrer le frontend
```bash
cd frontend
npm run start
# ou avec Angular CLI
ng serve -o
```
SPA dispo sur `http://localhost:4200`.

### 3) Vérifier les connexions
- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:4200`

## Tests
```bash
# Tests unitaires
python -m backend.tests

# Exemple ciblé
pytest backend\tests\test_retrieval.py -v
```

### Tests disponibles (extraits)
Tests disponibles
Fichier	Objectif
test_retrieval.py			---> Recherche vectorielle Qdrant
test_embedding.py			---> Génération embeddings
test_pipeline.py			---> End-to-end pipeline
test_decision_agent.py		---> Logique décision
test_risk_agent.py			---> Scoring risque

## Évaluation & Benchmarking

Latency
```bash
python -m  backend.evaluation.latency.py
```
Mesure les temps de réponse API.

Precision@K
```bash
python backend.evaluation.precision_k.py
```
Calcule accuracy de la recherche vectorielle.

Visualisation
```bash
python backend.evaluation.umap_visualization.py
```
Génère graph 2D des embeddings (UMAP).

## Logs et audits des modifications des dossiers
Format structuré (JSONL) dans les logs.


```bash
python -m backend.evaluation.latency
python backend.evaluation.precision_k
python backend.evaluation.umap_visualization
```
## Documentation
- `docs/00_Project_Vision.md`
- `docs/01_Architecture.md`
- `docs/02_Data_Schema.md`
- `docs/03_Demo_Script.md`

