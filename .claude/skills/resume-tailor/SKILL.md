---
name: resume-tailor
description: Tailor resume Skills and Experience sections to mirror a specific JD analysis
argument-hint: "application folder name, e.g. Acme_DataScientist_R12345_2026-03-17"
---

# Resume Tailor

Rewrite the resume to mirror a specific JD while preserving factual accuracy and the user's voice.

## Input

The user provides an application folder name (e.g. `Acme_DataScientist_R12345_2026-03-17`).

## Step 1: Load Context

Read all of these before writing anything:

1. `profile.yml` — user's name, contact info, links, writing rules
2. `applications/{folder}/jd_analysis.md` — **required**. If missing, stop and tell the user to run `/jd-analyze` first.
3. `materials/resume_master.md` — source of truth for all experience
4. `materials/skills_inventory.md` — source of truth for all skills and proficiency levels
5. `materials/papers/*.md` — publication details
6. `materials/projects/*.md` — project details

From `jd_analysis.md`, extract:
- Must-have and nice-to-have requirements
- ATS keywords to mirror
- Resume tailoring notes (from the dedicated section)
- Role archetype and seniority signals
- Gaps identified

## Step 2: Rewrite Skills Summary

Rewrite the Skills Summary section:
- **Reorder categories** so the most JD-relevant category comes first
- **Reorder items within categories** so the most JD-relevant skills lead
- **Echo ATS keywords** — use the exact terms from the JD where they map to real skills in `skills_inventory.md`
- **Add learnable tool-specific languages** (e.g., Spark, SAS, Scala) only if:
  - They are syntactically close to a language the user already knows
  - They can be practiced in a short project before interviews
  - They are listed specifically to pass ATS screening
  - Mark them naturally in the list — do not flag them as "learning" on the resume itself
- **Never add a skill that has no basis** in `skills_inventory.md` or a close transferable equivalent

## Step 3: Rewrite Experience Sections

Read `experience_level` from `profile.yml` to calibrate bullet counts and page targets. If not set, estimate from the number of roles in `resume_master.md`.

For each role in `resume_master.md`:

### Bullet Selection

Bullet count per role depends on experience level:

| Level | Bullets per role | Notes |
|---|---|---|
| `new_grad` | All available (up to 4) | Every role matters. Include internships, research, and academic work. |
| `early_career` | 3 to 5 | Include all roles. Prioritize the most recent. |
| `mid_career` | 4 to 6 | Standard selection. Trim older roles. |
| `senior` | 4 to 6 | Standard selection. Early career roles only if JD-relevant. |

Prioritize bullets by:
  1. Bullets that directly address a must-have requirement from the JD
  2. Bullets that contain or can naturally echo ATS keywords
  3. Bullets that demonstrate skills marked as ⚠️ Partial in the fit assessment (to strengthen weak areas)
  4. Bullets with quantifiable outcomes or scale indicators
- Drop bullets that are irrelevant to this specific JD unless they show critical soft skills

### Bullet Reframing
- **Echo JD language** in the bullet phrasing where it maps to real experience
- **Lead with the JD-relevant framing**, then add the specific detail
- **Keep the user's voice**: read `materials/bio.md` Writing Style Notes for guidance
- **Preserve all facts**: dates, tools, outcomes, scale, team sizes — never change these
- **Apply writing rules** from `profile.yml`

Use the four named reframing strategies (drawn from the Resume Tailoring Notes in `jd_analysis.md`):
1. **Keyword Alignment:** swap the opening verb or noun to echo JD language exactly (e.g., "built" -> "engineered and deployed" when JD uses "deploy"). Apply to ATS-critical bullets.
2. **Emphasis Shift:** reorder clauses so the JD-relevant outcome leads and supporting detail follows. Apply when the original bullet buries the most relevant result.
3. **Abstraction Level Adjustment:** raise specificity (e.g., domain name -> "large-scale alternative datasets") or lower it (e.g., narrow tool -> broader method) to match the JD's vocabulary level. Apply when the user's language is more domain-specific than the JD expects.
4. **Scale Emphasis:** surface volume, throughput, or scope numbers prominently when the JD values operational scale. Apply when large-scale, production, or sole-maintainer context is relevant.

Each bullet should use at most one or two strategies. Do not stack all four on a single bullet.

