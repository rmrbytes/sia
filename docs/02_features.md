[Back to Documentation](/docs/README.md)

# Features: Current & Future

1. **Docker Containers**: This entire farm of servers are orchestrated via docker containers. In tandem with the configuration files administrators can use resources suiting their needs.

2. **Embedding models**: Sia gives flexibilty to adminstators to use any model that is suits their requirement. The embedding server in the current version supports any model of the **Sentence Tranformer** type. This is over 200 models. Check the list on [Huggingface](https://huggingface.co/models?sort=trending&search=sentence-transformers). 

3. **Inference platforms**: Currently supports the [vLLM](https://github.com/vllm-project/vllm). Work is currently in progress to add [TGI](https://github.com/huggingface/text-generation-inference), the Text Generation Inference by HuggingFace and [Ollama](https://ollama.com)

4. **Text Generation modes**: The only Text Generation mode that Sia currently supports is Chat or Conversational mode, where a user can have a conversation about a topic.

5. **Retrieval Augmented Generation**: Fundamentally, Sia is designed to create agents using RAG which is doucment based text generation. Sia makes the entire process of creating chunks from the document using embedding models and retrieving them to be shared with the inference server an easy task.

6. **Text-Gen parameters**: Currently, Sia is configured to accept text generation parameters like temperature, max-tokens etc set by the Admin. In subsequent versions we are enabling it at the user-level.

> We would like folks to use [issues on github](https://github.com/rmrbytes/sia/issues) to suggest new features.

[Back to Documentation](/docs/README.md)