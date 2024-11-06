[Back to Documentation](/docs/README.md)

# Managing Agents

This section provides information on how to manage agents in SIA, including listing agents, viewing agent details, pulling agent configurations, updating agents, and deleting them.

## Listing Agents

To get a list of all agents currently configured in SIA, use the following command:

```bash
sia agent list
```

Alternatively, you can use the shorthand command:

```bash
sia agent ls
```

The command will return a list of agents with basic details, as shown below.

```bash
SRNO  NAME                 # FILES  E STATUS  CREATED ON UPDATED ON
-------------------------------------------------------------------
1     llm-expert           1                  12-Oct-24  13-Oct-24 
2     product-specialist   4                  11-Nov-24  11-Nov-24 
```

> The E Status is the Embedding Status. It shows a value of I (In process) when the embeddings are being generated in the background

## Viewing an Agent

To view the current configuration of a specific agent, use the following command:

```bash
sia agent --name=product-specialist
```

Or, you can use the shorthand version:

```bash
sia agent -n=product-specialist
```

This will display the agent's configuration in a YAML format, providing all details, including the welcome message, instructions, and associated files.
```yaml
name: product-specialist
welcome_message: Hi! I am the Product Manager of ACs in Aerocool Innovations.
instructions: |
    You are an expert on the entire AC product range of Aerocool Innovations. You have access to;
    - the product specifications
    - the installation guides
    - the FAQs
    - and the company profile

    Answer any queries related to the range of ACs. In case you are not aware of the answer gently decline to answer.
suggested_prompts:
    - When was Aerocool founded?
    - When do I need to change the filter in the AC?
    - What is the range of cooling capacities in the different products.
files:
    - filename: Brochure.pdf
      meta:
        split_by: passage
        split_length: 1
        split_overlap: 0
        split_threshold: 0
    - filename: TechNotes.md
      meta:
        split_by: sentence
        split_length: 5
        split_overlap: 1
        split_threshold: 2
    - filename: InstallationGuide.md
      meta:
        split_by: sentence
        split_length: 5
        split_overlap: 1
        split_threshold: 2
    - filename: FAQ.txt
      meta:
        split_by: sentence
        split_length: 2
        split_overlap: 0
        split_threshold: 0
createdon: 11-Nov-24
updatedon: 11-Nov-24
```

## Pulling an Agent Configuration as YAML

To download the current configuration of an agent as a YAML file, use the following command:

```bash
sia agent pull -n=insurance-specialist
```

This command will download the agent's configuration as a YAML file in your current directory. It is recommended to **pull** the agent's configuration before making any updates. Below is an example of a downloaded YAML file:

```yaml
# YAML format of agent
name: insurance-specialist # Do not change this
welcome_message: Hi there, I am an expert on insurance matters # This should be short and specific
instructions: |
  You are an expert on insurance policies. The policy document has been provided to you. Use the content provided to answer any queries.
# A maximum of 3 prompts are supported
suggested_prompts:
  - What is the max cover for a person over 60 years old?
  - What is the process for filing a nomination?
# Uncomment the file you wish to delete
deleted_files:
  # - rules.pdf
# Add new files, if any, giving full path
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

## Pushing an Agent Update

The YAML file downloaded using the **pull** command can be edited to make updates to the agent's configuration. Existing uploaded files will be listed under the `deleted_files` section, allowing you to remove them by uncommenting the relevant lines. You can also add new files in the `new_files` section.

Once the updates are made, push the changes using the following command:

```bash
sia agent push \
  --name=insurance-specialist \
  --file=insurance-specialist.yaml \
  --action=update
```

This command instructs SIA to update the specified agent with the new configuration.

> **Important**: When updating an agent, ensure that all changes are correctly specified in the YAML file. Any incorrect file paths or unsupported configurations will be ignored during the update process.

## Deleting an Agent

To delete an agent, use the following command:

```bash
sia agent delete -n=insurance-specialist
```

The system will ask for confirmation before proceeding with the deletion to prevent accidental data loss.

> **Note**: Deleting an agent is permanent, and all associated data will be removed. Ensure you have a backup or are certain before confirming the deletion.

[Back to Documentation](/docs/README.md)

