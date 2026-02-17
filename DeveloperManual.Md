# Developer Manual 



## 1. Overview

The Discord Audio Submission Bot is a Python-based automation tool that allows contributors to submit WAV audio assets via a Discord slash command. The bot validates the upload, saves it into the correct folder inside the Git repository, writes a metadata file, then runs `git add`, `git commit`, and `git push` to upload the asset to GitHub.

This supports a studio-style workflow by:

- enforcing a consistent submission method (`/submit_audio`)
- ensuring only valid `.wav` files are uploaded
- auto-sorting assets into category folders
- generating submission metadata per file
- committing/pushing assets to the repo automatically
- using a git lock to avoid collisions when multiple submissions happen at once

---

## 2. Features (Based on Current Code)

### Slash command
- Command: `/submit_audio`
- Parameters collected:
  - `contributor` (text)
  - `category` (dropdown: SFX / Foley / Voice Acting / Composition)
  - `title` (text)
  - `file` (Discord attachment)
  - `notes` (optional text)

### Validation
- File extension allowed: `.wav` only (`ALLOWED_EXTS`)
- File size limit: `MAX_FILE_BYTES = 25MB`
- Optional channel restriction:
  - if `SUBMISSION_CHANNEL_ID != 0`, bot rejects submissions outside that channel

### Output + Git automation
- Saves WAV into the correct folder based on category
- Creates a `.txt` metadata file alongside the WAV
- Runs:
  - `git add`
  - `git commit`
  - `git push`
- Uses an `asyncio.Lock()` (`bot.git_lock`) to prevent Git collisions

---

## 3. Folder Structure & Routing

### Game repo target folders (current config)

```text
DropOff/
  Sound/
    Sfx/
    Foley/
    VoiceActing/
    Music/
```

### Category routing table (current code)

- `SFX` → `DropOff/Sound/Sfx`
- `Foley` → `DropOff/Sound/Foley`
- `Voice Acting` → `DropOff/Sound/VoiceActing`
- `Composition` → `DropOff/Sound/Music`

This is controlled in:

```python
CATEGORY_TO_FOLDER = {
    "SFX": REPO_PATH / "DropOff" / "Sound" / "Sfx",
    "Foley": REPO_PATH / "DropOff" / "Sound" / "Foley",
    "Voice Acting": REPO_PATH / "DropOff" / "Sound" / "VoiceActing",
    "Composition": REPO_PATH / "DropOff" / "Sound" / "Music",
}
```

---

## 4. File Naming & Metadata

### Output filename format (current code)

```text
{contributor}__{title}__{timestamp}.wav
```

- `contributor` and `title` are slugged to lowercase, underscores, and safe characters
- timestamp format: `YYYYMMDD_HHMMSS` (UTC)

Example:

```text
zoe__ui_click_01__20260217_153522.wav
```

### Metadata file
For each WAV, the bot creates a `.txt` file next to it:

```text
zoe__ui_click_01__20260217_153522.wav.txt
```

Metadata content includes:

- contributor
- asset title
- category
- Discord user + user ID
- original filename
- notes

---

## 5. Configuration

### Environment variables (required)

The bot reads configuration from a `.env` file:

```env
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
GITHUB_REPO_PATH=/absolute/path/to/your/game-repo
SUBMISSION_CHANNEL_ID=0
```

**Variables:**
- `DISCORD_TOKEN` — required; Discord bot token
- `GITHUB_REPO_PATH` — required; absolute path to the **local clone of the game repo**
- `SUBMISSION_CHANNEL_ID` — optional; set to `0` to allow in any channel, or set to a channel ID to restrict uploads

---

## 6. Dependencies

### Python
- Python 3.9+ recommended

### Python packages
Create `requirements.txt`:

```text
discord.py>=2.3.2
python-dotenv>=1.0.1
```

Install:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

---

## 7. GitHub & Git LFS Requirements

Because WAV files are large binary assets, the machine running the bot must have:

- Git installed
- Git LFS installed and initialised

### macOS (Homebrew)

```bash
brew install git-lfs
git lfs install
```

### Ubuntu

```bash
sudo apt update
sudo apt install git-lfs
git lfs install
```

---

## 8. GitHub Authentication

The bot **does not store GitHub credentials**.  
Authentication is handled by the local Git configuration on the machine running the bot.

Recommended authentication method: **SSH**

### Create SSH key (macOS)

```bash
ssh-keygen -t ed25519 -C "discord-sound-bot"
pbcopy < ~/.ssh/id_ed25519.pub
```

Add the key to:

GitHub → Settings → SSH and GPG keys → New SSH Key

### Ensure repo remote uses SSH

Inside the **game repo**:

```bash
git remote -v
git remote set-url origin git@github.com:USERNAME/REPO.git
```

---

## 9. Running the Bot Locally

From the bot folder:

```bash
source venv/bin/activate
python3 discordsoundbot.py
```

Expected startup output:

- repo path printed
- category mappings printed
- “Logged in as …”
- “Synced … slash command(s)”

---

## 10. Common Errors & Fixes

### `git-lfs: command not found`
Cause: Git LFS not installed on the machine running the bot.  
Fix:

```bash
brew install git-lfs
git lfs install
```

### `remote end hung up unexpectedly`
Often follows the LFS error above, or indicates auth/network issues.  
Fix:
- install Git LFS
- confirm SSH auth works:
  ```bash
  ssh -T git@github.com
  ```

### `Missing DISCORD_TOKEN in .env`
Cause: `.env` not present or token missing.  
Fix: create `.env` in the bot folder and add `DISCORD_TOKEN=`.

### Slash command not updating
Cause: Discord command cache.  
Fix:
- restart bot
- wait ~60 seconds
- try again

---

## 11. Concurrency Safety

The code uses:

```python
bot.git_lock = asyncio.Lock()
```

This prevents overlapping `git add/commit/push` operations when multiple submissions occur at once, avoiding repository conflicts and partial pushes.

---

## 12. Security Notes

- `.env` must be ignored via `.gitignore`
- Never commit Discord tokens
- Consider restricting who can submit (future improvement: role checks)
- Keep the game repo clone on the server private and permissioned correctly

---

## Declared Assets

The following elements were created or modified with AI assistance:

* Discord bot structural code
* Audio standards documentation wording
* Academic write-up formatting


---


