"""Shared constants for Iris Agent.

Import-safe module with no dependencies — can be imported from anywhere
without risk of circular imports.
"""

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODELS_URL = f"{OPENROUTER_BASE_URL}/models"
OPENROUTER_CHAT_URL = f"{OPENROUTER_BASE_URL}/chat/completions"

Metaxis_API_BASE_URL = "https://inference-api.Metaxis Research.com/v1"
Metaxis_API_CHAT_URL = f"{Metaxis_API_BASE_URL}/chat/completions"
