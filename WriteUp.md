# Audio Submission Pipeline & Unreal Game Audio Standards

**Unit Name:** Interactive Audio & Technical Implementation

**Student Name:** Zoe Efstathiou

**Student ID:** 2423029

**User Guide Link:** [here](https://github.com/princessbleach/discord-sound-bot/blob/main/UserManual.md)

**Developer Guide Link:** [here](https://github.com/princessbleach/discord-sound-bot/blob/main/DeveloperManual.Md)

**Video Demonstration Link:** [here](https://github.com/princessbleach/discord-sound-bot/blob/main/audiobotdemonstration.mov)

---

## Abstract

This project explores the design and implementation of an automated audio submission pipeline for a game development workflow using Discord, Git, and Unreal Engine–compatible audio standards. The primary goal was to streamline how musicians upload sound assets while ensuring files meet technical, structural, and mastering requirements suitable for real-time game audio.

The system integrates a Discord slash-command bot that validates uploaded WAV files, structures metadata, and commits assets directly to a shared GitHub repository. Alongside the technical tool, a set of game-appropriate mastering and naming conventions was researched and defined to maintain consistency, performance, and mix clarity inside Unreal Engine.

---

## Research 

### What sources or references have you identified as relevant to this task?

Research focused on three intersecting areas:

* **Game audio technical standards** (sample rate, loudness philosophy, asset preparation)
* **Industry middleware and engine workflows** (Unreal, Wwise, FMOD)
* **Practical collaboration pipelines** (Git, automation, Discord integration)

The research directly informed:

* File format and mastering rules
* Naming conventions for scalable asset libraries
* Automation workflow design for collaborative development

---

### Sources

#### 1. Unreal Engine Audio Documentation (Epic Games)

Epic Games provides official documentation describing supported audio formats, import settings, and runtime mixing behaviour within Unreal Engine.

**Key findings:**

* Unreal expects 48 kHz WAV for optimal playback.
* Mono files are preferred for spatialised sounds.



From this research, I created a short document on how to use this tool (to be read by designers and musicians). This ensures that they submit files which are to the industry standard. This document can be found [here]

---

## Implementation 

### What was your development process and how did decisions evolve?

Development began with defining the core problem: musicians who are untrained in Git needed a pathway to submit audio assets. Early ideation explored manual Git uploads, but this proved error-prone and inconsistent.

The solution evolved into a Discord-based automation system:

1. User submits audio via slash command.
2. Bot validates format and size.
3. File is stored in structured folders.
4. Git commit and push occur automatically.

---

### What creative or technical methods did you try?

* Discord automation as a studio pipeline tool
* Git-based asset ingestion rather than cloud storage
* Applying interactive audio mastering philosophy instead of music streaming norms



---

## Testing 

### What testing methods did you use?

Testing combined:

* Internal functional testing of upload automation
* Peer testing for usability and clarity


Primary goals:

* Confirm reliable uploads
* Prevent invalid audio formats
* Ensure repository integrity

Testing confirmed the system successfully:

* Accepts only valid WAV files
* Generates metadata correctly
* Pushes assets to GitHub without manual intervention

| Tester | Platform | Device Specs | Test Type | Bugs Found | Avg. FPS | Severity | Repro Steps | Feedback                        |
| ------ | -------- | ------------ | --------- | ---------- | -------- | -------- | ----------- | ------------------------------- |
| Dev    | macOS    | M1 Air       | Internal  | 2          | N/A      | 2        | Yes         | Git LFS misconfigured initially |
| Peer   | Windows  | i5 / 16GB    | Peer      | 1          | N/A      | 2        | Yes         | Upload UX clear                 |
| User   | macOS    | Intel        | External  | 2          | N/A      | 3        | Yes         | Naming rules needed clarity     |

*Figure 4: Functional testing summary.*

---

## Critical Reflection 

### What went well?

* Successful creation of a **fully automated audio pipeline**
* Alignment with **real game-audio workflow philosophy**
* Clear improvement in **collaborative asset management**

The project exceeded expectations by moving beyond theory into a **practical studio-style tool**.

---

### What could be improved or done differently next time?

Future improvements could include:

* Web-based upload interface
* Automated loudness analysis during submission
* Direct Unreal integration via editor scripting
* Git LFS embedded into the bot initially


---

## Bibliography

Epic Games (2024) *Unreal Engine Audio Documentation*.
Audiokinetic (2023) *Wwise Documentation*.
FMOD (2023) *FMOD Studio User Guide*.

---

## Declared Assets

The following elements were created or modified with AI assistance:

* Discord bot structural code
* Audio standards documentation wording
* Academic write-up formatting


---
