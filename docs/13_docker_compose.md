[Back to Documentation](/docs/README.md)

# docker-compose.yaml

Sia's servers are a set of docker containers. Administrators have the ability to edit the contents of this file for their requirement


## Default docker-compose.yaml

The following is the docker-compose.yaml that is part of the inital download:

```yaml
services:
  # this downloads the models once on to host machine and exits
  model-downloader:
    image: rmrhub/model-downloader:v0.1.1
    volumes:
      - ./${DATA_DIR}:/app/${DATA_DIR} 
    restart: always 
    env_file:
      - .env

  # this is the inference-server
  inference-server:
    image: vllm/vllm-openai:latest
    ports:
      - "8000:8000"
    volumes:
      - ~/.cache/huggingface:/root/.cache/huggingface
    env_file:
      - .env
    ipc: "host"
    runtime: nvidia
    depends_on:
      - model-downloader    
    command: ["--model", "${LLM_MODEL_NAME}", "--dtype", "${DTYPE}"]

  # this is the embeddings server
  embeddings-server:
    hostname: embeddings-server
    image: rmrhub/sia-embeddings-server:v0.1.1
    environment:
      - PYTHONUNBUFFERED=1
    env_file:
      - .env  # Use environment variables from .env file
    volumes:
      - ./${DATA_DIR}:/app/${DATA_DIR}  # Mount shared data directory
    depends_on:
      - model-downloader
    ports:
      - "8002:8002"  # Expose port for the embeddings server API   
    restart: always
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # this is the api server
  api-server:
    hostname: api-server # required for web-server to proxy_pass
    image: rmrhub/sia-api-server:v0.1.1
    environment:
      - PYTHONUNBUFFERED=1 # can be removed in production
    env_file:
      - .env
    ports:
      - "8080:8080"
    volumes:
      - ./${DATA_DIR}:/app/${DATA_DIR}:rw  # Shared data directory
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    depends_on:
      - embeddings-server
    restart: always     
    command: >
      sh -c "chmod -R 777 /app/${DATA_DIR} && uvicorn main:app --host 0.0.0.0 --port 8080 --workers ${API_NO_WORKERS:-1}"

  # this is the proxy cum web-server for chat
  web-server:
    image: rmrhub/sia-web-server:v0.1.1
    ports:
      - "80:80"
      # Uncomment the following line to expose HTTPS port
      # - "443:443"
    depends_on:
      - api-server
    restart: always 
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

## Services

### Model-Downloader Service

This is the container that downloads the embeddings model used by the embeddings-server. Everytime the docker compose is run, it checks to see if the model is already downloaded and if so exits.

### Inference Server Service

Currently, the only supported Inference Server is the `vLLM Server`. vLLM provides a comprehensive list of [environment variables](https://docs.vllm.ai/en/latest/serving/env_vars.html) which are used when setting up the server, as well as [runtime variables](https://docs.vllm.ai/en/latest/models/engine_args.html). 

Adminstrators may wish to tune the performance of the inference server using these variables.


### Embeddings Server Service

This service uses the latest image from docker-hub (v0.1.1). It is recommended that no changes be made. However, if for some reason the port number is changed, Administrators may need to make the changes in the .env file too.


### API Server Service

This service uses the latest image from docker-hub (v0.1.1). Similar to the embeddings-server, there may be no need to make changes to these settings.

### Web Server Service

The Chat web server and proxy server is the front facing server. It is an nginx container with the following `nginx.conf` file available for administrators to edit.

```plaintext
# nginx.conf

# Defines the user and group that the Nginx worker processes run as.
# 'nginx' is the default user created in the Nginx Docker image.
user  nginx;

# Sets the number of worker processes. 'auto' means Nginx will
# automatically detect the number of available CPU cores and set
# the worker processes accordingly.
worker_processes  auto;

# Specifies the file where Nginx logs errors.
# The 'warn' parameter sets the minimum severity level of messages to log.
error_log  /var/log/nginx/error.log warn;

# Specifies the file where Nginx stores its process ID (PID).
pid        /var/run/nginx.pid;

# Events block contains directives that affect the general operation
# of Nginx worker processes.
events {
    # Sets the maximum number of simultaneous connections that can be opened by a worker process.
    worker_connections  1024;
}

