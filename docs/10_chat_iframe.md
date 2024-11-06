[Back to Documentation](/docs/README.md)

# Integrating Chat

The web chat client in SIA is **not** designed to be exposed directly to end-users. Instead, administrators are expected to embed the chat client within an existing web application to provide users with a seamless experience. This is typically achieved through the use of an iframe, allowing the host application to fully manage user access and interface features.

Below, we provide an example of how to integrate the chat client into a React page.

## Integration in a React Application

The following code demonstrates how you can embed the SIA chat client using React. The iframe approach allows the chat to adjust dynamically based on the parent application's requirements:

```javascript
// Chat page component
import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';

const ChatPage = () => {
    const { agentname } = useParams();
    const iframeref = useRef(null);
    const deltaH = 36; // Set height offset to match padding of parent div (e.g., padding-4)
    const [frameheight, setFrameheight] = useState(`${deltaH}px`);
    const server = "http://x.x.x.x" // set this to the ip or domain of sia servers

    useEffect(() => {
        const handleIframeMessage = (event) => {
            if (event.data.type === "iframeHeight") {
                setFrameheight(`${event.data.height + deltaH}px`);
            }
        };
        // Event listener for adjusting iframe height dynamically
        window.addEventListener("message", handleIframeMessage);
        return () => window.removeEventListener("message", handleIframeMessage);
    }, []);

    return (
        <div className="flex flex-col h-screen">
            <div className="flex flex-grow flex-col justify-start items-center p-4">
                <iframe
                    ref={iframeref}
                    className='w-full overflow-hidden'
                    width="100%"
                    height={frameheight}
                    src={`${server}/chat/${agentname}`}
                />
            </div>
        </div>
    );
};

export default ChatPage;
```

### Explanation of the Code

1. **React Imports**: We import `useState`, `useEffect`, and `useRef` from React to handle state, side effects, and references.

2. **`useParams` Hook**: The `useParams` hook from `react-router-dom` is used to extract the `agentname` parameter from the URL, allowing the iframe to point to the correct agent's chat page.

3. **Iframe Reference and Height Management**: The `useRef` hook is used to reference the iframe element, while `useState` manages the height of the iframe to ensure it adjusts dynamically:
   - **Height Adjustment**: The `handleIframeMessage` function listens for messages from the iframe to adjust its height dynamically based on the content, ensuring the chat is always fully visible without unnecessary scrollbars.

4. **Embedding the Chat Client**: The iframe's `src` points to the agent's chat endpoint (`${server}/chat/${agentname}`). The iframe dynamically resizes based on messages sent from the chat client. 

5. **Agent Name in src**: Note that the agentname must be passed in the url.

6. **Styling**: The chat container is styled using Tailwind CSS classes for consistent layout and padding.

> **Note**: Make sure the SIA chat endpoint is accessible from the domain of your main web application. Proper CORS settings are required to allow cross-origin communication between the iframe and the parent page.

## Enabling access to web chat

The chat interface, by default, is disabled within Sia's settings. Administrators need to allow access to the host web application which has integrated the web chat client. This is done in the `nginx.conf` on the sia servers' farm.

The following section must be edited to add the ip address or domain name of the hosted web app

```
    ...
    ...
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
    ...
    ...
```

[Back to Documentation](/docs/README.md)

