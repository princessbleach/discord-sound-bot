# Audio Upload Standards  (for musicians)


**Format**

* WAV only
* 48 kHz sample rate
* 24-bit preferred (16-bit OK for SFX)
* Mono → SFX, Foley, Voice
* Stereo → Music, ambience

**Loudness**
Games are **mixed dynamically in-engine**, so:

* Avoid clipping or heavy limiting
  Final loudness is balanced inside Unreal, not in mastering.

**General Loudness Ranges (guidance, not strict rules)**

* **SFX / Foley:** roughly −20 to −14 LUFS, peak ≤ −1 dBFS
* **Voice:** roughly −23 to −16 LUFS, clean noise floor
* **Music:** wide range, keep dynamic and unclipped

**File Size Guidance**

* Short SFX/UI: keep under ~1 MB
* Foley/voice lines: keep under ~2–3 MB
* Music: keep under ~25 MB when possible
  Trim silence and use mono where appropriate.

**Naming Convention (important)**

```
soundname__type__contributor__v01.wav
```

Example:

```
footstep_grass_light__sfx__zoe__v01.wav
```

Rules:

* lowercase, underscores only
* clear descriptive names
* increment version numbers for updates