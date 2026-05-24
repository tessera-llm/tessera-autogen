# tessera-autogen

[![PyPI](https://img.shields.io/pypi/v/tessera-autogen.svg)](https://pypi.org/project/tessera-autogen/)
[![Python](https://img.shields.io/pypi/pyversions/tessera-autogen.svg)](https://pypi.org/project/tessera-autogen/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Drop-in [Tessera](https://tesseraai.io) integration for [AutoGen](https://github.com/microsoft/autogen) 0.4+ (`autogen_core` / `autogen_agentchat` / `autogen_ext`). One line of config routes every LLM call your AutoGen agents make through Tessera's auto-route + auto-cache + auto-compress + auto-batch proxy.

**Free 60M tokens/month. Production: 20% of measured savings.** No card up front.

## Install

```bash
pip install tessera-autogen
```

Requires Python 3.10+. `autogen-core` + `autogen-ext` are peer dependencies. Install them alongside this package.

## Usage

The most common pattern uses a bundled factory to construct a pre-wired AutoGen `ChatCompletionClient`:

```python
from autogen_agentchat.agents import AssistantAgent
from tessera_autogen import tessera_openai_client

client = tessera_openai_client(
    model="gpt-4o",
    openai_api_key="sk-...",   # your OpenAI key
    tessera_api_key="tk_...",  # get a free one at tesseraai.io/dev
)

agent = AssistantAgent(name="researcher", model_client=client)

# Rest of your AutoGen code runs unchanged. Single-agent calls,
# SelectorGroupChat, Swarm, tool use all route through Tessera and
# benefit from auto-optimization.
```

For Anthropic models:

```python
from tessera_autogen import tessera_anthropic_client

client = tessera_anthropic_client(
    model="claude-sonnet-4-6",
    anthropic_api_key="sk-ant-...",
    tessera_api_key="tk_...",
)
```

For explicit `ChatCompletionClient` construction (rare; useful when you need fine-grained client kwargs):

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tessera_autogen import tessera_openai_config

client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="sk-...",
    **tessera_openai_config(api_key="tk_..."),
)
```

## What Tessera does for your AutoGen workloads

- **Auto-route**: calls to expensive models are evaluated for a cheaper alternative that preserves quality on canary samples.
- **Auto-cache**: exact-match + semantic cache for repeat queries. Multi-agent loops often re-issue identical sub-prompts; cache returns are free.
- **Auto-compress**: per-role heuristic compression on system prompts and tool descriptions (system + user toggles independent). Preserves code fences and JSON shapes. 5–15% on prompt tokens.
- **Auto-batch**: async teams with batch-tolerant SLAs get arbitraged onto provider batch APIs for ~50% cost reduction.

All gated by per-workload quality canaries; toggle any mechanic on/off from the [Tessera dashboard](https://ledger.tesseraai.io). Free Sandbox tier gives you observe-only mechanics; Production tier unlocks the full stack.

## Supported providers (v0.1)

| Provider | Status | Config function |
| --- | --- | --- |
| OpenAI | ✅ verified | `tessera_openai_config`, `tessera_openai_client` |
| Anthropic | ✅ verified | `tessera_anthropic_config`, `tessera_anthropic_client` |
| Mistral / Gemini | 🚧 queued for v0.2 | n/a |

v0.1 covers ~85% of customer traffic per our outreach research. Open an issue if you need a provider on the queue surfaced sooner.

## Companion packages

<!-- COMPANION-PACKAGES-START -->
Companion to [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk) (vanilla provider SDKs), [`tessera-langchain`](https://github.com/tessera-llm/tessera-langchain) (LangChain integration), [`tessera-vercel-ai`](https://github.com/tessera-llm/tessera-vercel-ai) (Vercel AI SDK integration), [`tessera-llamaindex`](https://github.com/tessera-llm/tessera-llamaindex) (LlamaIndex integration), [`tessera-mastra`](https://www.npmjs.com/package/@tessera-llm/mastra) (Mastra Agent framework integration), [`tessera-pydantic-ai`](https://pypi.org/project/tessera-pydantic-ai/) (Pydantic AI integration), and [`tessera-crewai`](https://pypi.org/project/tessera-crewai/) (CrewAI multi-agent integration). Same proxy, same mechanic stack, AutoGen-shaped API.
<!-- COMPANION-PACKAGES-END -->

## License

Apache 2.0. See [LICENSE](LICENSE).

---

## About Tessera

Tessera is the **substrate layer** for **LLM cost optimization**, also called the **Optimize Layer** in our product surface. A thin proxy that sits in your application's **request-path**, applies a conservative cascade of optimization mechanics, and measures every saved dollar against an **audit-immutable** baseline. We bill **20% of verified savings**, prepaid. Zero savings = zero fee. No per-token gateway fee, no subscription, no minimum monthly commitment; the category we operate in is "**success-fee LLM optimizer**," distinct from per-token **AI gateways** and observability dashboards.

Where observability tools tell you what you spent and AI gateways re-shape the request without measuring the cost delta, Tessera is the layer that does both, and only takes a cut when the measured savings are positive. The **verified-savings ledger** at [`ledger.tesseraai.io`](https://ledger.tesseraai.io) shows every original-vs-actual cost pair, snapshot-pinned to a `pricing_catalog` version captured at request time. Mid-contract price changes don't retroactively alter past savings. This is the **FinOps**-friendly model for AI inference: every line of the bill traces to a code-enforced rule.

Apache-2.0. Operated by Fintechagency OÜ (Tallinn, Estonia, registry code 16638667). Issues: [github.com/tessera-llm/tessera-autogen/issues](https://github.com/tessera-llm/tessera-autogen/issues).

- Developer entry: [tesseraai.io/dev](https://tesseraai.io/dev)
- Mechanic reference: [tesseraai.io/how-it-works](https://tesseraai.io/how-it-works)
- Dashboard: [ledger.tesseraai.io](https://ledger.tesseraai.io)
- Engineering blog: [tesseraai.io/blog](https://tesseraai.io/blog)
