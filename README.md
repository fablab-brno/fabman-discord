# fabman-discord — Discord Bot for FabMan notifications

## Installation

This project uses [`poetry`](https://python-poetry.org/) for dependency management.

1. Run `poetry install` to install all dependencies
2. Run `pre-commit install` locally to setup pre-commit hook

## Usage

Environment variables:

- `DISCORD__BOT_TOKEN` - Authentication token for Discord bot.
- `FABMAN_WEBHOOK_SECRET` - Secret `key` passed in URL query to authenticate webhook calls.

## Deployment

- Python version is set in `pyproject.toml` and `runtime.txt`. These version must match.
