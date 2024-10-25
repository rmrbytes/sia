import os
from huggingface_hub import snapshot_download

# Use environment variables passed via docker-compose
token = os.getenv("HF_API_TOKEN")
embedding_repo_id = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
embedding_model_dir = os.path.join(os.getenv("DATA_DIR", "data"), "models", embedding_repo_id)
tokenizer_repo_id = os.getenv("TOKENIZER_MODEL_NAME", "google-bert/bert-base-uncased")
tokenizer_model_dir = os.path.join(os.getenv("DATA_DIR", "data"), "models", tokenizer_repo_id)
DEBUG = os.getenv("DEBUG", "false").strip().lower() == "true"

# downloading embeddings model
snapshot_download(
    repo_id=embedding_repo_id,
    local_dir=embedding_model_dir,  # Ensure it's downloaded to /data/models
    token=token
)
# downloading chunking tokenizer model
snapshot_download(
    repo_id=tokenizer_repo_id,
    local_dir=tokenizer_model_dir,  # Ensure it's downloaded to /data/models
    token=token
)
