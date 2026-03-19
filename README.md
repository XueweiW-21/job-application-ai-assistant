# Job Application AI Assistant

An AI assistant for the full job application lifecycle, built as [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills. It learns your background from your documents, then helps you analyze job postings, tailor resumes, write cover letters, and prepare for interviews.

**What makes this different from other AI resume tools:**

- **It learns you first.** You build a structured materials package (resume, bio, skills inventory, projects) that all skills draw from. The more context it has, the better every output gets.
- **It won't make things up.** Every claim in a generated resume, cover letter, or interview answer must trace to your real experience. Gaps are surfaced honestly, not papered over.
- **It's just markdown files.** No Docker, no API keys beyond Claude, no browser automation. Drop the skills into Claude Code and go.

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/YOUR_USERNAME/job-application-ai-assistant.git
cd job-application-ai-assistant
cp profile.example.yml profile.yml
# Edit profile.yml with your name, contact info, and links
```

### 2. Build your materials

Open Claude Code in this directory and run:

```
/setup
```

Upload your existing resumes, cover letters, or LinkedIn PDF. The setup skill extracts your experience into structured files. You can start applying immediately, or run `/setup deepen` later to add more detail.

### 3. Analyze a job posting

Paste a JD URL or text into the chat. The assistant will ask if you want to run `/jd-analyze`. If the fit is strong, it automatically tailors your resume.

### 4. Optional: DOCX generation

If you want `.docx` resume output:

```bash
python -m venv .venv
.venv/Scripts/activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install python-docx pyyaml
```

Place a `.docx` template in `.claude/skills/resume-tailor/templates/`.

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

See `materials/examples/` for a complete example using a fictional data scientist.

## CLI vs Web Chat

**Claude Code CLI (recommended):** Full pipeline experience. Skills chain automatically, files persist between sessions, tracker updates silently.

**Claude Web Chat:** You can copy skill instructions into a web chat and use them individually. But you lose file persistence, auto-triggering, and the tracker. You'll need to manage files manually.

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
