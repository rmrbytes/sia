[Back to Documentation](/docs/README.md)

# Servers Installation

Before we begin with the installation steps, let’s review some prerequisites to ensure everything is in place.

## Prerequisites

### **A. Docker**

SIA servers run as Docker containers. Ensure that both the Docker daemon and Docker Compose are installed, and that the admin user has permissions to run containers. Refer to the [Docker installation documentation](https://docs.docker.com/engine/install/) for setup, especially for configurations [for non-root users](https://docs.docker.com/engine/install/linux-postinstall/).

### **B. Hugging Face Token**

SIA downloads its embedding and inference models from Hugging Face, a popular collaborative platform for machine learning models. You’ll need a *Hugging Face token* set as an environment variable to access these models.

- Register on [Hugging Face](https://huggingface.co/join) if needed, and create an access token from your account settings.
- Note: Certain models, like Llama, may require additional permissions. Visit the model’s page on [Hugging Face](https://huggingface.co/models) to check for any extra requirements.

### **C. API Keys & Secrets**

SIA allows administrators to set API keys for secure server authorization:

1. **X_API_KEY**: Used to authorize all admin requests.
2. **SECRET_KEY**: Used to hash the admin password.

> **Tip:** See below for some easy ways to generate these keys.

### **D. GPU-Based Server**

GenAI models typically require GPU resources. We recommend using at least a single-GPU server, such as AWS’s `g5.xlarge` instance, for your initial SIA setup. Nvidia-powered instances with pre-installed drivers are ideal for GenAI applications.

> We’ll expand this list to include other cloud providers over time.

### **E. Suitable OS Image**

SIA servers need a Linux OS with Docker installed. For a quick start, consider an OS image with pre-installed Nvidia drivers and Docker setup, such as:

```
Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.4 (Ubuntu 22.04)
ami-0522957486f40f1e7 (64-bit (x86)) / ami-0a7d5ba31c9516a28 (64-bit (Arm))
```

This image includes the Nvidia drivers, relevant software, and Docker with necessary permissions, making it ready for immediate use.

> In the AWS console, search for "Nvidia" under *Application & OS images* to locate this AMI.

## Installation Steps

Follow these steps for a quick install:

1. **Set up the Server**: Start a compute instance as described above, with a minimum of 16GB memory and at least one GPU. Ensure SSH access is configured, along with port 80 for admin API requests and chat access.

2. **Connect to the Server Terminal**: Use CloudShell or a local terminal client to connect to the server.

3. **Download the Release Archive**: Either from the home directory or from any `projects` directory, download the release archive using:

   - **To download a zip file**:
   ```bash
   wget https://github.com/rmrbytes/sia/releases/download/v1.0.0/sia-v0.1.0.zip
   ```
   
   - **To download a tar.gz file**:
   ```bash
   wget https://github.com/rmrbytes/sia/releases/download/v1.0.0/sia-v0.1.0.tar.gz
   ```

4. **Extract the Archive**:

   - **If zip was downloaded**:
     ```bash
     unzip sia-v0.1.0.zip
     ```
   
   - **If tar.gz was downloaded**:
     ```bash
     tar -xzvf sia-v0.1.0.tar.gz
     ```

   > **Note:** `zip` or `tar` utilities must be installed on the server.

   - After extraction, you should see a directory structure like this:
     ```bash
     sia
      ├── .env-sample
      ├── data
      ├── docker-compose.yaml
      └── nginx.conf
     ```

5. **Set Permissions for the Data Directory**:

   Ensure the data directory has the correct permissions for Docker to access and store data.

   ```bash
   cd sia
   chmod -R 777 data
   ```

6. **Create the .env File**:

   The `.env` file is the main configuration file for SIA. Copy the provided `.env-sample` and customize it as needed:

   ```bash
   cp .env-sample .env
   ```

7. **Set the Hugging Face Token and X-API-Key**:

   Edit the `.env` file to add the Hugging Face token and X-API-Key. The Hugging Face token should be obtained as described in the prerequisites, while the X-API-Key can be generated using one of the methods below:

   ```bash
   # In the .env file, add:
   HUGGING_FACE_HUB_TOKEN=Your-Token-Here
   X_API_KEY=Your-Generated-API-Key
   ```

   > Other variables can be customized, but for a quick install, we recommend leaving the default settings unchanged.

   Some simple ways to create an API key include:

   - **Using OpenSSL**:
     ```bash
     openssl rand -base64 32
     ```

   - **Using uuidgen**:
     ```bash
     uuidgen
     ```

8. **Create the Containers**:

   With everything in place, run Docker Compose to set up the containers and download necessary binaries:

   ```bash
   docker compose -f docker-compose.yaml up -d
   ```

   The first time you are running the servers we recommend not using the `-d` detached mode flag so that the progress of the image loading is visible

   > This step should take less than 20 minutes to complete.

### Your SIA servers are now ready for use!

[Back to Documentation](/docs/README.md)

