# swcapi (Software Campus Easyverein API Integration)

A Python integration for interacting with the Easyverein API v2.0, pre-configured with Dynaconf for dynamic settings management and automatic token refresh handling.

## Features

- **Automatic Token Refresh**: Seamlessly integrates with `python-easyverein` token refresh mechanism. Updates are automatically written back to your local secrets file.
- **Config Management**: Uses Dynaconf to load configuration and secrets from the `config/` directory.
- **CLI Entrypoint**: Registered entrypoint via Poetry for running operations directly from the terminal.

---

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Clone the repository
git clone <repository-url>
cd swcapi

# Install dependencies and the package
poetry install
```

---

## Configuration

Configuration files are located in the `config/` directory (which is ignored by Git to prevent leaking sensitive credentials).

### 1. `config/settings.toml`
Stores public configurations.
```toml
test = "test"
```

### 2. `config/.secrets.toml`
Stores sensitive access tokens and credentials.
```toml
apikey = "your-easyverein-api-token"
```

### Automatic Settings Writing
The settings loader is configured to support write-backs. Assigning to write-supported settings updates the file on disk instantly:
```python
from swcapi.config import settings

# This automatically updates the file config/.secrets.toml
settings.apikey = "new_token"
```

---

## Token Refresh

The `easyverein` API token refresh is handled in [utils.py](file:///Users/s.roehrl/git/swcapi/swcapi/utils.py).
When initializing the API client:
```python
from easyverein import EasyvereinAPI
from swcapi.config import settings
from swcapi.utils import handle_token_refresh

ev_client = EasyvereinAPI(
    api_key=settings.apikey,
    api_version="v2.0",
    token_refresh_callback=handle_token_refresh,
    auto_refresh_token=True,
)
```
When `EasyvereinAPI` auto-refreshes an expired token, the `handle_token_refresh` callback updates `settings.apikey`, which writes the updated bearer token back to `config/.secrets.toml` dynamically.

---

## Usage

You can run the main program using the Poetry script entrypoint:

```bash
poetry run swcapi
```

Alternatively, you can run the module directly:

```bash
poetry run python -m swcapi
```
