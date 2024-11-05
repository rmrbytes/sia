#config.py

import os
from decimal import Decimal, InvalidOperation
from typing import List

#Configuration class for loading environment variables and setting static constants.
class Settings:

    def __init__(self) -> None:
        # Directory paths
        self.data_dir = os.getenv("DATA_DIR", "data")
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.agents_dir = os.path.join(self.data_dir, "agents")
        self.models_dir = os.path.join(self.data_dir, "models")
        self.store_dir = os.path.join(self.data_dir, "store")
        
        # Adding DEBUG 
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

        # Database settings
        self.database_url = f"./{self.data_dir}/sia.db"

        # Security settings
        self.secret_key = os.getenv("SECRET_KEY", "some secret key")
        self.header_name = "X-Requested-With"  # header name for requests
        self.header_key = os.getenv("X_API_KEY", "")  # API Key
        self.algorithm = "HS256"  # Algorithm used for encoding JWT
        self.is_https = os.getenv("USE_HTTPS", "false").strip().lower() == "true"

        # Token settings
        access_token_expiry_hours = self._get_env_int("ACCESS_TOKEN_EXPIRY_IN_HOURS", 24)
        self.access_token_expire_minutes = access_token_expiry_hours * 60  # Convert hours to minutes

        # embeddings-server info
        self.embeddings_server = os.getenv("EMBEDDINGS_SERVER", "embeddings-server")
        self.embeddings_server_port = self._get_env_int("EMBEDDINGS_SERVER_PORT", 8002) # port used by the embeddings-server
        
        # chunking strategy
        self.split_by = os.getenv("SPLIT_BY", "sentence")
        self.split_length = self._get_env_int("SPLIT_LENGTH", 5)
        self.split_overlap = self._get_env_int("SPLIT_OVERLAP", 0)
        self.split_threshold = self._get_env_int("SPLIT_THRESHOLD", 0)

        # llm-server info
        self.inference_server = os.getenv("INFERENCE_SERVER", "llm-server")
        self.inference_server_port = self._get_env_int("INFERENCE_SERVER_PORT", 8000) # port used by the llm-server
        self.llm_model_name = os.getenv("LLM_MODEL_NAME", "microsoft/Phi-3-mini-4k-instruct")
        
        # chat params
        self.chat_response_length_default = os.getenv("CHAT_RESPONSE_LENGTH_DEFAULT", "M")
        self.chat_response_length_short = self._get_env_int("CHAT_RESPONSE_LENGTH_SHORT", 50)
        self.chat_response_length_medium = self._get_env_int("CHAT_RESPONSE_LENGTH_SHORT", 150)
        self.chat_response_length_long = self._get_env_int("CHAT_RESPONSE_LENGTH_SHORT", 300)
        self.chat_temperature = self._get_env_float("CHAT_TEMPERATURE", 0.7)
        self.chat_max_tokens = self._get_env_int("CHAT_MAX_TOKENS", default=200)
        self.chat_top_p = self._get_env_float("CHAT_TOP_P", 0.9)
        self.chat_frequency_penalty = self._get_env_float("CHAT_FREQUENCY_PENALTY", 0.0)  # Values from 0.0 to 2.0
        self.chat_presence_penalty = self._get_env_float("CHAT_PRESENCE_PENALTY", 0.0)

        # Allowed hosts handling
        #allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "")
        #self.allowed_hosts = self._parse_allowed_hosts(allowed_hosts_str)

    def _get_env_int(self, key: str, default: int) -> int:
        # Helper function to safely get an integer environment variable.
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
    
    def _parse_allowed_hosts(self, hosts_str: str) -> List[str]:
        # Helper function to parse the ALLOWED_HOSTS environment variable into a list.
        # Split the string by commas, strip spaces, and filter out empty strings
        return [host.strip() for host in hosts_str.split(",") if host.strip()]


# Instantiate settings object
settings = Settings()
