"""Provider config + factory functions for routing AutoGen agents through
the Tessera proxy.

AutoGen 0.4+ split the framework into autogen_core (primitives) +
autogen_agentchat (high-level agents) + autogen_ext (provider adapters).
Provider clients live under autogen_ext.models.<provider>:
- OpenAIChatCompletionClient(model, api_key, base_url, default_headers, ...)
- AnthropicChatCompletionClient(model, api_key, base_url, default_headers, ...)

Both accept the same base_url + default_headers pattern that the AsyncOpenAI
and AsyncAnthropic SDKs accept (they wrap those SDKs internally). Tessera's
proxy speaks the same OpenAI + Anthropic wire formats at /v1/<provider>,
so the integration is a thin shim: spread the proxy endpoint + headers
into the client constructor.

Field names verified against autogen-ext 0.4+ source (2026-05-19):
- OpenAIChatCompletionClient(model, api_key, base_url, default_headers)
- AnthropicChatCompletionClient(model, api_key, base_url, default_headers)

v0.1 covers OpenAI + Anthropic. Mistral/Gemini variants exist in
autogen_ext but were not verified end-to-end; queued for v0.2.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Literal

TESSERA_BASE_URL = "https://api.tesseraai.io"

ProviderName = Literal["openai", "anthropic"]


def _validate_api_key(api_key: str) -> str:
    if not isinstance(api_key, str) or not api_key:
        raise ValueError(
            "tessera_*_config(api_key=...) requires a non-empty string. "
            "Get a free key from https://tesseraai.io/dev"
        )
    return api_key


def _proxy_endpoint(provider: ProviderName) -> str:
    return f"{TESSERA_BASE_URL}/v1/{provider}"


def _headers(api_key: str, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    headers = {"x-tessera-api-key": api_key}
    if extra:
        headers.update(extra)
    return headers


def tessera_openai_config(
    api_key: str,
    extra_headers: Optional[Dict[str, str]] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Kwargs for `OpenAIChatCompletionClient(...)` to route through Tessera.

    Example::

        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from tessera_autogen import tessera_openai_config

        client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key="sk-...",  # your OpenAI key
            **tessera_openai_config(api_key="tk_..."),
        )
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint("openai")
    return {
        "base_url": endpoint,
        "default_headers": _headers(api_key, extra_headers),
    }


def tessera_anthropic_config(
    api_key: str,
    extra_headers: Optional[Dict[str, str]] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Kwargs for `AnthropicChatCompletionClient(...)` to route through Tessera.

    Example::

        from autogen_ext.models.anthropic import AnthropicChatCompletionClient
        from tessera_autogen import tessera_anthropic_config

        client = AnthropicChatCompletionClient(
            model="claude-sonnet-4-6",
            api_key="sk-ant-...",  # your Anthropic key
            **tessera_anthropic_config(api_key="tk_..."),
        )
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint("anthropic")
    return {
        "base_url": endpoint,
        "default_headers": _headers(api_key, extra_headers),
    }


def tessera_config(
    provider: ProviderName,
    api_key: str,
    extra_headers: Optional[Dict[str, str]] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Generic dispatcher — returns the right kwargs dict for the given provider."""
    mapping = {
        "openai": tessera_openai_config,
        "anthropic": tessera_anthropic_config,
    }
    if provider not in mapping:
        raise ValueError(
            f"Unknown provider {provider!r}. Supported: {list(mapping)}. "
            "Mistral / Gemini are queued for v0.2 — see the README."
        )
    return mapping[provider](
        api_key=api_key, extra_headers=extra_headers, base_url=base_url
    )


def tessera_openai_client(
    model: str,
    openai_api_key: str,
    tessera_api_key: str,
    extra_headers: Optional[Dict[str, str]] = None,
    base_url: Optional[str] = None,
    **client_kwargs: Any,
) -> Any:
    """Construct an AutoGen `OpenAIChatCompletionClient` pre-wired to Tessera.

    Lazy-imports `autogen_ext.models.openai.OpenAIChatCompletionClient` so
    this module imports cleanly without autogen-ext installed.

    Example::

        from autogen_agentchat.agents import AssistantAgent
        from tessera_autogen import tessera_openai_client

        client = tessera_openai_client(
            model="gpt-4o",
            openai_api_key="sk-...",
            tessera_api_key="tk_...",
        )
        agent = AssistantAgent(name="researcher", model_client=client)
    """
    from autogen_ext.models.openai import (  # type: ignore[import-not-found]
        OpenAIChatCompletionClient,
    )

    cfg = tessera_openai_config(
        api_key=tessera_api_key, extra_headers=extra_headers, base_url=base_url
    )
    return OpenAIChatCompletionClient(
        model=model,
        api_key=openai_api_key,
        **cfg,
        **client_kwargs,
    )


def tessera_anthropic_client(
    model: str,
    anthropic_api_key: str,
    tessera_api_key: str,
    extra_headers: Optional[Dict[str, str]] = None,
    base_url: Optional[str] = None,
    **client_kwargs: Any,
) -> Any:
    """Construct an AutoGen `AnthropicChatCompletionClient` pre-wired to Tessera.

    Lazy-imports `autogen_ext.models.anthropic.AnthropicChatCompletionClient`.

    Example::

        from autogen_agentchat.agents import AssistantAgent
        from tessera_autogen import tessera_anthropic_client

        client = tessera_anthropic_client(
            model="claude-sonnet-4-6",
            anthropic_api_key="sk-ant-...",
            tessera_api_key="tk_...",
        )
        agent = AssistantAgent(name="researcher", model_client=client)
    """
    from autogen_ext.models.anthropic import (  # type: ignore[import-not-found]
        AnthropicChatCompletionClient,
    )

    cfg = tessera_anthropic_config(
        api_key=tessera_api_key, extra_headers=extra_headers, base_url=base_url
    )
    return AnthropicChatCompletionClient(
        model=model,
        api_key=anthropic_api_key,
        **cfg,
        **client_kwargs,
    )
