# Changelog — tessera-autogen

All notable changes to this package are documented here. Versioning follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Wire format
compatibility across minor versions (0.X.Y) — breaking changes only on
major bumps.

## [0.1.0] — 2026-05-19 — first scaffold (monorepo)

- 2 verified provider config functions (`tessera_openai_config`,
  `tessera_anthropic_config`) returning the kwargs spread accepted by
  AutoGen's `OpenAIChatCompletionClient` / `AnthropicChatCompletionClient`
  constructors: `base_url` + `default_headers`.
- 2 lazy-import factory functions (`tessera_openai_client`,
  `tessera_anthropic_client`) constructing a pre-wired client instance.
- Generic dispatcher `tessera_config(provider, api_key, ...)` for callers
  iterating across providers.
- Unit-test coverage for config-dict shape + dispatcher error paths.
  E2E constructor-survives tests gate on autogen-ext availability via
  `pytest.importorskip` so they degrade gracefully on lean envs.
- py.typed marker — full type hints exposed to downstream type checkers.

Targets AutoGen 0.4+ (the post-split package layout — `autogen_core` +
`autogen_agentchat` + `autogen_ext`). Legacy `pyautogen` / AutoGen 0.2
not supported; use [tessera-sdk](https://github.com/tessera-llm/tessera-sdk)
directly with `pyautogen`'s `config_list` mechanism if you're on the
legacy package.

Publication to PyPI deferred until the next consolidate-cycle. Package
lives in the Tessera monorepo under `packages/tessera-autogen/` for the
scaffold cycle.
