[Back to Documentation](/docs/README.md)

# Set Admin Password

To secure your SIA server, you need to set an admin password. This process can only be performed locally on the server for security purposes.

## Steps to Set the Admin Password

### 1. **Use the CLI to Set the Password**

This task must be performed from the server terminal. Type the following command to initiate the password setup:

```bash
sia setpwd
```

The system will prompt you to enter a password and then repeat it for confirmation. Make sure to set a strong password (minimum of 6 characters):

```bash
$ sia setpwd                                 
Enter a strong password (min 6 chars):
Repeat above password:
```

> **Tip**: Use a mix of uppercase letters, lowercase letters, numbers, and special characters to create a strong password.

### 2. **Login to the CLI**

After setting the password, you need to log in to the CLI to use any administrative commands. Use the following command:

```bash
sia login
```

You will be prompted to enter the admin password:

```bash
$ sia login                                
Enter admin password:
```

Once logged in, you will have access to all CLI commands necessary to manage your SIA servers.

> **Note**: Always ensure that the admin password is kept secure and shared only with authorized personnel.

[Back to Documentation](/docs/README.md)
