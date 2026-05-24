"""Tessera × AutoGen integration — drop-in cost optimization for any
AutoGen 0.4+ agent / team.

Usage (most common)::

    from autogen_agentchat.agents import AssistantAgent
    from tessera_autogen import tessera_openai_client

    client = tessera_openai_client(
        model="gpt-4o",
        openai_api_key="sk-...",
        tessera_api_key="tk_...",
    )
    agent = AssistantAgent(name="researcher", model_client=client)

    # Existing AutoGen code runs unchanged — single-agent calls,
    # SelectorGroupChat, Swarm, tool use all route through Tessera proxy.

See https://tesseraai.io/dev for the dashboard, free tier, and full
mechanic documentation.
"""

from tessera_autogen._version import __version__
from tessera_autogen._config import (
    TESSERA_BASE_URL,
    tessera_openai_config,
    tessera_anthropic_config,
    tessera_config,
    tessera_openai_client,
    tessera_anthropic_client,
)

__all__ = [
    "__version__",
    "TESSERA_BASE_URL",
    "tessera_openai_config",
    "tessera_anthropic_config",
    "tessera_config",
    "tessera_openai_client",
    "tessera_anthropic_client",
]
