# Gemini Auto-Sync & OpenCode Stabilization System

## Overview
This system enables **seamless, automated account switching** for Google Gemini within OpenCode, synchronized with an external quota-monitoring service.

## Components

### 1. Auto-Switcher Service
- **Source**: `~/gemini-auto-switch.py`
- **Service**: `gemini-auto-switch.service` (Systemd --user)
- **Logic**: Polls quotas for project `rosy-odyssey-86f3p` every 60 seconds. If a bucket falls below 10%, it triggers `~/gemini-switch.py` to rotate accounts.
- **Output**: Updates `~/.gemini/oauth_creds.json` with the new tokens.

### 2. OpenCode Gemini Plugin (Patched)
- **Location**: `~/.config/opencode/opencode-gemini-auth/`
- **Build**: Compiled to `dist/opencode-gemini-auth.js` and symlinked to `~/.config/opencode/plugin/opencode-gemini-auth.js`.
- **Patch**: `src/plugin.ts` was modified to include `loadAuthFromDisk` (see `src/plugin/file-auth.ts`).
- **Function**: Before **every** generative request, the plugin reads `~/.gemini/oauth_creds.json`. If the credentials on disk differ from OpenCode's internal state, it **immediately** uses the disk credentials.

## CRITICAL FOR FUTURE AI AGENTS
> [!IMPORTANT]
> **DO NOT RE-INSTALL the `opencode-gemini-auth` plugin via NPM.**
> Doing so will overwrite the `src/plugin.ts` patch and break the auto-switch synchronization. 
> Always work within the local repository at `~/.config/opencode/opencode-gemini-auth/` and rebuild with `bun build opencode-gemini-auth.ts --outdir dist --target node`.

## Troubleshooting
- **No Sync**: Check `journalctl -u opencode.service`. Look for `OAuth sync` debug messages (requires `isGeminiDebugEnabled` to be true in the code or config).
- **OOM Errors**: Several runaway PHP language server processes (`devsense.php.ls`) were identified as the cause of 10GB+ memory leaks. Terminate them if OOM issues return.
