---
name: setup
description: Extract user materials from uploaded documents and optionally deepen thin areas with targeted questions
argument-hint: "or 'deepen' to fill gaps in existing materials"
---

# Setup

Build the personal materials package from uploaded documents. Two modes:

- **`/setup`** — initial extraction from resumes, cover letters, LinkedIn, etc.
- **`/setup deepen`** — targeted questions to fill gaps in existing materials

## Mode 1: Initial Setup

### Step 1: Collect Documents

Ask the user to provide whatever they have:
- Resume PDFs (multiple versions preferred — the union is richer than any single version)
- Cover letters they have written before
- LinkedIn profile (PDF export or URL)
- Portfolio links, published papers, project write-ups
- Personal website or blog

No minimum required. One resume is enough to start.

### Step 2: Extract into Materials

Parse all uploaded documents. Generate or update the following files:

**`materials/resume_master.md`**
- Merge all resume versions into one comprehensive file
- Deduplicate: keep the most detailed version of each bullet
- Preserve all roles, even those dropped from shorter resume versions
- Include: job title, company, dates, location, and all bullets for each role
- Maintain reverse chronological order

**`materials/skills_inventory.md`**
- Extract every skill mentioned across all documents
- Estimate proficiency from context:
  - Listed in skills section across multiple docs = likely proficient
  - Mentioned in experience bullets with specific outcomes = demonstrated
  - Mentioned once without context = noted but unclear proficiency
- Group by category (languages, frameworks, tools, methods, domain knowledge)

**`materials/bio.md`**
- Extract career narrative from cover letters and LinkedIn summary
- Capture how the user describes themselves in their own words
- Populate Writing Style Notes from actual writing samples: sentence length, vocabulary patterns, tone tendencies, any quirks (formal vs. casual, uses jargon vs. plain language)
- If only a resume is provided, leave bio.md as a minimal draft and flag it

**`materials/projects/*.md` and `materials/papers/*.md`**
- Create stub files for any projects, publications, or portfolio pieces mentioned in the documents
- Include whatever details are available (title, tools, outcome, description)
- Flag as stubs if details are thin

### Step 3: Classify Experience Level

After extracting materials, determine the user's experience level based on:
- Total years of professional experience (from earliest role to most recent)
- Number of distinct roles
- Whether they have publications, projects, or portfolio pieces

Write `experience_level` to `profile.yml`:

| Level | Criteria | Resume target |
|---|---|---|
| `new_grad` | 0-1 years experience, or only internships and academic roles | 1 page |
| `early_career` | 1-4 years experience, 1-2 full-time roles | 1 page |
| `mid_career` | 5-10 years experience, 2-4 roles | 1-2 pages |
| `senior` | 10+ years experience, or 4+ roles with significant scope | 2 pages |

If `experience_level` already exists in `profile.yml`, do not overwrite it. The user may have set it manually.

Tell the user what level was detected: "Based on your materials, I have set your experience level to {level}. This controls resume length and formatting. You can change it in profile.yml if it does not feel right."

### Step 4: Show Extraction Summary

Display what was extracted with gap indicators:

```
Materials extracted:

Experience level: {level} (resume target: {1 page / 1-2 pages / 2 pages})

resume_master.md — {N} roles found, {N} bullets total
  ✅ {Role} at {Company} ({N} bullets)
  ⚠️ {Role} at {Company} ({N} bullets — thin)

skills_inventory.md — {N} skills found
  ✅ {skills appearing in multiple docs}
  ⚠️ {skills mentioned once, proficiency unclear}

bio.md — {status: draft from cover letter / minimal from resume only}

projects/ — {N} stubs created
papers/ — {N} stubs created
```

### Step 5: Done — User Can Start Applying

Tell the user:
- They can run `/jd-analyze` on any job posting now
- Materials are sufficient for basic resume tailoring
- For stronger interview prep and cover letters, run `/setup deepen` anytime

This is the exit point. Do not push the user into Track 2.

---

## Mode 2: `/setup deepen`

Targeted questions to strengthen thin areas in existing materials. Can be run anytime, stopped anytime, and resumed later.

### Step 1: Scan Existing Materials

Read all files in `materials/`. Identify gaps:
- Roles with fewer than 4 bullets
- Skills listed without demonstrated context in any bullet
- Projects or papers that are stubs (title only, no technical details or outcomes)
- Missing or thin `bio.md` (no career narrative, no writing style notes)
- Skills inventory with unclear proficiency levels

### Step 2: Prioritize and Ask

Rank gaps by impact (roles with more years of experience and skills with more JD relevance matter more than internships or one-off tools).

Ask targeted, specific, answerable questions. Not generic career coaching. Examples:

**For thin roles:**
- "You were at {Company} for {N} years but I only have {N} bullets. What was your main project there?"
- "What tools or technologies did you use day to day?"
- "Did you work with any stakeholders outside your immediate team?"
- "What's a result you achieved there that you're proud of? Numbers help if you have them."

**For skills without context:**
- "You listed {Skill}. Was that in a production system or exploratory work? At what scale?"

**For stub projects/papers:**
- "Can you describe what problem {Project} solved, what you built, and what happened as a result?"

**For bio gaps:**
- "Why did you move from {Company A} to {Company B}?"
- "What kind of roles are you targeting now and why?"

### Step 3: Integrate Answers

After each answer, immediately update the relevant materials file. Show the user what was added:
- "Added 3 bullets to your {Company} role in resume_master.md"
- "Updated {Skill} proficiency to Proficient in skills_inventory.md"

The user can stop anytime. Progress is saved. They can run `/setup deepen` again later and it will pick up remaining gaps.

### Step 4: Summary

When the user is done (or wants to stop), show:
- What was strengthened
- What gaps remain
- Suggest: "These materials are strong enough for [resume tailoring / full analysis / interview prep]"

## Hard Rules

1. **Extract first, ask second.** Never ask the user to type something that was already in their documents.
2. **No fabrication.** Extraction must reflect what the documents say. If something is ambiguous, ask rather than assume.
3. **No pressure.** Track 2 is always optional. Never guilt the user into deepening.
4. **Incremental.** Every answer immediately improves the materials. There is no "you must finish the whole process" requirement.
5. **Universal schema.** The materials structure is the same regardless of domain. A designer's resume_master.md has the same format as an engineer's. Do not create domain-specific templates.
