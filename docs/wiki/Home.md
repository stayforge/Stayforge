Welcome to the Stayforge Wiki! This guide provides information on deploying Stayforge,
using its APIs and webhooks, and developing plugins for Stayforge.

# Deploy Stayforge

Start by installing Docker.

Next, clone the Stayforge repository and run `docker compose up -d` to start the container. Ensure port `80` is not in
use,
and configure your firewall to allow internal traffic on port `80`.

    ⚠️ Note: A single Stayforge instance is not designed for high concurrency. Avoid sending direct traffic to Stayforge.
    Always configure a load balancer or API gateway in front of Stayforge to ensure stability.

### Configure SSL

We recommend configuring SSL on your reverse proxy to enable HTTPS encryption and setting robust firewall rules for
security purposes.
If required by compliance or for additional needs, you can directly configure an SSL certificate on Stayforge, enabling
end-to-end encryption.

[Reverse proxy configuration guide]()

#### Strict Encryption with SSL on Stayforge

For detailed instructions on configuring SSL certificates on Stayforge, visit [Configuring Traffic on Stayforge]().

# Secondary Development

Stayforge's functionality is powered entirely by its robust API and Webhook system, providing extensive opportunities
for developers.

SDKs are available for Python, Javascript, Rust, Java, and more. However, you can create Stayforge plugins in any
programming language of your choice.

## Stayforge API & Webhook

The Stayforge API and webhook systems enable smooth integration with Stayforge's powerful features, allowing for
advanced customization and automation.
Essentially, Stayforge plugins utilize the API for requests and the webhook for responses.
For detailed tutorials on plugin development, please refer to the Plugins documentation.

### Accessing Stayforge API Documentation

- From within Stayforge: Access detailed API documentation directly from the Stayforge dashboard.
- From the official website: Find the latest static API documentation for offline use.

API and Webhook Capabilities:

- **API Calls:** Programmatically interact with Stayforge's core features.
- **Webhooks:** Automate responses to specific events triggered within Stayforge.

Stayforge Plugins can take full advantage of these APIs and webhooks. Detailed implementation guides are available in
the Plugins documentation.

### Stayforge Webhooks

You can capture any API activity by using the Stayforge Webhook Manager API, as detailed in the Stayforge API
documentation.
When triggered, the Stayforge webhook middleware captures the `Request` and `Response` contents and sends them to your
configured `Endpoint` in JSON format.

# Stayforge Plugins

Stayforge offers a powerful plugin engine for extending its capabilities through API and webhook integration, enabling
deep customization.

Plugins are distributed as container images. In a production environment, these plugins must run as containers alongside
Stayforge.
This design allows plugin development in any programming language.

Stayforge also provides SDK tools to simplify development, with support for Python currently available, and support for
Node.js, Java, and Rust coming soon.

### Plugin Development

- **Container-Based Deployment:** Plugins are distributed as container images and must be deployed alongside Stayforge
  in a containerized environment.
- **Language Flexibility:** Create Stayforge plugins in any programming language.

### SDK Tools

To streamline plugin development, Stayforge provides SDK tools:

- **Available Now:** Python
- **Coming Soon:** Node.js, Java, and Rust

