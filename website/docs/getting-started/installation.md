---
sidebar_position: 2
title: "Installation"
description: "Install Iris Agent on Linux, macOS, or WSL2"
---

# Installation

Get Iris Agent up and running in under two minutes with the one-line installer, or follow the manual steps for full control.

## Quick Install

### Linux / macOS / WSL2

```bash
curl -fsSL https://raw.githubusercontent.com/Metaxis Research/iris-agent/main/scripts/install.sh | bash
```

:::warning Windows
Native Windows is **not supported**. Please install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run Iris Agent from there. The install command above works inside WSL2.
:::

### What the Installer Does

The installer handles everything automatically — all dependencies (Python, Node.js, ripgrep, ffmpeg), the repo clone, virtual environment, global `Iris` command setup, and LLM provider configuration. By the end, you're ready to chat.

### After Installation

Reload your shell and start chatting:

```bash
source ~/.bashrc   # or: source ~/.zshrc
Iris             # Start chatting!
```

To reconfigure individual settings later, use the dedicated commands:

```bash
Iris model          # Choose your LLM provider and model
Iris tools          # Configure which tools are enabled
Iris gateway setup  # Set up messaging platforms
Iris config set     # Set individual config values
Iris setup          # Or run the full setup wizard to configure everything at once
```

---

## Prerequisites

The only prerequisite is **Git**. The installer automatically handles everything else:

- **uv** (fast Python package manager)
- **Python 3.11** (via uv, no sudo needed)
- **Node.js v22** (for browser automation and WhatsApp bridge)
- **ripgrep** (fast file search)
- **ffmpeg** (audio format conversion for TTS)

:::info
You do **not** need to install Python, Node.js, ripgrep, or ffmpeg manually. The installer detects what's missing and installs it for you. Just make sure `git` is available (`git --version`).
:::

---

## Manual Installation

If you prefer full control over the installation process, follow these steps.

### Step 1: Clone the Repository

Clone with `--recurse-submodules` to pull the required submodules:

```bash
git clone --recurse-submodules https://github.com/Metaxis Research/iris-agent.git
cd iris-agent
```

If you already cloned without `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

### Step 2: Install uv & Create Virtual Environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv with Python 3.11 (uv downloads it if not present — no sudo needed)
uv venv venv --python 3.11
```

:::tip
You do **not** need to activate the venv to use `Iris`. The entry point has a hardcoded shebang pointing to the venv Python, so it works globally once symlinked.
:::

### Step 3: Install Python Dependencies

```bash
# Tell uv which venv to install into
export VIRTUAL_ENV="$(pwd)/venv"

# Install with all extras
uv pip install -e ".[all]"
```

If you only want the core agent (no Telegram/Discord/cron support):
```bash
uv pip install -e "."
```

<details>
<summary><strong>Optional extras breakdown</strong></summary>

| Extra | What it adds | Install command |
|-------|-------------|-----------------|
| `all` | Everything below | `uv pip install -e ".[all]"` |
| `messaging` | Telegram & Discord gateway | `uv pip install -e ".[messaging]"` |
| `cron` | Cron expression parsing for scheduled tasks | `uv pip install -e ".[cron]"` |
| `cli` | Terminal menu UI for setup wizard | `uv pip install -e ".[cli]"` |
| `modal` | Modal cloud execution backend | `uv pip install -e ".[modal]"` |
| `tts-premium` | ElevenLabs premium voices | `uv pip install -e ".[tts-premium]"` |
| `pty` | PTY terminal support | `uv pip install -e ".[pty]"` |
| `honcho` | AI-native memory (Honcho integration) | `uv pip install -e ".[honcho]"` |
| `mcp` | Model Context Protocol support | `uv pip install -e ".[mcp]"` |
| `homeassistant` | Home Assistant integration | `uv pip install -e ".[homeassistant]"` |
| `slack` | Slack messaging | `uv pip install -e ".[slack]"` |
| `dev` | pytest & test utilities | `uv pip install -e ".[dev]"` |

You can combine extras: `uv pip install -e ".[messaging,cron]"`

</details>

### Step 4: Install Submodule Packages

```bash
# Terminal tool backend (required for terminal/command-execution)
uv pip install -e "./mini-swe-agent"

# RL training backend
uv pip install -e "./tinker-atropos"
```

Both are optional — if you skip them, the corresponding toolsets simply won't be available.

### Step 5: Install Node.js Dependencies (Optional)

Only needed for **browser automation** (Browserbase-powered) and **WhatsApp bridge**:

```bash
npm install
```

### Step 6: Create the Configuration Directory

```bash
# Create the directory structure
mkdir -p ~/.Iris/{cron,sessions,logs,memories,skills,pairing,hooks,image_cache,audio_cache,whatsapp/session}

# Copy the example config file
cp cli-config.yaml.example ~/.Iris/config.yaml

# Create an empty .env file for API keys
touch ~/.Iris/.env
```

### Step 7: Add Your API Keys

Open `~/.Iris/.env` and add at minimum an LLM provider key:

```bash
# Required — at least one LLM provider:
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Optional — enable additional tools:
FIRECRAWL_API_KEY=fc-your-key          # Web search & scraping (or self-host, see docs)
FAL_KEY=your-fal-key                   # Image generation (FLUX)
```

Or set them via the CLI:
```bash
Iris config set OPENROUTER_API_KEY sk-or-v1-your-key-here
```

### Step 8: Add `Iris` to Your PATH

```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/Iris" ~/.local/bin/Iris
```

If `~/.local/bin` isn't on your PATH, add it to your shell config:

```bash
# Bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc

# Zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc

# Fish
fish_add_path $HOME/.local/bin
```

### Step 9: Configure Your Provider

```bash
Iris model       # Select your LLM provider and model
```

### Step 10: Verify the Installation

```bash
Iris version    # Check that the command is available
Iris doctor     # Run diagnostics to verify everything is working
Iris status     # Check your configuration
Iris chat -q "Hello! What tools do you have available?"
```

---

## Quick-Reference: Manual Install (Condensed)

For those who just want the commands:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone & enter
git clone --recurse-submodules https://github.com/Metaxis Research/iris-agent.git
cd iris-agent

# Create venv with Python 3.11
uv venv venv --python 3.11
export VIRTUAL_ENV="$(pwd)/venv"

# Install everything
uv pip install -e ".[all]"
uv pip install -e "./mini-swe-agent"
uv pip install -e "./tinker-atropos"
npm install  # optional, for browser tools and WhatsApp

# Configure
mkdir -p ~/.Iris/{cron,sessions,logs,memories,skills,pairing,hooks,image_cache,audio_cache,whatsapp/session}
cp cli-config.yaml.example ~/.Iris/config.yaml
touch ~/.Iris/.env
echo 'OPENROUTER_API_KEY=sk-or-v1-your-key' >> ~/.Iris/.env

# Make Iris available globally
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/Iris" ~/.local/bin/Iris

# Verify
Iris doctor
Iris
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Iris: command not found` | Reload your shell (`source ~/.bashrc`) or check PATH |
| `API key not set` | Run `Iris model` to configure your provider, or `Iris config set OPENROUTER_API_KEY your_key` |
| Missing config after update | Run `Iris config check` then `Iris config migrate` |

For more diagnostics, run `Iris doctor` — it will tell you exactly what's missing and how to fix it.
