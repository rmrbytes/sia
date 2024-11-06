[Back to Documentation](/docs/README.md)

# Features: Current & Future

1. **Docker Containers**: SIA’s entire server farm is orchestrated via Docker containers, offering flexible deployment options. Administrators can adjust resource allocation to fit their environment and scale up as needed. Configuration files make it easy to modify and manage server settings.

2. **Flexible Embedding Models**: SIA empowers administrators to select the embedding model that best fits their needs. The embedding server in the current version supports any **Sentence Transformer** model, giving access to over 200 models. Explore the full list on [Hugging Face](https://huggingface.co/models?sort=trending&search=sentence-transformers) to find the model that suits your data and requirements.

3. **Inference Platforms**: SIA currently supports the [vLLM](https://github.com/vllm-project/vllm) platform, optimized for efficient, high-speed language generation. Future support is planned for [TGI](https://github.com/huggingface/text-generation-inference) (Text Generation Inference) by Hugging Face and [Ollama](https://ollama.com), enabling even broader compatibility with open-source LLMs.

4. **Text Generation Modes**: Currently, SIA supports a Chat or Conversational mode, allowing users to engage in a continuous conversation on topics configured per agent. Future releases may introduce additional modes based on community feedback.

5. **Retrieval-Augmented Generation (RAG)**: SIA is purpose-built for document-based text generation using RAG. The platform streamlines the process of chunking documents with embedding models, managing retrieval, and integrating with inference servers. This architecture simplifies the creation of intelligent agents powered by RAG.

6. **Text Generation Parameters**: SIA allows administrators to configure generation parameters—such as temperature, max tokens, and top-p—via environment variables. These control the style and depth of generated responses. In upcoming versions, we plan to support user-level customization, allowing end-users to adjust parameters dynamically.

7. **Web inteface for chat**: SIA provides a web interface for making the agent chat available to your end-users. By design, this chat interface is to be part of another hosted web application (using `iframe`) where the access to the agents may be controlled. 

8. **Extensibility for New Features**: SIA is designed to be modular, and the development roadmap includes enhancing customization options, adding more inference models, and expanding user-level configuration.

> **We welcome your input!** Use the [issues section on GitHub](https://github.com/rmrbytes/sia/issues) to suggest features, provide feedback, and help shape SIA’s future.

[Back to Documentation](/docs/README.md)
