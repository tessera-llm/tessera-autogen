"""E2E constructor-survives test for tessera_autogen factories.

Requires autogen_ext.models.openai + .anthropic installed. Skips gracefully
without them so test_config.py can still run on lean dev envs.

Real network E2E lives in the integration suite at consolidate-cycle time.
"""

from __future__ import annotations

import pytest

pytest.importorskip("autogen_ext.models.openai")

from tessera_autogen import tessera_openai_client  # noqa: E402


def test_openai_client_factory_constructs() -> None:
    client = tessera_openai_client(
        model="gpt-4o",
        openai_api_key="sk-test-openai",
        tessera_api_key="tk_test_e2e",
    )
    # OpenAIChatCompletionClient stores the underlying AsyncOpenAI client;
    # exact attribute name is internal — the smoke test only asserts that
    # the constructor completed without raising.
    assert client is not None


def test_anthropic_client_factory_constructs() -> None:
    pytest.importorskip("autogen_ext.models.anthropic")
    from tessera_autogen import tessera_anthropic_client

    client = tessera_anthropic_client(
        model="claude-sonnet-4-6",
        anthropic_api_key="sk-ant-test",
        tessera_api_key="tk_test_e2e",
    )
    assert client is not None
