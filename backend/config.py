# config centralisée 
# ===============================
# Vector & Embedding Configuration
# ===============================

TEXT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
IMAGE_EMBEDDING_MODEL = "openclip-vit-b32"  # optionnel

USE_IMAGE_EMBEDDING = True   # tu peux le désactiver si besoin

# ===============================
# Vector Fusion
# ===============================

NORMALIZE_L2 = True

# ===============================
# Qdrant Configuration
# ===============================

QDRANT_COLLECTION = "credit_cases"
QDRANT_DISTANCE = "Cosine"
TOP_K_SIMILAR = 10

# ===============================
# Similarity Thresholds
# ===============================

SIMILARITY_THRESHOLD = 0.5
FRAUD_SIMILARITY_THRESHOLD = 0.80

# ===============================
# Evaluation
# ===============================

PRECISION_K = 5

# ===============================
# Performance
# ===============================

ENABLE_LATENCY_LOGGING = True

# ===============================
# Qdrant Cloud Configuration
# ===============================

QDRANT_URL = "https://880b58fd-3475-43fb-b1d1-3d084b21b497.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "xxx"
QDRANT_COLLECTION = "credit_cases"