# The 'http' block contains directives for handling HTTP web traffic.
http {
    # Includes MIME types for files served by Nginx.
    include       /etc/nginx/mime.types;

    # Sets the default MIME type for files whose types are not specified in the 'mime.types' file.
    default_type  application/octet-stream;

    # Enables or disables the use of sendfile(). 'on' uses the sendfile() system call
    # which can improve performance when serving static files.
    sendfile        on;

    # Sets the timeout for keep-alive connections with the client.
    # A higher value allows clients to keep connections open longer.
    keepalive_timeout  65;

    # Gzip compression settings to reduce the size of the responses and improve performance.
    # 'gzip on' enables gzip compression.
    gzip on;

    # Specifies the MIME types that will be compressed.
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Defines a group of servers (upstream) that can be referenced in 'proxy_pass'.
    # This is used to load balance or proxy requests to backend servers.
    upstream api_server {
        # Specifies the backend server's hostname (service name in Docker network) and port.
        server api-server:8080;
    }

    # Server block defines a virtual server that handles incoming HTTP requests.
    server {
        # Listens on port 80 (HTTP).
        listen 80;

        # Defines the server name (domain or IP) that the server block responds to.
        # 'localhost' means it will respond to requests to 'localhost'.
        server_name localhost;

        # Redirects all HTTP requests to HTTPS.
        # Uncomment the following line to enable redirection.
        # return 301 https://$host$request_uri;

        # Listens on port 443 (HTTPS).
        # Uncomment the following lines to enable HTTPS.
        # listen 443 ssl;
        # server_name your_domain.com;

        # Specifies the paths to the SSL certificate and key files.
        # Uncomment and provide your SSL certificate paths to enable HTTPS.
        # ssl_certificate     /etc/nginx/ssl/server.crt;
        # ssl_certificate_key /etc/nginx/ssl/server.key;

        # Configures the SSL protocols and ciphers.
        # Uncomment and adjust as needed for security requirements.
        # ssl_protocols       TLSv1.2 TLSv1.3;
        # ssl_ciphers         HIGH:!aNULL:!MD5;

        # Location block for serving static files.
        location / {
            # Sets the root directory for requests.
            root /usr/share/nginx/html;

            # Tries to serve the requested URI, if not found, serves 'index.html'.
            try_files $uri /index.html;
        }

        # Restrict iframe embedding using Content Security Policy (CSP)
        location /chat {
            root /usr/share/nginx/html;

            # Serve the chat page
            try_files $uri /index.html;

            # Add CSP header to restrict iframe embedding
            # Initially prevent access, uncomment and add domains as needed
            add_header Content-Security-Policy "frame-ancestors 'none'" always;

            # Example: Uncomment the below header to allow specific domains and comment the above header
            # add_header Content-Security-Policy "frame-ancestors authorized-domain.com another-authorized.com" always;

            # Prevent direct access
            if ($http_referer = "") {
                return 403;  # Block direct access if there is no referer
            }
        }

        # Location block for proxying API requests to the backend API server.
        location /api/ {
            # Proxies requests to the 'api_server' upstream defined earlier.
            proxy_pass http://api-server:8080/api/;

            # Preserves the original 'Host' header from the client.
            proxy_set_header Host $host;

            # Forwards the client's real IP address to the backend server.
            proxy_set_header X-Real-IP $remote_addr;

            # --- CORS Settings ---

            # Adds the 'Access-Control-Allow-Origin' header to the response.
            # '*' allows all origins; specify domains as needed for security.
            # Uncomment to enable CORS.
            # add_header 'Access-Control-Allow-Origin' '*' always;

            # Specifies the allowed HTTP methods.
            # Uncomment to enable.
            # add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;

            # Specifies the allowed HTTP headers.
            # Uncomment to enable.
            # add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization' always;

            # Handles preflight OPTIONS requests by returning a 204 No Content response.
            if ($request_method = OPTIONS ) {
                return 204;
            }
        }

        # Additional server blocks or configurations can be added here.
    }
}
```

Administrators may want to make changes to add https access and CORS access to these servers.


[Back to Documentation](/docs/README.md)

