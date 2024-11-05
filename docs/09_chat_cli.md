[Back to Documentation](/docs/README.md)

# Chat from CLI

The SIA Admin CLI provides administrators with the ability to test agents directly from the command line. This feature is useful for verifying the agent's responses and evaluating the overall performance of the SIA system. By using the CLI to chat with agents, administrators can tweak configurations, adjust system settings, and determine if server resources (e.g., number of GPUs, RAM) are sufficient for optimal performance.

## Starting a Chat Session

To start a chat session with a specific agent, use the following command:

```bash
sia agent chat --name=insurance-specialist
```

Or, you can use the shorthand version:

```bash
sia agent chat -n=insurance-specialist
```

This command initiates an interactive chat session, allowing you to send queries to the agent and receive responses in real-time.

### Chatting with the Agent

1. After starting the chat session, you can type any query to interact with the agent. The agent will provide responses based on the data and instructions it has been configured with.

2. To exit the chat mode and return to the terminal prompt, simply type:

   ```bash
   q
   ```

This will terminate the chat session and bring you back to the regular terminal.

> **Tip**: The CLI chat feature is particularly useful for testing new agent configurations before deploying them to end users, ensuring that the agent behaves as expected.

[Back to Documentation](/docs/README.md)

