# TRUSTIA — Recherche Vectorielle & Détection de Fraude

##  Description
Projet full‑stack démontrant l'ingestion, l'indexation et la recherche de documents via embeddings (Qdrant), avec des agents métier Python pour parsing, retrieval et détection de fraude. Frontend moderne en Angular, backend robuste en Python.

## Architecture (vue d'ensemble)
```
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
```
## Pipeline:
1) Soumission dossier + documents  
2) Analyse documents  
3) Fusion profil  
4) Embeddings  
5) Retrieval Qdrant  
6) Fraude  
7) Risque  
8) Scenarios  
9) Decision  
10) Explication + Audit  
11) Learning loop (post-decision)


## 📁 Arborescence (fichiers clés)

```
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
│   │   └── schema.py                  # Schéma vecteurs
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
```

##  Prérequis
- **Python**: 3.9+ (vérifier `backend/requirements.txt`)
- **Node.js**: 16+ avec npm ou yarn
- **Qdrant**: instance locale (Docker) ou service cloud
- **Git**: pour versionnage et collaboration

## Installation locale

##  Lancement local

### 1. Démarrer le backend
Lancer l’API principale:
```bash
uvicorn backend.main:app --relaod
```
```bash
uvicorn backend.app:app --reload --port 8000

```
Lancer l’API learning et audit 
- API disponible sur: `http://localhost:8000` (ou port configuré)

Cette configuration multi-points d’entrée est temporaire et utilisée uniquement à des fins de test. une API FastAPI unique sera mise en place dans la version finale.

### 2. Démarrer le frontend
```bash
cd frontend
npm run start
# ou avec Angular CLI
ng serve -o
```
- SPA disponible sur: `http://localhost:4200`

### 3. Vérifier les connexions
- Accès Qdrant: `http://localhost:6333/health` (ou config)
- API backend: `http://localhost:8000/docs` (si FastAPI avec Swagger)
- Frontend: `http://localhost:4200`

##  Configuration & secrets


Dans le  fichier config.py:
```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here
QDRANT_COLLECTION
```



##  Flux principal de fonctionnement

### 1. Upload d'un document
- Utilisateur envoie document via UI Angular.
- API backend reçoit fichier → `document_agent` le traite.
- `document_parser` extrait texte et métadonnées.

### 2. Indexation (embedding)
- `embedding_agent` calcule embedding (vecteur).
- Stockage dans Qdrant avec métadonnées.

### 3. Recherche & Décision
- Utilisateur soumet requête de recherche.
- `retrieval_agent` envoie requête vectorielle à Qdrant.
- Résultats post-traités par `decision_agent` (règles métier, scoring).

### 4. Audit & Traçabilité
- Chaque action critiques loggée dans `backend/logs/audit_log.jsonl`.
- Format JSONL pour parsing et analytics.

### 5. Détection de fraude (optionnel)
- `fraud_agent` analyse patterns suspects.
- `risk_agent` scores le risque global.

## Tests

### Exécuter les tests
```bash
# Test unitaires
python -m backend.tests

# Test spécifique
pytest backend/tests/test_retrieval.py -v


```

### Tests disponibles
| Fichier | Objectif |
|---------|----------|
| `test_retrieval.py` | Recherche vectorielle Qdrant |
| `test_embedding.py` | Génération embeddings |
| `test_pipeline.py` | End-to-end pipeline |
| `test_decision_agent.py` | Logique décision |
| `test_risk_agent.py` | Scoring risque |


## 📈 Évaluation & Benchmarking

### Latency
```bash
python -m  backend.evaluation.latency.py
```
Mesure les temps de réponse API.

### Precision@K
```bash
python backend.evaluation.precision_k.py
```
Calcule accuracy de la recherche vectorielle.

### Visualisation
```bash
python backend.evaluation.umap_visualization.py
```
Génère graph 2D des embeddings (UMAP).




### Logs et audits des modifications des dossiers 
- Format structuré (JSONL) dans les logs.

