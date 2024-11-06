[Back to Documentation](/docs/README.md)

# SIA CLI Installation

The SIA Command Line Interface (CLI) is a terminal-based tool used to administer SIA servers. The tool is developed as a separate open-source project. To download the latest version, refer to the [release notes]((https://github.com/rmrbytes/sia-cli/releases/tag/v0.1.1).


## List of Binaries available

The following are the available binaries of the CLI. Download the appropriate one for your access platform:

- **Linux**:
  - [Linux (x86_64)](https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-linux)
  - [Linux (ARM)](https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-linux-arm)
  - [Linux (ARMv7)](https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-linux-armv7)
- **macOS**:
  - [macOS (Intel)](https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-mac-intel)
  - [macOS (ARM)](https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-mac-arm)
- **Windows**:
  - [Windows (x86_64)](https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-windows.exe)

## Installation Steps

**Step 1: Download the appropriate Binary**

You may download the appropriate Binary by clicking on the above link or using `wget` from the terminal.

- `wget https://github.com/rmrbytes/sia-cli/releases/download/v0.1.1/sia-linux` (change the name accordingly)

**Step 2: Install the CLI**
- **Linux**:
  1. Make the binary executable:
     ```bash
     chmod +x sia-linux  # or sia-linux-arm/sia-linux-armv7 based on your download
     ```
  2. Move it to `/usr/local/bin` and rename it to **"sia"** for easy access:
     ```bash
     sudo mv sia-linux /usr/local/bin/sia
     ```
  3. Verify the installation:
     ```bash
     sia --help
     ```
- **macOS**:
  1. Make the binary executable:
     ```bash
     chmod +x sia-mac-arm  # or sia-mac-intel based on your download
     ```
  2. Move it to `/usr/local/bin` and rename it to "sia" for easy access:
     ```bash
     sudo mv sia-mac-arm /usr/local/bin/sia
     ```
  3. If you receive a message saying "sia can't be opened because Apple cannot check it for malicious software", follow these steps:
     - Open `System Preferences` > `Security & Privacy`.
     -  You will see a message about "sia" being blocked. Click `Open Anyway`.
     - Run the `sia` command again, and confirm by clicking `Open` in the pop-up.
  4. Verify the installation:
     ```bash
     sia --help
     ```
- **Windows**:
  1. Rename the downloaded file to `sia.exe` and move it to a directory included in your PATH.
  2. Verify the installation by opening a command prompt and running:
     ```cmd
     sia --help
     ```

> You can also install the CLI on a [remote computer](06_set_remote_cli.md) to manage the servers remotely. 

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

[Back to Documentation](/docs/README.md)
