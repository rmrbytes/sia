[Back to Documentation](/docs/README.md)

# Servers Installation

Before we begin let us examine some pre-requisites.

## Prerequisites

**A. Hugging Face token**: Popularly most data scientists and engineering folks in ML and AI use HuggingFace as the source of all open-source models. It made sense for us to follow this established practice. 

> [Hugging Face](https://huggingface.co) is a collaborative platform for building, training, and deploying machine learning (ML) models

Consequently, the install procedure requires setting up of the *Hugging Face Token* as an environment variable. This is used by both the Embeddings Server and Inference Server to download the desired models. To obtain the token, you need to [register](https://huggingface.co/join) and create an access token from settings.

> Some of the models like Llama require you to additional seek their permission to use the model. It is recommended that you go to the desired model from their [models page](https://huggingface.co/models) and check if any additional permissions are required.

**B. GPU based server**: Gen AI usually requires a GPU-based server. Often multiple GPUs. We recommend that if you are installing Sia servers for the first time, you pick at least a single-GPU server. Perhaps a `g5.xlarge` EC2 instance from the AWS stack. The reason is that these Nvidia servers with GPU and drivers make is ready-made for GenAI needs.

> Over time we will add similar compute platforms from other cloud providers.

**C. Appropriate OS image**: At its core, Sia servers need a Linux OS with Docker. However, some OS images are "ready" to use with no configuration and set up required to use the hardware and run docker containers. For a quick install we recommend using:

```
Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.4 (Ubuntu 22.04)
ami-0522957486f40f1e7 (64-bit (x86)) / ami-0a7d5ba31c9516a28 (64-bit (Arm))
```

The advantage is that this has the Nvidia drivers, relevant software pre-loaded including docker with the appropriate rights set for the user. In short, *good to go*.

> In AWS console, you can type "Nvidia" in the *Application & OS image* choice to get a list from which you can pick the above

## Steps
The following are the steps for a quick install:

1. **Setup the server**: Instantiate a compute server as defined above. Ensure it has adequate memory (min 16GB) and at least 1 GPU. Ensure that the OS image has the min set of drivers and docker pre-installed (e.g. the above image has everything in place).

2. **Connect to server terminal**: Use either the CloudShell or the local terminal client to connect to the server.

3. **Download the release archive**: Either from the home directory or from any other `projects` directory, download the release archive using:
   
   3.1 **to download a zip:**
    ```bash
    wget https://github.com/rmrbytes/sia/releases/download/v1.0.0/sia-v0.1.0.zip
    ```
   
   3.2 **to download tar.gz:**
    ```bash
    wget https://github.com/rmrbytes/sia/releases/download/v1.0.0/sia-v0.1.0.tar.gz
    ```

4. **Extracting the archive**: 
   
   4.1 **if zip was downloaded:**
    ```bash
    unzip sia-v0.1.0.zip
    ```
   
   4.2 **if tar.gz was downloaded:**
    ```bash
    tar -xzvf sia-v0.1.0.tar.gz
    ```
    ⚠️ Prerequisite
    `zip` or `tar` must be installed on the server.

   4.3 This will create the following directory 
   ```bash
   sia
    ├── .env-sample
    ├── data
    ├── docker-compose.yaml
    └── nginx.conf
   ```

5. **Setting rights to Data directory**:
    
    The data directory rights need to be set right for the docker containers to access them and store data.
    ```bash
    # move to sia directory
    cd sia
    # set rights to data directory
    chmod -R 777 data
    ```
    
6. **Create the .env file**:

    The `.env` is the most important configuration file to customize Sia for your needs. A sample has been provided. Make a copy of it and edit as required.
    ```bash
    cp .env-sample .env
    ```

7. **Set Hugging Face token and X-API-Key**:
    
    The Hugging Face token and X-API-Keys are two important environment variables that need to be set before we proceed with the installation. The Hugging Face token, as explained above is provided by the HF site. The X-API key is what you need to generate. This has to be used by the CLI to access the servers as well as the web-application that access the web-server from the sia server farm. Some easy methods of creating API keys are suggested below. However, you may choose any key you wish.
    
    Edit the copied .env file using any editor (nano/vi) and add your HF token obtained as a prerequisite. You need to set 
    ```
    ...
    # Hugging Face token
    HUGGING_FACE_HUB_TOKEN=Put-Your-Token-Here
    ...
    # x-api key
    X_API_KEY=Create-Your-API-Key
    ...
    ```

    > Other environment variables can be changed. However, this being the quick install section, we recommend keep all other settings as-is.

    Some simple ways to create an API key are:

    7.1 **Using OpenSSL**:

    ```bash
    openssl rand -base64 32
    ```

    7.2 **Using uuidgen**:
    ```bash
    uuidgen
    ```

8 **Create the Containers**:

    Now, with everything in place, this is the last step to create the containers and download the binaries.
    ```bash
    docker compose -f docker-compose-yaml up`
    ```

    > The above command should take under 20 minutes to download and extract the binaries.

### Your Sia servers are ready for use!


[Back to Documentation](/docs/README.md)