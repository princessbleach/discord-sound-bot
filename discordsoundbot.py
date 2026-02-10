import os
import re
import asyncio
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
REPO_PATH = Path(os.getenv("GITHUB_REPO_PATH", ".")).resolve()
SUBMISSION_CHANNEL_ID = int(os.getenv("SUBMISSION_CHANNEL_ID", "0"))

# ✅ EDIT THESE to match your actual game repo folders
CATEGORY_TO_FOLDER = {
    "SFX": REPO_PATH / "DropOff" / "Sound" / "Sfx",
    "Foley": REPO_PATH / "DropOff" / "Sound" / "Foley",
    "Voice Acting": REPO_PATH / "DropOff" / "Sound" / "VoiceActing",
    "Composition": REPO_PATH / "DropOff" / "Sound" / "Music",
}

ALLOWED_EXTS = {".wav"}

MAX_FILE_BYTES = 25 * 1024 * 1024  # 25MB


def safe_slug(text: str) -> str:
    """Filesystem-friendly name."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9_\- ]+", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:80] if text else "untitled"


async def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str]:
    """Run a command without blocking the event loop."""
    def _run():
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return p.returncode, p.stdout

    return await asyncio.to_thread(_run)


async def git(*args: str) -> tuple[int, str]:
    return await run_cmd(["git", *args], REPO_PATH)


async def ensure_repo_ok() -> tuple[bool, str]:
    if not REPO_PATH.exists():
        return False, f"Repo path not found: {REPO_PATH}"

    code, out = await git("rev-parse", "--is-inside-work-tree")
    if code != 0 or "true" not in out:
        return False, f"Not a git repo at: {REPO_PATH}\n{out}"

    return True, ""


def build_dest_paths(category: str, contributor_name: str, asset_title: str, ext: str) -> tuple[Path, Path]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    contributor = safe_slug(contributor_name)
    title = safe_slug(asset_title)

    dest_dir = CATEGORY_TO_FOLDER[category]
    dest_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{contributor}__{title}__{stamp}{ext}"
    dest_path = dest_dir / filename
    meta_path = dest_path.with_suffix(dest_path.suffix + ".txt")
    return dest_path, meta_path


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id={bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print("❌ Command sync failed:", e)


@bot.tree.command(
    name="submit_audio",
    description="Submit an audio asset to the game repo (commits + pushes to GitHub)."
)
@app_commands.describe(
    contributor="Contributor name (musician/voice actor/composer/etc.)",
    category="Type of audio",
    title="Asset title (e.g., UI_Click_01)",
    file="Upload the audio file here",
    notes="Optional notes / context"
)
@app_commands.choices(category=[
    app_commands.Choice(name="SFX", value="SFX"),
    app_commands.Choice(name="Foley", value="Foley"),
    app_commands.Choice(name="Voice Acting", value="Voice Acting"),
    app_commands.Choice(name="Composition", value="Composition"),
])
async def submit_audio(
    interaction: discord.Interaction,
    contributor: str,
    category: app_commands.Choice[str],
    title: str,
    file: discord.Attachment,
    notes: Optional[str] = ""
):
    # Optional channel restriction
    if SUBMISSION_CHANNEL_ID and interaction.channel_id != SUBMISSION_CHANNEL_ID:
        return await interaction.response.send_message(
            "Not in the submission channel. Use the designated audio submissions channel.",
            ephemeral=True
        )

    # Quick validation
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTS:
        return await interaction.response.send_message(
            f"File type `{ext}` not allowed.\nAllowed: {', '.join(sorted(ALLOWED_EXTS))}",
            ephemeral=True
        )

    if file.size and file.size > MAX_FILE_BYTES:
        return await interaction.response.send_message(
            f"That file is too big for this pipeline ({file.size/1024/1024:.1f}MB). "
            f"Max is {MAX_FILE_BYTES/1024/1024:.0f}MB.\n"
            f"Export a smaller version (game-ready) or we can switch to cloud-link submissions.",
            ephemeral=True
        )

    ok, reason = await ensure_repo_ok()
    if not ok:
        return await interaction.response.send_message(
            f"Repo setup error:\n```{reason[:1800]}```",
            ephemeral=True
        )

    await interaction.response.send_message("Uploading + committing… ✅", ephemeral=True)

    chosen_category = category.value
    dest_path, meta_path = build_dest_paths(chosen_category, contributor, title, ext)

    try:
        await file.save(dest_path)
    except Exception as e:
        return await interaction.followup.send(
            f"Failed to save attachment:\n```{str(e)[:1800]}```",
            ephemeral=True
        )

    meta_path.write_text(
        f"contributor: {contributor}\n"
        f"asset_title: {title}\n"
        f"category: {chosen_category}\n"
        f"submitted_by: {interaction.user} ({interaction.user.id})\n"
        f"original_filename: {file.filename}\n"
        f"notes: {notes or ''}\n",
        encoding="utf-8"
    )

    rel_audio = dest_path.relative_to(REPO_PATH)
    rel_meta = meta_path.relative_to(REPO_PATH)

    # Serialize git operations (prevents collisions if two people submit at once)
    if not hasattr(bot, "git_lock"):
        bot.git_lock = asyncio.Lock()

    async with bot.git_lock:
        code, out = await git("add", str(rel_audio), str(rel_meta))
        if code != 0:
            return await interaction.followup.send(
                f"Git add failed:\n```{out[:1800]}```",
                ephemeral=True
            )

        commit_msg = f"Add audio: {title} ({chosen_category})"
        code, out = await git("commit", "-m", commit_msg)
        if code != 0:
            return await interaction.followup.send(
                f"Git commit failed:\n```{out[:1800]}```",
                ephemeral=True
            )

        code, out = await git("push")
        if code != 0:
            return await interaction.followup.send(
                f"Git push failed:\n```{out[:1800]}```",
                ephemeral=True
            )

    folder_display = dest_path.parent.relative_to(REPO_PATH).as_posix()
    await interaction.followup.send(
        f"✅ Submitted **{dest_path.name}** → **{folder_display}/** (committed + pushed).",
        ephemeral=True
    )


def main():
    if not DISCORD_TOKEN:
        raise RuntimeError("Missing DISCORD_TOKEN in .env")

    print(f"Repo path: {REPO_PATH}")
    for k, p in CATEGORY_TO_FOLDER.items():
        print(f"{k} -> {p}")

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()

