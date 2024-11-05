[Back to Documentation](/docs/README.md)

# Understanding SIA

> SIA is a farm of interconnected servers that enables you to create and manage intelligent GenAI agents, each tailored to serve specific needs with dedicated data.

SIA lets you build multiple agents, each designed for a unique purpose, with its own data resources for enhanced customization and effectiveness.

![network_diagram](/docs/images/sia_network.svg)

## Server Components

1. **Proxy Server**: This server acts as the entry point for all requests from both the Command Line Interface (CLI) client and the web chat interface. It’s responsible for routing admin and customer queries securely. Administrators can configure HTTPS, CORS, and other security settings via a configuration file.

2. **API Server**: The API server manages the GenAI solution's core functionality. Through REST APIs accessible via the CLI, it enables setup and management of **agents**. It frames chat prompts into requests suitable for the inference server and coordinates with the embeddings and inference servers as needed.

3. **Embeddings Server**: This key component in the RAG (Retrieval-Augmented Generation) pipeline processes all private company data into retrievable tokens. It supports configuration for embedding models and several chunking strategies, allowing for tailored data handling based on the document types associated with each agent.

4. **Inference Server**: As the final stage in the GenAI pipeline, the inference server processes requests and generates responses using the selected Large Language Model (LLM). This server is performance-intensive and often requires one or more GPUs (Graphics Processing Units) to handle real-time query loads effectively.

5. **Model Downloader**: This Docker container ensures that any new model specified in the `.env` file is automatically downloaded and applied on the next server run. After the download, the container stops, ensuring efficient resource use.

## Host

All servers are deployed as **Docker containers** and share a common data folder, simplifying storage management and configuration. More details on Docker setup and shared data configuration are available in the documentation.

## Clients

1. **SIA-CLI**: This terminal-based CLI acts as the primary administrative interface for managing SIA servers, similar to *git* or *docker*. A separate section provides detailed guidance on using the CLI effectively.

2. **Web Interface for Chat**: SIA includes a web interface to enable end-users to interact with agents. **Note:** This web interface is designed to be embedded within *another web application*, rather than as a standalone product. Instructions for integration (via iframe) are provided elsewhere in the documentation.

## Nature of GenAI

GenAI solutions require careful alignment between inference models, embedding models, and chunking strategies. These elements must be tailored to your data and the intelligence each agent is designed to provide. SIA supports this need for experimentation by offering a highly configurable platform. Using just two tools—environment variables and Docker Compose commands—SIA administrators can efficiently set up and adjust servers to optimize performance and accuracy.

> **Did you know?** Setting up these servers for the first time takes less than 20 minutes!

[Back to Documentation](/docs/README.md)