### Early Career Roles
- For `new_grad` and `early_career`: include ALL roles. These are the user's primary experience, not filler.
- For `mid_career` and `senior`: include only if the JD analysis indicates relevance (research, academic, domain-specific). If included, limit to 2 to 3 bullets maximum. Later experience makes a stronger case for most JDs.

## Step 4: Select Publications / Portfolio

- If `materials/papers/` and `materials/projects/` are empty or contain no files, skip this section entirely. Do not include a Publications header with nothing under it.
- If publications or portfolio pieces exist, select the **2 to 4 most JD-relevant items**
- Relevance is determined by:
  - Methods used (does the piece demonstrate a required skill?)
  - Domain overlap (does the topic relate to the company/role domain?)
  - Impact (high-profile venues or outcomes carry weight for relevant roles)
- For non-research roles, these can be shortened to a compact list without summaries

## Step 5: Assemble the Resume

Output structure (markdown):

```markdown
# {Name from profile.yml}
{Contact line from profile.yml: email | phone | links}
{Location from profile.yml}

## Education
[Keep exactly as in resume_master.md — never modify education]

## Skills Summary
[Rewritten per Step 2]

## Experience
[Rewritten per Step 3 — keep chronological order, most recent first]

## Publications
[Selected per Step 4]
```

Target length depends on `experience_level` from `profile.yml`:

| Level | Target |
|---|---|
| `new_grad` | **1 page** strictly. Trim aggressively. Every line must earn its place. |
| `early_career` | **1 page**. Exceed only if the user has dense, relevant experience that cannot be cut without losing JD coverage. |
| `mid_career` | **1 to 2 pages**. Use judgment based on role count and JD relevance. |
| `senior` | **2 pages**. If content runs long, trim lower-priority bullets from older roles first. |

If `experience_level` is not set, default to 1 page for 2 or fewer roles, 2 pages for 3 or more.

## Step 6: Write Output

Save the tailored resume to:
```
applications/{folder}/resume_tailored.md
```

## Step 6b: Update Tracker

After writing the markdown (auto, silent):
- Find the row in `tracker.csv` where `folder` matches the current folder
- Set `resume_version` = `Yes` and `last_updated` = today
- If no row exists, create one (status = `analyzed`, fill what is available)

## Step 7: Generate DOCX

After writing the markdown, run the docx generation script. Read `profile.yml` for the user's name to construct the output filename `{Name} Resume {YYYY-MM-DD}.docx`:

```bash
# macOS/Linux:
.venv/bin/python .claude/skills/resume-tailor/scripts/generate_docx.py "applications/{folder}/resume_tailored.md" "applications/{folder}/{Name} Resume {YYYY-MM-DD}.docx"
# Windows:
.venv/Scripts/python.exe .claude/skills/resume-tailor/scripts/generate_docx.py "applications/{folder}/resume_tailored.md" "applications/{folder}/{Name} Resume {YYYY-MM-DD}.docx"
```

If the script fails (missing dependencies, etc.), tell the user and suggest they install requirements:
```bash
pip install -r requirements.txt
```

The `.md` version is the primary deliverable. The `.docx` is a convenience output.

## Step 8: Show Summary

After generating both files, display to the user:
- Which bullets were selected for each role (by count)
- Which publications were included
- Key reframing decisions made (so the user can review)
- Any gaps from the JD analysis that the resume cannot address (be transparent)
- File paths for both outputs

## Hard Rules

1. **Never fabricate experience.** Every bullet must trace to a real entry in `resume_master.md`. Reframe tone and emphasis, not facts.
2. **Never change job titles, company names, dates, or team sizes.**
3. **Apply writing rules from profile.yml** in all generated text.
4. **Be transparent about gaps.** If the JD requires something not in the materials, do not try to cover it by stretching a bullet beyond recognition. Note it in the summary.
5. **Programming language exception:** Languages tied to learnable tools (Spark, SAS, Scala, Julia) can be added to the skills list if there is a transferable basis. This is strictly for ATS. Do not add them to experience bullets.
6. **Preserve the user's voice.** Read `materials/bio.md` Writing Style Notes for guidance. No corporate padding, no buzzword stacking.

## Quality Checks Before Saving

- Every bullet in the output must have a corresponding source in `resume_master.md`
- Skills listed must exist in `skills_inventory.md` (or meet the learnable language exception)
- ATS keywords from `jd_analysis.md` should appear naturally in the resume (check coverage)
- Writing rules from `profile.yml` are applied throughout
- Contact info matches `profile.yml`
- Education is unchanged from source
