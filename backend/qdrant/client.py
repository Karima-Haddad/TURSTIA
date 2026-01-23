from qdrant_client import QdrantClient
from backend.config import QDRANT_URL, QDRANT_API_KEY

_qdrant_client = None


def get_qdrant_client():
    """
    Retourne une instance unique du client Qdrant (Cloud)
    """
    global _qdrant_client

    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )

    return _qdrant_client
