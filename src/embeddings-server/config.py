#config.py

import os

# Configuration class for loading environment variables and setting static constants
class Settings:
    # Initialize settings by loading environment variables and setting defaults
    def __init__(self) -> None:
        
        # Enables or disables debug mode.
        self.DEBUG = os.getenv("DEBUG", "false").strip().lower() == "true"
        
        #self.ner_model_name: str = os.getenv("NER_MODEL_NAME", "dbmdz/bert-large-cased-finetuned-conll03-english")
        self.embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
        self.embedding_model_filename: str = os.getenv("EMBEDDING_MODEL_FILENAME", "pytorch_model.bin") 
        self.no_workers: int = self._get_env_int("EMBEDDINGS_NO_WORKERS", 1)
        self.hf_api_token: str = os.getenv("HUGGING_FACE_HUB_TOKEN", "NONE")

        # Supported file types
        #self.file_types = os.getenv("FILE_TYPES", "txt,pdf").split(",")

        # Chunking-specific variables
        #self.tokenizer_model_name = os.getenv("CHUNKING_MODEL_NAME", "google-bert/bert-base-uncased")
        self.chunk_size = self._get_env_int("CHUNK_SIZE", 512)
        self.chunk_overlap = self._get_env_int("CHUNK_OVERLAP", 50)
        self.chunk_strategy = os.getenv("CHUNK_STRATEGY", "sentence")
        self.max_input_tokens = self._get_env_int("MAX_INPUT_TOKENS", 2048)
        self.min_chunk_size = self._get_env_int("MIN_CHUNK_SIZE", 128)
        self.max_chunk_count = self._get_env_int("MAX_CHUNK_COUNT", 0)
        if self.max_chunk_count == 0:
            self.max_chunk_count = None  # Set to None if not specified.
        # query
        # Number of top similar chunks to retrieve
        self.top_n = self._get_env_int("TOP_N", 5)
        self.retrieval_strategy = os.getenv("RETRIEVAL_STRATEGY", "knn")
        self.threshold_similarity = self._get_env_float("THRESHOLD_SIMILARITY", 0.8)
        self.mmr_lambda = self._get_env_float("MMR_LAMBDA", 0.5) 
        self.distance_metric = os.getenv("DISTANCE_METRIC", "cosine")
        #self.initial_results = self._get_env_int("INITIAL_RESULTS", 100) 

        # Directory paths
        self.data_dir: str = os.getenv("DATA_DIR", "data")
        self.base_dir: str = os.path.abspath(os.path.dirname(__file__))
        self.agents_dir: str = os.path.join(self.data_dir, "agents")
        self.models_dir: str = os.path.join(self.data_dir, "models")
        self.store_dir: str = os.path.join(self.data_dir, "store")
        
        # Security settings
        self.header_name: str = "X-Requested-With"  # Fixed header name for requests from the frontend
        self.header_key: str = "XteNATqxnbBkPa6TCHcK0NTxOM1JVkQl"  # Fixed secret key expected from the frontend
        
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
