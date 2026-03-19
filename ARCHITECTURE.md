# Job Application AI Assistant — Architecture

## Overview

A Claude Code skill suite that manages the full job application lifecycle: JD analysis, resume tailoring, cover letter writing, referral notes, application tracking, and interview prep. Built as interconnected skills that share context through structured personal materials and a CSV tracker.

---

## Directory Structure

```
job-application-ai-assistant/
├── .claude/
│   └── skills/
│       ├── setup/
│       │   └── SKILL.md
│       ├── jd-analyze/
│       │   └── SKILL.md
│       ├── resume-tailor/
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   │   └── generate_docx.py
│       │   └── templates/
│       │       └── (user's .docx template, gitignored)
│       ├── cover-letter/
│       │   └── SKILL.md
│       ├── referral-note/
│       │   └── SKILL.md
│       ├── track/
│       │   └── SKILL.md
│       └── interview-prep/
│           └── SKILL.md
│
├── materials/                        # Personal data (gitignored except examples/)
│   ├── examples/                     # Fictional example person (committed)
│   │   ├── resume_master.md
│   │   ├── bio.md
│   │   ├── skills_inventory.md
│   │   ├── papers/
│   │   └── projects/
│   ├── resume_master.md             # Your real data (gitignored)
│   ├── bio.md
│   ├── skills_inventory.md
│   ├── papers/
│   └── projects/
│
├── applications/                     # Per-application outputs (gitignored)
│   └── {Company}_{Role}_{JobID}_{YYYY-MM-DD}/
│       ├── jd_analysis.md
│       ├── resume_tailored.md
│       ├── {Name} Resume {YYYY-MM-DD}.docx
│       ├── cover_letter.md
│       ├── referral_note.md
│       └── interview_prep_{type}.md
│
├── profile.yml                       # Your config (gitignored)
├── profile.example.yml               # Template (committed)
├── tracker.csv                       # Application log (gitignored)
├── CLAUDE.md                         # Project instructions
├── ARCHITECTURE.md                   # This file
├── CONTRIBUTING.md
└── README.md
```

---

## Skill Flow

```
/setup (one-time onboarding)
      │
      ▼
  materials/ populated
      │
      ▼
/jd-analyze <url or text>
      │  auto-updates tracker.csv
      ▼
  jd_analysis.md
      │
      ├─ 🟢 Strong Fit ──────────────────► auto-run /resume-tailor
      │
      ├─ 🔵 🟡 ─────────────────────────► ask user: "proceed?"
      │
      └─ 🔴 Mismatch ───────────────────► stop, tell user not a good match
                                                    │
                                              user says yes
                                                    │
                                                    ▼
                                            /resume-tailor
                                      (auto-updates tracker.csv)
                                                    │
                                                    ▼
                                        resume.md + resume.docx
                                                    │
                                          ask: "Want a cover letter?"
                                                    │
                                    ┌── yes ─────────┴──── no ──┐
                                    ▼                            │
                             /cover-letter                       │
                       (auto-updates tracker.csv)               │
                                    │                            │
                                    └──────────┬─────────────────┘
                                               ▼
                              ask: "Do you have a referral?
                               Want a recommendation note?"
                                               │
                                         user says yes
                                               │
                                               ▼
                                     /referral-note
                                   referral_note.md

      ════════════ application submitted ════════════

      [interview invite received — user mentions it]
                                               │
                                               ▼
                                   /interview-prep <folder> <type>
                                    (auto-updates tracker.csv)
                                               │
                                               ▼
                                   interview_prep_{type}.md
```

---

## Skill Summaries

### `/setup`
Two modes: initial extraction from uploaded documents (resumes, cover letters, LinkedIn) into structured materials, and `/setup deepen` for targeted questions to fill gaps. Progressive onboarding — minimal effort to start, deeper investment pays off at interview stage.

### `/jd-analyze`
Foundation skill. Fetches JD, extracts Job ID for unique folder naming, scores requirements against materials, classifies fit tier (🟢/🔵/🟡/🔴). Outputs a structured match brief with gap analysis, reframing strategies, and cover letter angle.

### `/resume-tailor`
Rewrites Skills and Experience sections using four named reframing strategies (Keyword Alignment, Emphasis Shift, Abstraction Level Adjustment, Scale Emphasis). Generates .md + ATS-optimized .docx via python-docx script.

### `/cover-letter`
Opt-in. Writes a concise letter (250-350 words) grounded in JD priorities. Three pillars: hook (referral or strongest match), experience mapped to responsibilities, company connection. JD is primary source; web research is supplementary.

### `/referral-note`
Writes a 150-200 word third-person blurb for a referrer to forward. Professional tone, not the user's voice. Grounded in real experience and JD fit reasons.

### `/track`
CSV-based application tracker. Auto-updated silently by all other skills. Manual commands: add, update, list, summary. Follow-up dates auto-computed by status.

### `/interview-prep`
Generates round-specific prep documents calibrated to interview type (screening/HM/technical/behavioral/final) and interviewer role. Uses JD priority signals (repeated terms) to predict likely questions.

---

## Key Design Decisions

### Materials as source of truth
All skills read from `materials/` rather than asking the user to re-describe their experience each time. This creates a cumulative knowledge layer that improves with each `/setup deepen` session.

### profile.yml for personalization
User config (name, contact, links, font, writing rules) lives in a YAML file read by all skills and the docx generator. Keeps skills generic and shareable.

### Tracker as shared state
`tracker.csv` is updated silently by every skill, creating pipeline awareness without requiring manual logging.

### Honest constraints
The no-fabrication rule, transparent gap handling, and named reframing strategies (adapted from varunr89/resume-tailoring-skill) are embedded at the project level (CLAUDE.md), skill level, and quality-check level. Redundancy is intentional — rules stated once get ignored in long generations.
