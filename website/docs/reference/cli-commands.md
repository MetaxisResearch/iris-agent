---
sidebar_position: 1
title: "CLI Commands Reference"
description: "Comprehensive reference for all Iris CLI commands and slash commands"
---

# CLI Commands Reference

## Terminal Commands

These are commands you run from your shell.

### Core Commands

| Command | Description |
|---------|-------------|
| `Iris` | Start interactive chat (default) |
| `Iris chat -q "Hello"` | Single query mode (non-interactive) |
| `Iris chat --continue` / `-c` | Resume the most recent session |
| `Iris chat -c "my project"` | Resume a session by name (latest in lineage) |
| `Iris chat --resume <id>` / `-r <id>` | Resume a specific session by ID or title |
| `Iris chat --model <name>` | Use a specific model |
| `Iris chat --provider <name>` | Force a provider (`Metaxis`, `openrouter`, `zai`, `kimi-coding`, `minimax`, `minimax-cn`) |
| `Iris chat --toolsets "web,terminal"` / `-t` | Use specific toolsets |
| `Iris chat --verbose` | Enable verbose/debug output |
| `Iris --worktree` / `-w` | Start in an isolated git worktree (for parallel agents) |
| `Iris --checkpoints` | Enable filesystem checkpoints before destructive file operations |

### Provider & Model Management

| Command | Description |
|---------|-------------|
| `Iris model` | Switch provider and model interactively |
| `Iris login` | OAuth login to a provider (use `--provider` to specify) |
| `Iris logout` | Clear provider authentication |

### Configuration

| Command | Description |
|---------|-------------|
| `Iris setup` | Full setup wizard — configures provider, model, terminal, and messaging all at once |
| `Iris config` | View current configuration |
| `Iris config edit` | Open config.yaml in your editor |
| `Iris config set KEY VAL` | Set a specific value |
| `Iris config check` | Check for missing config (useful after updates) |
| `Iris config migrate` | Interactively add missing options |
| `Iris tools` | Interactive tool configuration per platform |
| `Iris status` | Show configuration status (including auth) |
| `Iris doctor` | Diagnose issues |

### Maintenance

| Command | Description |
|---------|-------------|
| `Iris update` | Update to latest version |
| `Iris uninstall` | Uninstall (can keep configs for later reinstall) |
| `Iris version` | Show version info |

### Gateway (Messaging + Cron)

| Command | Description |
|---------|-------------|
| `Iris gateway` | Run gateway in foreground |
| `Iris gateway setup` | Configure messaging platforms interactively |
| `Iris gateway install` | Install as system service (Linux/macOS) |
| `Iris gateway start` | Start the service |
| `Iris gateway stop` | Stop the service |
| `Iris gateway restart` | Restart the service |
| `Iris gateway status` | Check service status |
| `Iris gateway uninstall` | Uninstall the system service |
| `Iris whatsapp` | Pair WhatsApp via QR code |

### Skills

| Command | Description |
|---------|-------------|
| `Iris skills browse` | Browse all available skills with pagination (official first) |
| `Iris skills search <query>` | Search skill registries |
| `Iris skills install <identifier>` | Install a skill (with security scan) |
| `Iris skills inspect <identifier>` | Preview before installing |
| `Iris skills list` | List installed skills |
| `Iris skills list --source hub` | List hub-installed skills only |
| `Iris skills audit` | Re-scan all hub skills |
| `Iris skills uninstall <name>` | Remove a hub skill |
| `Iris skills publish <path> --to github --repo owner/repo` | Publish a skill |
| `Iris skills snapshot export <file>` | Export skill config |
| `Iris skills snapshot import <file>` | Import from snapshot |
| `Iris skills tap add <repo>` | Add a custom source |
| `Iris skills tap remove <repo>` | Remove a source |
| `Iris skills tap list` | List custom sources |

### Cron & Pairing

| Command | Description |
|---------|-------------|
| `Iris cron list` | View scheduled jobs |
| `Iris cron status` | Check if cron scheduler is running |
| `Iris cron tick` | Manually trigger a cron tick |
| `Iris pairing list` | View pending + approved users |
| `Iris pairing approve <platform> <code>` | Approve a pairing code |
| `Iris pairing revoke <platform> <user_id>` | Remove user access |
| `Iris pairing clear-pending` | Clear all pending pairing requests |

### Sessions

| Command | Description |
|---------|-------------|
| `Iris sessions list` | Browse past sessions (shows title, preview, last active) |
| `Iris sessions rename <id> <title>` | Set or change a session's title |
| `Iris sessions export <id>` | Export a session |
| `Iris sessions delete <id>` | Delete a specific session |
| `Iris sessions prune` | Remove old sessions |
| `Iris sessions stats` | Show session statistics |

