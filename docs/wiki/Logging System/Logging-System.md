# Logging System

Stayforge has a two-tier logging system: one layer outputs system logs to the console, and another layer records
operation logs in the database.

# System Log

Stayforge outputs daily maintenance logs to the console. When `Debug` mode is enabled, Stayforge also outputs debug
logs.

## Enabling Debug Logs

Set the environment variable `Debug=true` to enable debug logs in the console output.

## Log File Storage Path

Stayforge is not designed as a stateless server, so logs are not saved to a specific file path. You can configure the
container to save console logs to the host machine
or collect logs through the logging services provided by major cloud platforms.

# Operation Log

Any API call behavior in Stayforge (excluding health check endpoints) will be logged in a MongoDB table. These logs
include:

- Requested HTTP headers and body
- Response body content
- Requester information
- Timestamps and other metadata

## Example Operation Log

```json

```

## Clearing Operation Logs

To save database disk space, you can configure a cron job on the host machine to regularly call the API for clearing
operation logs.

### Access Restrictions

By default, the API for clearing logs only allows access from intranet IP ranges (`10.0.0.0/8`, `172.16.0.0/16`,
`192.168.0.0/24`).

You can modify the access control by configuring the environment variable `ALLOW_CLEAN_LOG_SOURCE` as follows:

- Specify allowed IP ranges using a comma-separated list (e.g., `ALLOW_CLEAN_LOG_SOURCE=10.0.0.0/8,10.0.0.1/8`).
- Set `ALLOW_CLEAN_LOG_SOURCE=false` to block access from all network segments.
- Set `ALLOW_CLEAN_LOG_SOURCE=true` to allow access from all network segments.