[Back to Documentation](/docs/README.md)

# Create an Agent

Agents in SIA are configured using a YAML file, which makes it easy to define the properties and behaviors of each agent. This section will guide you through understanding the structure of the YAML file and using it to create a new agent.

## Understanding the Agent YAML Structure

The SIA CLI uses a YAML format to specify an agent's configuration. Below is an example of an agent YAML file:

```yaml
name: agent-name # A meaningful name with letters, digits, hyphen, underscore, no spaces
instructions: |
  This is a sample instruction for the agent. It can be multiline.
  
  Edit it accordingly.
welcome_message: Welcome to the Agent!
suggested_prompts: # A maximum of 3 prompts can be provided
  - What can you do?
  - How do I use this agent?
  - Tell me something interesting.
new_files:
  - filepath: "~/docs/document1.pdf" # Absolute path
    meta:
      split_by: "sentence"
      split_length: 4
      split_overlap: 1
      split_threshold: 0
  - filepath: "../files/file1.txt" # Relative path to the current working directory
    meta:
      split_by: "word"
      split_length: 200 # Defaults will be used for missing meta values
```

## Understanding the YAML Elements

1. **Agent Name**: This can be set only when **creating** a new agent. It must be short, meaningful, and consist of letters, digits, hyphens (`-`), and underscores (`_`). Spaces are not permitted.

   > **Examples**: `product-specialist`, `insurance_expert`

2. **Instructions**: This is one of the most important elements of the agent configuration. These instructions are sent to the inference model (LLM) with **every request** and define how the agent should handle customer queries. Instructions can be multiline and should be as detailed as needed to ensure the agent behaves as intended.

   **Example**:
   ```
   You are a technical expert on ACs. Use the documents provided to you, which contain all the specs, FAQs, and other technical information, to answer queries. If you do not understand the query or lack the knowledge, please respond with "I do not know about this topic."

   Keep your answers brief and to the point. If there are multiple possible answers, feel free to ask clarifying questions.
   ```

3. **Welcome Message**: This is a short introductory message that will be displayed to users when they start interacting with the agent. Keep it concise and welcoming.

   **Example**:
   ```
   Hi, I am your insurance policy expert and am ready to answer any queries you have.
   ```

4. **Suggested Prompts**: Suggested prompts help guide users in asking relevant questions. SIA supports up to 3 suggested prompts, which will be displayed on the chat interface.

   **Example**:
   ```
   What is covered in the warranty of AC-2357?
   ```

5. **New Files**: This section lists the documents that the agent will use to generate responses. There is no limit to the number of files that can be added, but each file requires some metadata for effective processing:

   - **File Path**: The path to the file on your local computer. This can be an absolute path (`~/docs/document1.pdf`) or a relative path (`../files/file1.txt`). Currently supported file types include **txt**, **pdf**, and **md**.

   - **Meta Data**: Each file must include metadata to guide the embedding process. The metadata consists of:
     - `split_by`: The chunking strategy to use for embedding. Options are `sentence`, `page`, `word`, or `passage`.
     - `split_length`: The number of items in each chunk. For example, `split_length: 10` with `split_by: sentence` means each chunk will contain 10 sentences.
     - `split_overlap`: The number of items that overlap across chunks, helping to maintain context. For instance, a value of 2 means two sentences will be repeated between chunks.
     - `split_threshold`: The minimum number of items needed in a chunk. If a chunk is too small, its content will be merged with the previous chunk.

> **Note**: Default values for metadata can be set in the `.env` file. If any metadata is missing from the YAML, the system will use these defaults.

## Using the CLI Command

### 1. **Download an Agent Template**

To create a new agent, start by downloading a YAML template using the following command:

```bash
sia agent create
```

This command will download a sample YAML template into the current directory, which you can customize to define your specific agent.

### 2. **Edit the Template**

Use any text editor to modify the template. It is good practice to rename the YAML file to reflect the agent's name, such as `insurance-specialist.yaml`.

### 3. **Push the YAML to the Server**

Once you've edited the YAML file, push it to the server to create the agent:

```bash
sia agent push \
  --name=insurance-specialist \
  --file=insurance-specialist.yaml \
  --action=create
```

This command tells SIA to push the specified file and create an agent with the given name.

If successful, you will see a response in your terminal with details of the saved agent. Note that the YAML file used to create the agent will be **deleted** from your directory to prevent unintended updates or misuse.

> **Single Source of Truth**: SIA uses the concept of a single source of truth for agents. The saved agent configuration will be based on the validated YAML file, with any invalid or extra elements being ignored. For example, if more than 3 prompts are provided, only the first three will be accepted.

> **Important**: When you push a new agent or update an existing agent, SIA servers will begin the embedding process in the background. Depending on the number and size of the documents, this may take a few minutes. You can check the status by viewing the agent as described in the next section.

[Back to Documentation](/docs/README.md)

