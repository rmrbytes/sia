[Back to Documentation](/docs/README.md)

# Understanding Sia

> Sia is a farm of interconnected servers and connected clients that gives the ability to build your own GenAI agents using your own data serving your own customers.

Sia is designed to help you build multiple agents each for a specific need and fed with its own related data.

![network_diagram](/docs/images/sia_network.png)

## Server Components

1. **Proxy Server**: This server is the proxy server that handles all requests that come from the Command Line Interface (CLI) client for admin purposes as well as the web chat interface that is integrated with your application serving your customers. Administrations in your set up will have the ability to set up https, cors and other security requirements via the conf file available.

2. **API Server**: The API server is what controls the access to the genAI solution put in place. REST APIs are available via the CLI to set up your **agents**. Its main job is to accept the chat user's prompt and frame it in the form of a proper request for the inference server. The APIs access the needs of the embeddings server and inference servers when required. 

3. **Embeddings Server**: This critical component of the RAG (*Retrieval Augmented Generation*) pipeline takes the full load of pre-processing all the private data of the company and make it available in a form (tokens) that can be queried for retrieval purposes. The configuration allows choosing an embedding model of your choice and picking one of the popular chunking strategies based on the nature of the documents you submit for an agent.

4. **Inference Server**: The last server of the genAI server farm processes the request submitted and gets a response. The choice of the LLM (Large Language Model) is based on your requirement. This server is a heavy-duty one usually requiring one or more GPUs (Graphical Processing Units) to aid performance of requests.

## Host

All the above servers are served via **Docker containers** with a data folder serving to share data amongst the servers. More details are provided elsewhere in this documentation.

## Clients

1. **SIA-CLI**: A terminal-based CLI is the admin interface to access and control the SIA set of servers. Similar to *git* and *docker*. A separate section of the documentation provides help on the use of the cli.

2. **Web interface for chat**: Sia provides a simple web interface for the end users to chat with the agents. **By design**, this web interface is to be integrated within *another web application* and not provide it as-is to the end-user. The method of such an integration (via iframe) is described elsewhere in this documentation.

## Philosophy

The nature of GenAI solutions indicates a **match** of appropriate inference models with effective embedding models based on correct choice of chunking strategies which is a function of your document content and the type of agent intelligence required. All of the above calls for a certain amount of experimentation.

Sia serves that need by making the task of such experimentation a bit easier. Hence, by design, Sia is a highly configurable platform in the hands of the administrator relying on two simple tools. Environment variables and Docker compose commands. Simple yet effective.

> A data point. Setting up these servers the first time takes less than 20 minutes!

[Back to Documentation](/docs/README.md)