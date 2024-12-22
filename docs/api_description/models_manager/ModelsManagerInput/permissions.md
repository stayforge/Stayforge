### Example

`null` or `JSON Started dict`.

When the value is null, the content in the plug-in configuration `permissions.json` is used.

Stayforge APIs that can be called by the model, starting with `_` are method names.

```json
{
  "room": {
    "_methods": {
      "_post": {
        "_allow": true,
        "_webhook": true,
        "_webhook_path": "/webhook/room"
      }
    }
  }
}
```

### Key Elements

1. **API Name** (`<API Name>`):
    - Represents the name of the API the model interacts with (e.g., `"room"`).

2. **_methods**:
    - Defines the HTTP methods (e.g., `_post`, `_get`, `_put`, `_delete`) that the API supports.

3. **HTTP Method Configuration**:
    - `_allow` (Required):
        - A boolean indicating whether the method is allowed for models. If `False`, the model cannot use this method.
    - `_webhook` (Optional):
        - A boolean indicating whether webhook functionality is enabled for this method. If `True`, a `_webhook_path`
          must be specified.
    - `_webhook_path` (Required if `_webhook` is `True`):
        - A string representing the webhook submission URL path. The full URL is constructed by concatenating the
          `model_host` with `_webhook_path`.
