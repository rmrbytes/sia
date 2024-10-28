[Back to Documentation](/docs/README.md)

# Sia CLI installation

The Sia Command Line Interface is a terminal based tool to administer sia servers.

## Steps
The following are the steps to install it on your server:

### 1. **Download the latest CLI Release**: 
   
   The CLI tool has been developed as a separate open-source project. The steps to download are provided in the Release documentation available at:

   [Sia-cli v0.1.0](https://github.com/rmrbytes/sia-cli/releases/tag/v0.1.0)

   Kindly go throught the steps mentioned and install them on your server. 

   Test the sia using `sia --help`

   > You may later also install them on your remote computer to access administer the server.

### 2. **Setting up the CLI to connect to the Servers**:

    2.1 For the CLI to connect to the servers, two environment variables have to be set up from the client machine. They are: `SIA_SERVER_URL` and `SIA_API_KEY`. 
    
    2.2 When the server is set up for the first time, you can **only connect** to it from the local terminal of the server and not from a **remote client**. 
    
    2.3 This is by design to setup the admin password. This is a security measure to ensure that the adminstrator who set up the servers also sets up the admin pasword.

    2.4 Set the environment variables as shown below:
    ```bash
    # this will be as given below because you are accessing
    # the server from the terminal client of the host
    export SIA_SERVER_URL=http://localhost

    # enter the API key that you put in the .env file
    export SIA_API_KEY=
    ```

### 3. **Setting of the Admin password**:

    Using the CLI type: `sia setpwd`. At the prompt provide a strong password.



[Back to Documentation](/docs/README.md)