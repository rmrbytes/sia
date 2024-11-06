[Back to Documentation](/docs/README.md)

# Sample Agent

The Sample agent below is a **Product Specialist** of Air Conditioners of a fictitious company.

## Content for RAG

The following four files can be downloaded into the directory from where you are running the `sia-cli`.

1. [Brochure.pdf](/docs/files/Brochure.pdf)
2. [TechNotes.md] (/docs/files/TechNotes.md)
3. [InstallationGuide.md](/docs/files/InstallationGuide.md)
4. [FAQ.txt](/docs/files/FAQ.txt)

## Building your Agent

**Step 1**: Set up Sia servers 

Set up your Sia servers as detailed in [3. Servers' Installation](03_servers_installation.md) including setting up of the admin password.

**Step 2**: Set admin password on server

Set up CLI as detailed in [4. Server CLI Installation](04_cli_installation.md)

**Step 3**: Set CLI on remote machine 

Set up remote CLI on your local machine as detailed in [6. Set Remote CLI](06_set_remote_cli.md)

[Back to Documentation](/docs/README.md)

**Step 4**: Download template for new agent

Download the template for a new agent from your remote machine using the command:

`sia agent create`

This will create a `create_agent.yaml` file. 

**Step 5**: Edit template

Edit it as below:
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
new_files:
    - filepath: "Brochure.pdf"
      meta:
        split_by: passage
        split_length: 1
        split_overlap: 0
        split_threshold: 0
    - filepath: "TechNotes.md"
      meta:
        split_by: sentence
        split_length: 5
        split_overlap: 1
        split_threshold: 2
    - filepath: "InstallationGuide.md"
      meta:
        split_by: sentence
        split_length: 5
        split_overlap: 1
        split_threshold: 2
    - filepath: "FAQ.txt"
      meta:
        split_by: sentence
        split_length: 2
        split_overlap: 0
        split_threshold: 0
```

This assumes that the 4 files downloaded are in the current working directory. If not please change the path accordingly.

**Step 6**: Push template to create agent

1. Before pushing the template rename the `create_agent.yaml` to `product-specialist.yaml`. This is not required but recommended to avoid confusion.
2. Type `sia agent --name=product-specialist --file=product-specialist.yaml --action=create`
3. This should create the agent

**Step 7**: Check list of agents

Type `sia agent ls` to display list of agents. The just created agent should show up. Confirm that the E-Status (Embedding Status) is blank and not "I". If it shows "I", wait for a couple of minutes and give the command again. The embeddings for the 4 documents should take only a few seconds.

**Step 8**: Call the Chat interface

1. Type `sia agent chat -n=product-specialist`. 
2. This will ask for a user prompt. 
3. You may begin with one of the suggested prompts. And then proceed with other relevant prompts.
4. To exit the chat interface, type `q`.

