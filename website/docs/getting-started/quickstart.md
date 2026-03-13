---
sidebar_position: 1
title: "Quickstart"
description: "Your first conversation with Iris Agent — from install to chatting in 2 minutes"
---

# Quickstart

This guide walks you through installing Iris Agent, setting up a provider, and having your first conversation. By the end, you'll know the key features and how to explore further.

## 1. Install Iris Agent

Run the one-line installer:

```bash
# Linux / macOS / WSL2
curl -fsSL https://raw.githubusercontent.com/Metaxis Research/iris-agent/main/scripts/install.sh | bash
```

:::tip Windows Users
Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) first, then run the command above inside your WSL2 terminal.
:::

After it finishes, reload your shell:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

## 2. Set Up a Provider

The installer configures your LLM provider automatically. To change it later, use one of these commands:

```bash
Iris model       # Choose your LLM provider and model
Iris tools       # Configure which tools are enabled
Iris setup       # Or configure everything at once
```

`Iris model` walks you through selecting an inference provider:

| Provider | What it is | How to set up |
|----------|-----------|---------------|
| **Metaxis Portal** | Subscription-based, zero-config | OAuth login via `Iris model` |
| **OpenAI Codex** | ChatGPT OAuth, uses Codex models | Device code auth via `Iris model` |
| **OpenRouter** | 200+ models, pay-per-use | Enter your API key |
| **Custom Endpoint** | VLLM, SGLang, any OpenAI-compatible API | Set base URL + API key |

:::tip
You can switch providers at any time with `Iris model` — no code changes, no lock-in.
:::

## 3. Start Chatting

```bash
Iris
```

That's it! You'll see a welcome banner with your model, available tools, and skills. Type a message and press Enter.

```
❯ What can you help me with?
```

The agent has access to tools for web search, file operations, terminal commands, and more — all out of the box.

## 4. Try Key Features

### Ask it to use the terminal

```
❯ What's my disk usage? Show the top 5 largest directories.
```

The agent will run terminal commands on your behalf and show you the results.

### Use slash commands

Type `/` to see an autocomplete dropdown of all commands:

| Command | What it does |
|---------|-------------|
| `/help` | Show all available commands |
| `/tools` | List available tools |
| `/model` | Switch models interactively |
| `/personality pirate` | Try a fun personality |
| `/save` | Save the conversation |

### Multi-line input

Press `Alt+Enter` or `Ctrl+J` to add a new line. Great for pasting code or writing detailed prompts.

### Interrupt the agent

If the agent is taking too long, just type a new message and press Enter — it interrupts the current task and switches to your new instructions. `Ctrl+C` also works.

### Resume a session

When you exit, Iris prints a resume command:

```bash
Iris --continue    # Resume the most recent session
Iris -c            # Short form
```

## 5. Explore Further

Here are some things to try next:

### Set up a sandboxed terminal

For safety, run the agent in a Docker container or on a remote server:

```bash
Iris config set terminal.backend docker    # Docker isolation
Iris config set terminal.backend ssh       # Remote server
```

### Connect messaging platforms

Chat with Iris from your phone via Telegram, Discord, Slack, or WhatsApp:

```bash
Iris gateway setup    # Interactive platform configuration
```

### Schedule automated tasks

```
❯ Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram.
```

The agent will set up a cron job that runs automatically via the gateway.

### Browse and install skills

```bash
Iris skills search kubernetes
Iris skills install openai/skills/k8s
```

Or use the `/skills` slash command inside chat.

### Try MCP servers

Connect to external tools via the Model Context Protocol:

```yaml
# Add to ~/.Iris/config.yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `Iris` | Start chatting |
| `Iris model` | Choose your LLM provider and model |
| `Iris tools` | Configure which tools are enabled per platform |
| `Iris setup` | Full setup wizard (configures everything at once) |
| `Iris doctor` | Diagnose issues |
| `Iris update` | Update to latest version |
| `Iris gateway` | Start the messaging gateway |
| `Iris --continue` | Resume last session |

## Next Steps

- **[CLI Guide](../user-guide/cli.md)** — Master the terminal interface
- **[Configuration](../user-guide/configuration.md)** — Customize your setup
- **[Messaging Gateway](../user-guide/messaging/index.md)** — Connect Telegram, Discord, Slack, WhatsApp
- **[Tools & Toolsets](../user-guide/features/tools.md)** — Explore available capabilities
