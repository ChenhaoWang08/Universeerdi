# Safety Judge

Fail the change if any of the following appear:

- secrets, credentials, tokens, or `.env` files
- runtime network access or external API integration
- deployment configuration
- generated cache files or large bundled datasets
- edits to forbidden files
- destructive commands or automatic cleanup
