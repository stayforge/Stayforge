Welcome to the Stayforge Wiki! This guide provides information on deploying Stayforge, 
using its APIs and webhooks, and developing plugins for Stayforge.

# Deploy Stayforge

請先安裝Docker。

然後，clone Stayforge倉庫，運行`docker compose up -d`來啟動容器。確保您的`80`端口沒用被佔用，
並且防火牆允許內部的`80`端口流量。

    ⚠️注意：單個Stayforge實例並不為高併發設計。您不應該讓Stayforge直接承受流量。
    在Stayforge之前，您必須配置一個Load balancer/Api Getaways以保證Stayforge的穩定性。


### 如何配置SSL？

我們建議您在前置反向代理之上配置SSL來實現Https加密，並配置合理的防火牆規則以保證安全性。
若因合規性或您有任何進一步需求，您可以在Stayforge上配置SSL證書，使得流量可以得到全段加密。

[反向代理配置指南]()


#### 在Stayforge上配置SSL實現嚴格加密

關於在Stayforge上配置SSL證書，敬請訪問[在Stayforge上配置流量]()。

# 二次開發

Stayforge的所有功能依賴於強大的Stayforge API & Webhook。正因如此，您有足夠的可能對Stayforge進行二次開發。

我們提供了Python、Javascript、Rust、Java等語言的SDK，但您仍然可以用自己喜歡的任何語言來開發Stayforge插件。

## Stayforge API & Webhook
The Stayforge API and webhook system enable seamless integration with all Stayforge functionalities. 
By utilizing these tools, you can achieve extensive customization and automation.
The Stayforge plug-in is also implemented in basic form by calling the Stayforge API.
For specific Stayforge Plugins development tutorial implementation, please refer to the Plugins documentation.

### Stayforge API Documentation Access

- Within the Stayforge Instance: Access detailed API documentation directly from your Stayforge dashboard.
- Official Stayforge Website: Find the latest static API documentation for offline reference.

API and Webhook Usage

-	Calling the Stayforge API: Allows interaction with Stayforge’s core functionalities programmatically.
-	Receiving the Stayforge Webhook: Enables automated responses to events triggered within Stayforge.

For more advanced development, Stayforge Plugins can also leverage these APIs and webhooks. 
Detailed implementation tutorials are available in the Plugins documentation.

### Stayforge Webhook

您可以通過調用Stayforge Webhooks Manager API來設定您想捕獲的在Stayforge API文檔上顯示的任何API。
當API被調用時，Stayforge Webhook Middleware 將會捕獲`Request`以及`Response`的內容並通過JSON提交到您的`Endpoint`。


# Stayforge Plugins

Stayforge offers a robust plugin engine to extend its capabilities. Plugins are powered by 
the StayforgeAPI and webhooks, allowing extensive customization.

Stayforge provides a powerful plug-in engine. The basic form is implemented by calling 
the Stayforge API and receiving the Stayforge Webhook.
Stayforge Plugins are distributed in the form of container images. In a production environment, you need to deploy Plugins as a container to run with Stayforge.
So, in theory, you can make Stayforge Plugins in any programming language you like.

Of course, we provide SDK Tools for Python, Node.js (scheduled), Java (scheduled), and Rust (scheduled).

### Plugin Development

- Container-Based Deployment: Stayforge Plugins are distributed as container images. In production, these plugins must be deployed as containers to run alongside Stayforge.
- Language Flexibility: Plugins can be developed in any programming language of your choice.

### SDK Tools

To simplify plugin development, Stayforge provides SDK tools:
•	Available Now: Python
•	Scheduled: Node.js, Java, and Rust

