[Back to Documentation](/docs/README.md)

# SIA CLI Installation

The SIA Command Line Interface (CLI) is a terminal-based tool used to administer SIA servers. Follow the steps below to install and configure the CLI on your server.

## Installation Steps

### 1. **Download the Latest CLI Release**

The SIA CLI tool is developed as a separate open-source project. To download the latest version, refer to the release documentation available here:

- [SIA CLI v0.1.0](https://github.com/rmrbytes/sia-cli/releases/tag/v0.1.0)

Follow the steps mentioned in the release notes to install the CLI on your server. Once installed, you can test the installation using the following command:

```bash
sia --help
```

> You can also install the CLI on a remote computer to manage the servers remotely.

### 2. **Set Up the CLI to Connect to the Servers**

To connect the CLI to the servers, two environment variables need to be set on the client machine: `SIA_SERVER_URL` and `SIA_API_KEY`.

1. **Initial Local Setup**: When setting up the server for the first time, you can only connect to it from the local terminal of the server itself. This is by design to ensure that the administrator who sets up the servers also sets up the admin password, providing an extra layer of security.

2. **Set Environment Variables**: Set the following environment variables on the server terminal:

   ```bash
   # Set the server URL (use localhost for initial local setup)
   export SIA_SERVER_URL=http://localhost

   # Set the API key (use the key from the .env file)
   export SIA_API_KEY=Your-Generated-API-Key
   ```

### 3. **Set the Admin Password**

To set the admin password, use the following command:

```bash
sia setpwd
```

At the prompt, enter a strong password. This step ensures that the server is secured and accessible only to authorized administrators.

> **Note**: Setting a strong password is crucial for the security of your SIA servers.

### 4. **Remote CLI Access**

After setting the admin password locally, you can set up the CLI on a remote computer to manage the servers. To do this, ensure that the `SIA_SERVER_URL` points to the server's public IP or domain name, and set the `SIA_API_KEY` accordingly.

For example:

```bash
export SIA_SERVER_URL=http://your-server-ip
export SIA_API_KEY=Your-Generated-API-Key
```

This allows you to manage SIA servers from any authorized remote machine, providing flexibility and ease of access.

[Back to Documentation](/docs/README.md)
