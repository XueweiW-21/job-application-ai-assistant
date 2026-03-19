---
name: jd-analyze
description: Analyze a job description and produce a structured match brief with fit scores and gaps
argument-hint: "JD text, URL, or paste"
---

# JD Analyzer

Analyze the provided job description and produce a structured match brief.

## Instructions

1. If the user provides a URL, fetch the page content using WebFetch. If they paste text or attach a PDF, use that directly.
1b. **Extract Job ID from the JD.** Look for fields labeled "Job ID", "Req ID", "Requisition #", "Posting ID", "Job Ref", or similar (common formats: R-12345, JR123456, 12345). If found, use it in the folder name. If not found, generate a 6-character slug from the first letters of the role title and team/org name (e.g., "Data Scientist, Watson Health" -> "DSWH"). If no team is mentioned, use the first 6 consonants of the role title.
2. Read the following materials to assess fit:
   - `materials/resume_master.md`
   - `materials/skills_inventory.md`
   - `materials/bio.md` (elevator pitch and target roles)
   - Scan `materials/papers/*.md` and `materials/projects/*.md` for relevant experience
3. **Before writing anything to disk, do a fast fit screen:**
   - Count must-have requirements from the JD
   - Estimate how many are ✅ Strong, ⚠️ Partial, or ❌ Gap based on materials
   - Compute a preliminary fit tier (see Fit Tier definitions below)
   - Display the fit banner to the user immediately (see Banner format below)
   - **If fit tier is 🔴 Likely Mismatch: stop here.** Tell the user this is not a good match and not worth pursuing. Do not ask if they want to continue. Write only the fit banner to disk (no full analysis).
   - **If fit tier is 🟡 Stretch: tell the user** before proceeding and confirm they want the full analysis.
   - If fit tier is 🟢 or 🔵: proceed with full analysis.
4. Determine the output folder and check for collisions:
   - Folder name format: `applications/{Company}_{Role}_{JobID}_{YYYY-MM-DD}/`
   - Clean company name and role title for folder naming (no spaces, use underscores; truncate role to 3 words max)
   - Use the Job ID extracted in Step 1b
   - **Before creating the folder:** scan `applications/` for any existing folder containing the same Job ID. If found, warn the user: "A folder for Job ID {id} already exists at {existing_folder}. Do you want to overwrite it or create a new entry?" Do not proceed until the user confirms.
   - If no Job ID collision, create the folder and write `jd_analysis.md`
5. Update `tracker.csv` (auto, silent — do not interrupt the user):
   - If `tracker.csv` does not exist yet, create it with the full header row first
   - Header: `date_applied,company,role,folder,job_id,source,referral,fit_tier,status,interview_stage,next_interview_date,last_contact_date,follow_up_date,resume_version,cover_letter,notes,last_updated`
   - If a row for this folder already exists, update it: set `fit_tier`, `job_id`, `last_updated` to today's values
   - If no row exists, create one with: `date_applied` = today, `company`, `role`, `folder`, `job_id` from Step 1b, `fit_tier` from the banner, `status` = `analyzed`, `resume_version` = No, `cover_letter` = No, `last_updated` = today
6. After writing, display a brief summary to the user: company, role, overall fit assessment, and top 3 action items.

## Fit Tier Definitions

Score based on must-have requirements only:

| Tier | Emoji | Label | Criteria |
|---|---|---|---|
| 1 | 🟢 | Strong Fit | Fewer than 2 must-haves are ❌ Gap; majority are ✅ Strong |
| 2 | 🔵 | Moderate Fit | 2 to 3 must-haves are ❌ Gap; most partials are genuinely close |
| 3 | 🟡 | Stretch | 4 or more must-haves are ❌ Gap or ⚠️ Partial with thin evidence |
| 4 | 🔴 | Likely Mismatch | More than half of must-haves are ❌ Gap, or a core non-negotiable is missing |

## Banner Format

The very first line of the output file and the first thing shown to the user must be:

```
{emoji} {Label} — {Role Title} at {Company} | {X} of {N} must-haves matched | {Date}
```

## Hard Rules (from CLAUDE.md)
- Be transparent about gaps. Never hide a mismatch.
- Do not fabricate experience. Suggest honest reframing only.
- Learnable tool-specific languages (SAS, Scala, etc.) can be flagged as "can ramp quickly" if transferable.

## Output Structure

Write the analysis as a markdown file with these sections:

