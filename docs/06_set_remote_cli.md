[Back to Documentation](/docs/README.md)

# Set Remote CLI Access

The SIA Command Line Interface (CLI) can be installed on a remote computer to manage SIA servers from anywhere. This provides flexibility for administrators to perform management tasks without being physically present at the server.

## Steps to Set Up Remote CLI Access

### 1. **Open Port 80 on the Server**

Ensure that port 80 was kept open during the server installation step. This is required to allow remote access to the SIA servers.

### 2. **Install the CLI on the Remote Computer**

Follow the instructions in [Admin CLI Installation](04_cli_installation.md) to download and install the CLI on your remote machine. Move the CLI to the user home directory or set the system path to access it easily from any terminal session.

Once installed, test that the CLI was correctly installed by running:

```bash
sia --help
```

### 3. **Set Environment Variables for Remote Access**

Unlike the server setup, where `SIA_SERVER_URL` was set to `http://localhost`, on a remote computer you need to use the server's IP address or domain name. Set the following environment variables:

```bash
export SIA_SERVER_URL=http://<server-ip-address>
export SIA_API_KEY=Your-Generated-API-Key
```

Replace `<server-ip-address>` with the actual IP address or domain name of your server and `Your-Generated-API-Key` with the API key set in the `.env` file.

### 4. **Log In to SIA Servers**

After setting the environment variables, use the following command to log in to the SIA servers:

```bash
sia login
```

You will be prompted to enter the admin password:

```bash
$ sia login                                
Enter admin password:
```

Once logged in, you can administer your SIA servers from the remote computer just as you would locally.

> **Note**: Always ensure that remote access is configured securely to prevent unauthorized access to your SIA servers.

[Back to Documentation](/docs/README.md)

