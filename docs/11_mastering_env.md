[Back to Documentation](/docs/README.md)

# Mastering `.env`

The `.env` file is central to configuring the SIA farm of servers. It provides flexibility by allowing administrators to customize different server settings to suit their needs. This page provides an overview of the key settings and how they impact SIA's functionality.

## General Settings

The following settings are commonly used by multiple servers in the SIA setup:

### 1.1. **Hugging Face Token**

```plaintext
HUGGING_FACE_HUB_TOKEN=Put-Your-HF-Token-here
```

This token is used to authenticate with Hugging Face to download models. Obtain your token from your account settings at [Hugging Face](https://huggingface.co).

### 1.2. **API Key (`X_API_KEY`)**

```plaintext
X_API_KEY=Put-Your-API-Key-here
```

This key authorizes admin access through the CLI. To generate an API key, refer to the [Servers Installation](03_servers_installation.md) page for simple command suggestions.

### 1.3. **Debug Mode**

```plaintext
DEBUG=false
```

Set this to `true` to enable detailed logs on the server console and CLI. This is useful for troubleshooting issues.

### 1.4. **Data Directory**

```plaintext
DATA_DIR=data
```

The data directory is where all SIA-related data is stored, including the database, agent documents, embeddings store, and models. Ensure that appropriate permissions (`chmod -R 777`) are applied to this directory since it will be accessed and updated by the servers.

### 1.5. **HTTPS**

```plaintext
USE_HTTPS=false
```

Set this to `true` if HTTPS is enabled for the SIA servers to ensure secure communication.

## API Server Settings

These settings are used to configure the API server:

### 2.1. **Number of Workers**

```plaintext
API_NO_WORKERS=1
```

Adjust this value based on server load and available resources.

### 2.2. **Secret Key**

```plaintext
SECRET_KEY=Your-secret-key
```

The secret key is used for generating authentication tokens for admin access.

### 2.3. **Access Token Expiry**

```plaintext
ACCESS_TOKEN_EXPIRY_IN_HOURS=24
```

Set the number of hours for which the admin access token will be valid. After expiry, the user will need to log in again.

### 2.4. **Embeddings Server Name**

```plaintext
EMBEDDINGS_SERVER=embeddings-server
```

This is the service name of the embeddings server. You can customize it if the service name in the Docker Compose file changes.

### 2.5. **Embeddings Server Port**

```plaintext
EMBEDDINGS_SERVER_PORT=8002
```

This is the port number of the embeddings server. Change it only if the server port in the Docker Compose file is modified.

### 2.6. **Inference Server Name**

```plaintext
INFERENCE_SERVER=inference-server
```

This is the service name of the inference server. You can modify it if the service name in the Docker Compose file changes.

### 2.7. **Inference Server Port**

```plaintext
INFERENCE_SERVER_PORT=8000
```

This is the port number of the inference server. Update it only if the server port in the Docker Compose file changes.

## Embeddings Server Settings

The following settings are used by the embeddings server:

### 3.1. **Number of Workers**

```plaintext
EMBEDDINGS_NO_WORKERS=1
```

Adjust this value based on server load and available resources.

### 3.2. **Embeddings Model Name**

```plaintext
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

You can select any [sentence-transformer model](https://huggingface.co/models?sort=trending&search=sentence-transformers) from Hugging Face that suits your requirements. If left blank, the default model (`all-MiniLM-L6-v2`) will be used.

### 3.3. **Splitting Strategy**

```plaintext
SPLIT_BY=sentence
```

The default split strategy for chunking documents. Options include `sentence`, `page`, `word`, or `passage`. We recommend specifying the strategy for each document during agent creation.

### 3.4. **Splitting Length**

```plaintext
SPLIT_LENGTH=5
```

The number of items (e.g., sentences, words) in each chunk. For example, if `split_by` is set to `sentence` and `split_length` is `5`, each chunk will consist of 5 sentences.

### 3.5. **Split Overlap**

```plaintext
SPLIT_OVERLAP=2
```

The number of items to overlap between chunks, which helps maintain context. For example, if set to `2`, the last two items of a chunk will be repeated in the next chunk.

### 3.6. **Split Threshold**

```plaintext
SPLIT_THRESHOLD=5
```

The minimum number of items required for a chunk. If the content is insufficient, it will be added to the previous chunk.

### 3.7. **Distance Metric**

```plaintext
DISTANCE_METRIC=cosine
```

The distance metric used to determine the relevance of a chunk based on a user prompt. Acceptable options are `cosine` (default), `ip` (inner product), or `l2` (squared L2).

### 3.8. **Number of Results**

```plaintext
TOP_N=3
```

The number of relevant chunks that the embeddings server must retrieve based on a user prompt.

### 3.9. **API Server Name**

```plaintext
API_SERVER=api-server
```

This is the service name of the API server. You can customize it if the service name in the Docker Compose file changes.

### 3.10. **API Server Port**

```plaintext
API_SERVER_PORT=8080
```

This is the port number of the API server. Change it only if the server port in the Docker Compose file is modified.

## Inference Server Settings

The inference server settings are based on the type of inference platform used. Currently, SIA supports vLLM, and the following settings can be configured via environment variables. Refer to the complete set of [vLLM Docker environment variables](https://docs.vllm.ai/en/v0.5.5/serving/env_vars.html) for more information.

### 4.1 **Target Device**

```plaintext
VLLM_TARGET_DEVICE=CUDA
```

Specify the device type. Supported are: rocm, neuron, cpu, openvino

### 4.2. **LLM Model Name**

```plaintext
LLM_MODEL_NAME=meta-llama/Llama-3.2-1B-Instruct
```

Specify the LLM model to run on the inference server. You can choose any open-source model available on Hugging Face.

### 4.3. **Model Data Type (`DTYPE`)**

```plaintext
DTYPE=float16
```

Specify the data type for the model weights. Options are `auto`, `float16`, or `float32` (default). Using `float16` can reduce memory usage.

### 4.4. **GPU Memory Fraction**

```plaintext
VLLM_GPU_MEMORY_FRACTION=0.9
```

Set a value between `0` and `1` to determine the fraction of GPU memory used by the model. A higher value allows for better performance.

### 4.5. **Number of GPU Layers**

```plaintext
VLLM_NUM_GPU_LAYERS=40
```

Specify the number of transformer layers to keep on the GPU (when offloading to the CPU is enabled). Increase the value to keep more layers in GPU memory for better performance.

### 4.6. **CPU Offloading**

```plaintext
VLLM_OFFLOAD_CPU=true
```

Enable offloading of model layers to the CPU if GPU memory is insufficient. This is useful for large models that may not fully fit in GPU memory.

### 4.7. **Maximum Sequence Length**

```plaintext
VLLM_MAX_SEQ_LENGTH=4096
```

Specify the maximum sequence length in tokens. Set this based on the model's capabilities and requirements.

### 4.8. **OpenAPI Key**

```plaintext
OPENAPI_KEY=None
```

Although SIA uses locally loaded models, an OpenAPI key may be required for future use if integrating with OpenAI's models.

## Chat Settings

These settings are only used for the purposes of Chat. In later versions these value can be set differently for an agent and also can be overriden by a user. Currently, these values are applicable for all agents.

### 5.1 **Chat Response Length**

```plaintext
CHAT_RESPONSE_LENGTH=M
```

This is to set the length of the response from the Inference server. Supported values are: S, M, L for Short, Medium and Long. These are a convenience for the end-user (not currently supported) to specify the length of response.

### 5.2 **Chat Response Length - Short**

```plaintext
CHAT_RESPONSE_LENGTH_SHORT=50
```

This sets the max number of tokens of a short response. Useful if you want the Inference server to provide pointed answer.

### 5.3 **Chat Response Length - Medium**

```plaintext
CHAT_RESPONSE_LENGTH_MEDIUM=150
```

This sets the max number of tokens of a medium response.

### 5.4 **Chat Response Length - Long**

```plaintext
CHAT_RESPONSE_LENGTH_LONG=300
```

This sets the max number of tokens of a long response.

### 5.5 **Chat Temperature**

```plaintext
CHAT_TEMPERATURE=0.7
```

Sets the temperature of the response. The range is 0 (deterministic) to 1.0 (more creative). 

### 5.6 **Chat Top P Sampling Parameter**

```plaintext
CHAT_TOP_P=0.9
```

Sets the Sampling Parameter of the response. Range is 0 to 1. A higher value will allow more randomness


### 5.7 **Chat Frequency Penalty**

```plaintext
CHAT_FREQUENCY_PENALTY=0
```

Sets the Frequency Penalty of the response. Range is 0 to 2. Higher the value, reduces likelihood of repetitive words.

### 5.8 **Chat Presence Penalty**

```plaintext
CHAT_PRESENCE_PENALTY=0
```

Sets the Presence Penalty of the response. Range is 0 to 2. Higher the value, increases the likelihood of new concepts.


[Back to Documentation](/docs/README.md)