```
{emoji} {Label} — {Role Title} at {Company} | {X} of {N} must-haves matched | {Date}

# JD Analysis: {Role Title} at {Company}

## Job Metadata
- **Company:**
- **Role Title:**
- **Job ID:** (requisition number, posting ID, or generated slug if not found — note which)
- **Location:** (on-site / hybrid / remote; city if specified)
- **Employment Type:** (full-time / part-time / contract / internship)
- **Compensation:** (if listed; salary range, equity, benefits mentioned)
- **Authorization Requirements:** (citizenship, security clearance, green card, work authorization — note exactly what is stated)
- **Visa Sponsorship:** (yes / no / not mentioned — quote the exact language if present)
- **Travel:** (percentage or frequency if mentioned)
- **Reports To:** (if mentioned)
- **Team/Org:** (if mentioned)
- **Source URL:** (if available)
- **Date Analyzed:** {today}

## Role Archetype
Classify the role:
- IC Technical / People Leadership / Cross-functional / Player-Coach
- Individual depth vs. breadth expectation
- Seniority signals (years of experience, "senior", "lead", "staff", scope of ownership)

## Requirements Breakdown

### Must-Have (Explicit)
List each requirement explicitly stated as required. For each:
- Requirement
- My match: ✅ Strong / ⚠️ Partial / ❌ Gap
- Evidence: specific experience from materials, or gap description

### Nice-to-Have (Explicit)
Same format as above for preferred/bonus qualifications.

### Implicit Preferences
Requirements not explicitly stated but strongly implied by:
- JD language and phrasing
- Team/company context
- Role responsibilities that assume certain skills

## Technical Keywords
List all technical terms, tools, frameworks, methodologies mentioned.
Categorize as:
- **Must mirror in resume** (explicitly required)
- **Should include if applicable** (nice-to-have or implied)
- **ATS keywords** (terms to echo for automated screening)

## Company & Culture Signals
- Industry and company stage (startup / growth / enterprise / academic / government)
- Values or culture keywords (move fast, rigorous, collaborative, etc.)
- Tone of the JD (formal / casual / technical / marketing-heavy)
- Any DEI, mission, or impact language

## Red Flags & Considerations
- Overqualification risks (role may be too junior)
- Underqualification risks (role may expect more seniority)
- Scope ambiguity (vague responsibilities, "wear many hats" without clarity)
- Unrealistic combinations (e.g., expert in 8 languages + PhD + 2 years experience)
- Any concerns about role stability, team maturity, or unclear reporting

## Fit Assessment

### Overall Fit: {Strong Fit / Moderate Fit / Stretch / Likely Mismatch}

### Strengths (what makes me competitive)
- Bullet points referencing specific materials

### Gaps (what I am missing)
- Bullet points with honest assessment
- For each gap: suggested framing using adjacent real experience, or "genuine gap, no adjacent experience"

### Positioning Strategy
- 2-3 sentences on how to position for this role
- Which experiences to lead with
- Which narrative angle from bio.md fits best

### Impact Alignment
Assess whether the type of impact demonstrated in the materials matches what this role values:
- **Metrics-driven:** Does the JD reward quantifiable outcomes (revenue, efficiency, accuracy)? Rate alignment with quantified results.
- **Collaboration-driven:** Does the JD emphasize cross-functional influence or stakeholder leadership? Rate alignment with documented cross-functional work.
- **Innovation-driven:** Does the JD reward novel methods, research, or architectural decisions? Rate alignment with publications and project design work.
- **Scale-driven:** Does the JD emphasize volume, production systems, or operational reliability? Rate alignment with large-scale pipelines, production APIs, and operational roles.
Note which impact type the role values most and whether the materials demonstrate it directly, partially, or not at all.

## Resume Tailoring Notes
- Keywords to add to Skills section
- Experiences to emphasize or re-order
- Bullet points from resume_master.md to prioritize
- Any learnable tools to list (with note: "can ramp quickly")
- Recommended reframing strategies for each bullet (choose from the four named strategies below):
  - **Keyword Alignment:** swap the opening verb or noun to echo JD language exactly (e.g., "built" -> "engineered and deployed" when JD uses "deploy")
  - **Emphasis Shift:** reorder clauses so the JD-relevant outcome leads and supporting detail follows
  - **Abstraction Level Adjustment:** raise specificity (e.g., domain name -> "large-scale alternative datasets") or lower it (e.g., narrow tool -> broader method) to match the JD's vocabulary level
  - **Scale Emphasis:** surface volume, throughput, or scope numbers prominently when the JD values operational scale

## Cover Letter Angle
- Suggested opening hook
- Which story from bio.md to lead with
- Company-specific connection point
- Tone recommendation (formal / conversational / technical)
```

## Quality Checks Before Saving
- Every "My match" rating must cite specific evidence from materials or honestly state the gap
- Authorization/sponsorship section must quote exact JD language, not paraphrase
- Do not rate overall fit higher than the gaps justify
- If more than 3 must-have requirements are ❌ Gap, overall fit should not be "Strong Fit"