### Insights

| Command | Description |
|---------|-------------|
| `Iris insights` | Show usage analytics for the last 30 days |
| `Iris insights --days 7` | Analyze a custom time window |
| `Iris insights --source telegram` | Filter by platform |

---

## Slash Commands (Inside Chat)

Type `/` in the interactive CLI to see an autocomplete dropdown.

### Navigation & Control

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/quit` | Exit the CLI (aliases: `/exit`, `/q`) |
| `/clear` | Clear screen and reset conversation |
| `/new` | Start a new conversation |
| `/reset` | Reset conversation only (keep screen) |

### Tools & Configuration

| Command | Description |
|---------|-------------|
| `/tools` | List all available tools |
| `/toolsets` | List available toolsets |
| `/model [provider:model]` | Show or change the current model (supports `provider:model` syntax to switch providers) |
| `/provider` | Show available providers with auth status |
| `/config` | Show current configuration |
| `/prompt [text]` | View/set custom system prompt |
| `/personality [name]` | Set a predefined personality |
| `/reasoning [arg]` | Manage reasoning effort and display. Args: effort level (`none`, `low`, `medium`, `high`, `xhigh`) or display toggle (`show`, `hide`). No args shows current state. |

### Conversation

| Command | Description |
|---------|-------------|
| `/history` | Show conversation history |
| `/retry` | Retry the last message |
| `/undo` | Remove the last user/assistant exchange |
| `/save` | Save the current conversation |
| `/compress` | Manually compress conversation context |
| `/title [name]` | Set or show the current session's title |
| `/usage` | Show token usage for this session |
| `/insights [--days N]` | Show usage insights and analytics (last 30 days) |

#### /compress

Manually triggers context compression on the current conversation. This summarizes middle turns of the conversation while preserving the first 3 and last 4 turns, significantly reducing token count. Useful when:

- The conversation is getting long and you want to reduce costs
- You're approaching the model's context limit
- You want to continue the conversation without starting fresh

Requirements: at least 4 messages in the conversation. The configured model (or `compression.summary_model` from config) is used to generate the summary. After compression, the session continues seamlessly with the compressed history.

Reports the result as: `Compressed: X → Y messages, ~N → ~M tokens`.

:::tip
Compression also happens automatically when approaching context limits (configurable via `compression.threshold` in `config.yaml`). Use `/compress` when you want to trigger it early.
:::

### Media & Input

| Command | Description |
|---------|-------------|
| `/paste` | Check clipboard for an image and attach it (see [Vision & Image Paste](/docs/user-guide/features/vision)) |

### Skills & Scheduling

| Command | Description |
|---------|-------------|
| `/cron` | Manage scheduled tasks |
| `/skills` | Browse, search, install, inspect, or manage skills |
| `/platforms` | Show gateway/messaging platform status |
| `/verbose` | Cycle tool progress: off → new → all → verbose |
| `/<skill-name>` | Invoke any installed skill |

### Gateway-Only Commands

These work in messaging platforms (Telegram, Discord, Slack, WhatsApp) but not the interactive CLI:

| Command | Description |
|---------|-------------|
| `/stop` | Stop the running agent (no follow-up message) |
| `/sethome` | Set this chat as the home channel |
| `/status` | Show session info |
| `/reload-mcp` | Reload MCP servers from config |
| `/rollback` | List filesystem checkpoints for the current directory |
| `/rollback <N>` | Restore files to checkpoint #N |
| `/update` | Update Iris Agent to the latest version |

---

## Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Alt+Enter` / `Ctrl+J` | New line (multi-line input) |
| `Alt+V` | Paste image from clipboard (see [Vision & Image Paste](/docs/user-guide/features/vision)) |
| `Ctrl+V` | Paste text + auto-check for clipboard image |
| `Ctrl+C` | Clear input/images, interrupt agent, or exit (contextual) |
| `Ctrl+D` | Exit |
| `Tab` | Autocomplete slash commands |

:::tip
Commands are case-insensitive — `/HELP` works the same as `/help`.
:::

:::info Image paste keybindings
`Alt+V` works in most terminals but **not** in VSCode's integrated terminal (VSCode intercepts Alt+key combos). `Ctrl+V` only triggers an image check when the clipboard also contains text (terminals don't send paste events for image-only clipboard). The `/paste` command is the universal fallback. See the [full compatibility table](/docs/user-guide/features/vision#platform-compatibility).
:::
