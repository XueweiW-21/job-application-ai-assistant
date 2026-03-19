# Job Application AI Assistant

An AI assistant that learns your background, prepares everything from application materials to interview, and finds strengths you did not know you had. Built as [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills.

## Key Features

- **Learns you, not just your resume.** Builds a structured picture of your skills, voice, career arc, and writing style. Outputs sound like you.
- **Honest about gaps.** Tells you what is missing and how to frame what you do have. No fabrication, no false confidence.
- **Full lifecycle.** JD analysis, resume tailoring, cover letters, referral notes, application tracking, interview prep. All connected.
- **Portable.** Just markdown files. Works in Claude Code CLI, adaptable to web chat. No Docker, no browser automation.

## Overview

**Not just a resume tailor.** Feed it your resumes and past cover letters. It maps your experience against every job you look at, surfaces connections you missed ("your research lab work is exactly what this finance company calls alternative data"), and tells you honestly where the gaps are.

**Why this matters if you are job searching right now:** the hardest part is not writing a resume. It is seeing yourself clearly when you are stressed and second-guessing everything. This tool does that for you. The more you use it, the better it knows you.

## Privacy

All your personal data (resume, bio, skills, application outputs, tracker) stays on your machine. These files are gitignored and never leave your local directory. The only external calls are to the Claude API when you run skills, which is covered by Anthropic's [usage policy](https://www.anthropic.com/policies).

## Prerequisites

You need two things before starting:

1. **Claude Code** — install it by following the [official setup guide](https://docs.anthropic.com/en/docs/claude-code/getting-started). Claude Code is a CLI tool. If you have never used a terminal before, the setup guide walks you through it.
2. **An Anthropic account with API access** — Claude Code uses the Claude API, which requires either a paid API plan or a Claude Pro/Max subscription. Each full pipeline run (analyze a JD, tailor a resume, write a cover letter) typically costs a few cents in API usage. You can monitor your usage at [console.anthropic.com](https://console.anthropic.com/).

## Getting Started

### 1. Clone and configure

```bash
git clone https://github.com/XueweiW-21/job-application-ai-assistant.git
cd job-application-ai-assistant
```

Then copy the example profile to create your own:

- **macOS/Linux:** `cp profile.example.yml profile.yml`
- **Windows PowerShell:** `Copy-Item profile.example.yml profile.yml`

Open `profile.yml` in any text editor and fill in your name, contact info, and links.

### 2. Build your materials

Start Claude Code in this directory. Two ways:

- **VS Code:** Install the [Claude Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code), open this folder, and Claude Code appears in the sidebar.
- **Terminal:** Open a terminal, `cd` into this folder, and run `claude`.

Once Claude Code is running, type:

```
/setup
```

Upload your existing resumes, cover letters, or LinkedIn PDF. The setup skill extracts your experience into structured files. You can start applying immediately, or run `/setup deepen` later to add more detail.

### 3. Analyze a job posting

Paste a JD URL or text into the chat. The assistant will ask if you want to run `/jd-analyze`. If the fit is strong, it automatically tailors your resume.

### 4. Resume output formats

`/resume-tailor` always produces a `resume_tailored.md` file. This is the primary output. You can paste it directly into online application forms, or open it in any text editor for a final review before submitting.

**Optional: generate a DOCX file**

If you want a formatted `.docx` file to upload to company portals, set up the Python environment:

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Place a `.docx` template in `.claude/skills/resume-tailor/templates/` if you want custom formatting. Without a template, a clean default style is used.

**Why DOCX and not PDF?**

Most job portals accept DOCX and PDF equally, but many ATS (Applicant Tracking Systems) parse DOCX more reliably than PDF. The generator is built specifically for ATS compatibility: no headers or footers, no tables, no text boxes, plain paragraphs only. Once you have the DOCX and are happy with it, open it in Word or Google Docs and export to PDF for the final upload.

## Skills

| Skill | What it does |
|---|---|
| `/setup` | Build your materials package from uploaded documents |
| `/setup deepen` | Fill gaps in materials with targeted questions |
| `/jd-analyze` | Analyze a JD, score fit, identify gaps and keywords |
| `/resume-tailor` | Rewrite resume to mirror the JD (outputs .md + .docx) |
| `/cover-letter` | Write a cover letter grounded in JD and your experience |
| `/referral-note` | Write a third-person blurb for a referrer to forward |
| `/track` | Log and query applications in tracker.csv |
| `/interview-prep` | Generate interview prep calibrated to the round type |

## How the Pipeline Works

```
Paste a JD
    ↓
/jd-analyze scores fit
    ↓
Strong fit? → auto-tailors resume
Moderate/stretch? → asks you first
Mismatch? → tells you, stops
    ↓
Asks: want a cover letter?
Asks: have a referral?
    ↓
Application submitted
    ↓
Interview invite comes in
    ↓
/interview-prep generates round-specific prep
```

Every skill auto-updates `tracker.csv` so you always know where each application stands.

## Materials Structure

The materials folder is your personal knowledge base. All skills read from it.

```
materials/
├── resume_master.md      # Every role, every bullet (source of truth)
├── bio.md                # Career story, motivations, writing style
├── skills_inventory.md   # All skills with proficiency levels
├── papers/               # Publications, case studies, portfolio pieces
└── projects/             # Project details
```

See `materials/examples/` for a complete example using Michael Scott from *The Office* as a data scientist. The names and companies are obviously fictional so you can see exactly what real materials look like without anyone's actual data.

## CLI vs Web Chat

**Claude Code CLI (recommended):** This is the intended experience. Skills chain automatically (JD analysis triggers resume tailoring, which prompts for a cover letter), files persist between sessions, and the tracker updates silently in the background.

**Claude Web Chat:** You can adapt individual skills for use in web chat by copying the contents of a SKILL.md file into your conversation as context. However, this is a manual process: you lose automatic skill chaining, file persistence, and the tracker. Each skill would need to be run independently, and you would manage files yourself. This path works if you only need one skill occasionally, but for a full application pipeline, the CLI is significantly smoother.

## Configuration

All personal settings live in `profile.yml`:

```yaml
name: "Your Name"
email: "you@email.com"
phone: "(555) 123-4567"
location: "City, State"
links:
  LinkedIn: "https://linkedin.com/in/you"
  GitHub: "https://github.com/you"
font: "Times New Roman"
writing_rules:
  - "No hyphens or dashes in generated text"
target_roles:
  - "Data Scientist"
```

This file is gitignored. Your data stays local.

## Credits

- Reframing strategies (Keyword Alignment, Emphasis Shift, Abstraction Level Adjustment, Scale Emphasis) adapted from [varunr89/resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill)
- Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by [Anthropic](https://www.anthropic.com/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug fixes, skill improvements, and example materials for new domains are welcome.

## License

MIT
