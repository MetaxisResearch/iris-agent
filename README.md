<p align="center">
  <img src="assets/banner.png" alt="Iris Agent" width="100%">
</p>

# Iris Agent ⚕
[![Batch C](https://github.com/MetaxisResearch/iris-agent/actions/workflows/deploy-batch-e.yml/badge.svg)](https://github.com/MetaxisResearch/iris-agent/actions/workflows/deploy-batch-e.yml)
<p align="center">

  <a href="https://MetaxisResearch.com/docs/"><img src="https://img.shields.io/badge/Docs-Iris--agent.Metaxis Research.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://discord.gg/Metaxis Research"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/Metaxis Research/iris-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://MetaxisResearch.com"><img src="https://img.shields.io/badge/Built%20by-Metaxis%20Research-blueviolet?style=for-the-badge" alt="Built by Metaxis Research"></a>
  
</p>

**The self-improving AI agent built by [Metaxis Research](https://MetaxisResearch.com).** It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — [Metaxis Portal](https://MetaxisResearch.com), [OpenRouter](https://openrouter.ai) (200+ models), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), OpenAI, or your own endpoint. Switch with `Iris model` — no code changes, no lock-in.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six terminal backends — local, Docker, SSH, Daytona, Singularity, and Modal. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, Atropos RL environments, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

---

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/MetaxisResearch/iris-agent/main/scripts/install.sh | bash
```

Works on Linux, macOS, and WSL2. The installer handles everything — Python, Node.js, dependencies, and the `Iris` command. No prerequisites except git.

> **Windows:** Native Windows is not supported. Please install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run the command above.

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
Iris              # start chatting!
```

---

## Getting Started

```bash
Iris              # Interactive CLI — start a conversation
Iris model        # Choose your LLM provider and model
Iris tools        # Configure which tools are enabled
Iris config set   # Set individual config values
Iris gateway      # Start the messaging gateway (Telegram, Discord, etc.)
Iris setup        # Run the full setup wizard (configures everything at once)
Iris claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
Iris update       # Update to the latest version
Iris doctor       # Diagnose any issues
```

📖 **[Full documentation →](https://MetaxisResearch.com/iris-agent/docs/)**

---

## Documentation

All documentation lives at **[iris-agent.Metaxis Research.com/docs](https://MetaxisResearch.com/iris-agent/docs/)**:

| Section | What's Covered |
|---------|---------------|
| [Quickstart](https://MetaxisResearch.com/iris-agent/docs/getting-started/quickstart) | Install → setup → first conversation in 2 minutes |
| [CLI Usage](https://MetaxisResearch.com/iris-agent/docs/user-guide/cli) | Commands, keybindings, personalities, sessions |
| [Configuration](https://MetaxisResearch.com/iris-agent/docs/user-guide/configuration) | Config file, providers, models, all options |
| [Messaging Gateway](https://MetaxisResearch.com/iris-agent/docs/user-guide/messaging) | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://MetaxisResearch.com/iris-agent/docs/user-guide/security) | Command approval, DM pairing, container isolation |
| [Tools & Toolsets](https://MetaxisResearch.com/iris-agent/docs/user-guide/features/tools) | 40+ tools, toolset system, terminal backends |
| [Skills System](https://MetaxisResearch.com/iris-agent/docs/user-guide/features/skills) | Procedural memory, Skills Hub, creating skills |
| [Memory](https://MetaxisResearch.com/iris-agent/docs/user-guide/features/memory) | Persistent memory, user profiles, best practices |
| [MCP Integration](https://MetaxisResearch.com/iris-agent/docs/user-guide/features/mcp) | Connect any MCP server for extended capabilities |
| [Cron Scheduling](https://MetaxisResearch.com/iris-agent/docs/user-guide/features/cron) | Scheduled tasks with platform delivery |
| [Context Files](https://MetaxisResearch.com/iris-agent/docs/user-guide/features/context-files) | Project context that shapes every conversation |
| [Architecture](https://MetaxisResearch.com/iris-agent/docs/developer-guide/architecture) | Project structure, agent loop, key classes |
| [Contributing](https://MetaxisResearch.com/iris-agent/docs/developer-guide/contributing) | Development setup, PR process, code style |
| [CLI Reference](https://MetaxisResearch.com/iris-agent/docs/reference/cli-commands) | All commands and flags |
| [Environment Variables](https://MetaxisResearch.com/iris-agent/docs/reference/environment-variables) | Complete env var reference |

---

## Migrating from OpenClaw

If you're coming from OpenClaw, Iris can automatically import your settings, memories, skills, and API keys.

**During first-time setup:** The setup wizard (`Iris setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.

**Anytime after install:**

```bash
Iris claw migrate              # Interactive migration (full preset)
Iris claw migrate --dry-run    # Preview what would be migrated
Iris claw migrate --preset user-data   # Migrate without secrets
Iris claw migrate --overwrite  # Overwrite existing conflicts
```

What gets imported:
- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.Iris/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

See `Iris claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://MetaxisResearch.com/iris-agent/docs/developer-guide/contributing) for development setup, code style, and PR process.

Quick start for contributors:

```bash
git clone --recurse-submodules https://github.com/MetaxisResearch/iris-agent.git
cd iris-agent
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[all,dev]"
uv pip install -e "./mini-swe-agent"
python -m pytest tests/ -q
```

---

## Community

- 💬 [Discord](https://discord.gg/MetaxisResearch)
- 📚 [Skills Hub](https://agentskills.io)
- 🐛 [Issues](https://github.com/MetaxisResearch/iris-agent/issues)
- 💡 [Discussions](https://github.com/MetaxisResearc/iris-agent/discussions)

---

## License

MIT — see [LICENSE](LICENSE).

Built by [Metaxis Research](https://MetaxisResearch.com).
