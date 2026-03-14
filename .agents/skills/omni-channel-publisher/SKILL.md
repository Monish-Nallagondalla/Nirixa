---
name: omni-channel-publisher
description: Automates platform-native publishing mechanics for X.com (Twitter) and LinkedIn. Enforces character count limits, auto-compiles multi-slide PDFs for LinkedIn, validates 4-image grid/threads for X, and generates explicit Document Titles upfront.
---

# Omni-Channel Publisher Skill (`omni-channel-publisher`)

Use this skill whenever drafting or packaging content for X.com (Twitter), LinkedIn, Medium, or newsletters.

## Platform Rules & Nuance Validation

### 1. X.com (Twitter) Validation
- **Character Count Rule**: Standard tweets MUST be under **280 characters** (including spaces). Always output character count validation.
- **Multi-Slide Visuals**: X does NOT render PDFs. Multi-slide visual assets MUST be formatted as **1 to 4 PNG image attachments** (`[post-X-slide-1.png]`).
- **Thread Formatting**: If the narrative requires > 280 characters, it MUST be structured as an explicit thread: `1/N: [Tweet 1 < 280 chars]`, `2/N: [Tweet 2 < 280 chars]`.

### 2. LinkedIn Validation
- **Document Carousels**: Multi-slide visuals MUST ALWAYS be automatically compiled into a single multi-page PDF document (`post-X-carousel.pdf`) using Python (`PIL` / `Pillow`). Never present separate image arrays for LinkedIn carousels.
- **Document Title**: ALWAYS provide an explicit, high-converting **LinkedIn Document Title** upfront (e.g. `The 3 AM Production Incident: Chatbots vs. Event-Driven AI`).
- **Character Limit**: Maximum 3,000 characters. First 3 lines before "...see more" must contain a pattern-interrupt hook.

### 3. Execution Pipeline
1. Check target platforms (LinkedIn, X.com, or both).
2. Validate text length against 280-char (X) and 3,000-char (LinkedIn) limits.
3. Automatically run Python script to build `post-X-carousel.pdf` for LinkedIn.
4. Output ready-to-publish bundles for both platforms in a single turn.
