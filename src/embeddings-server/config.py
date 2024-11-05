#config.py

import os

# Configuration class for loading environment variables and setting static constants
class Settings:
    # Initialize settings by loading environment variables and setting defaults
    def __init__(self) -> None:

        # HF Token        
        self.hf_api_token: str = os.getenv("HUGGING_FACE_HUB_TOKEN", "NONE")
        # Enables or disables debug mode.
        self.DEBUG = os.getenv("DEBUG", "false").strip().lower() == "true"
        # Security settings
        self.header_name: str = "X-Requested-With"  # header name for requests
        self.header_key: str = os.getenv("X_API_KEY", "") # header key 
        # Directory paths
        self.data_dir: str = os.getenv("DATA_DIR", "data")
        self.base_dir: str = os.path.abspath(os.path.dirname(__file__))
        self.agents_dir: str = os.path.join(self.data_dir, "agents")
        self.models_dir: str = os.path.join(self.data_dir, "models")
        self.store_dir: str = os.path.join(self.data_dir, "store")
        
        # workers, embedding model
        self.no_workers: int = self._get_env_int("EMBEDDINGS_NO_WORKERS", 1)       
        self.embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
        self.embedding_model_filename: str = os.getenv("EMBEDDING_MODEL_FILENAME", "pytorch_model.bin") 

        # Chunking-specific variables
        self.split_by = os.getenv("SPLIT_BY", "sentence")
        self.split_length = self._get_env_int("SPLIT_LENGTH", 5)
        self.split_overlap = self._get_env_int("SPLIT_OVERLAP", 0)
        self.split_threshold = self._get_env_int("SPLIT_THRESHOLD", 0)
        # Number of top similar chunks to retrieve
        self.distance_metric = os.getenv("DISTANCE_METRIC", "cosine")
        self.top_n = self._get_env_int("TOP_N", 5)
        
        # api-server info
        self.api_server = os.getenv("API_SERVER", "api-server")
        self.api_server_port = self._get_env_int("API_SERVER_PORT", 8080) # port used by the api-server

    # Helper function to safely get an integer environment variable.
    def _get_env_int(self, key: str, default: int) -> int:
        try:
            return int(os.getenv(key, default))
        except ValueError:
            return default
        
    def _get_env_float(self, key: str, default: float) -> float:
        # Helper function to safely get a float environment variable.
        try:
            return float(os.getenv(key, default))
        except (ValueError, TypeError):
            return default

# Instantiate settings object
settings = Settings()
