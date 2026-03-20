---
name: quick-apply
description: One-pass JD extraction, resume tailoring, DOCX generation, and tracker update for mass applications
argument-hint: "JD text, URL, or paste"
---

# Quick Apply

Single-pass pipeline for volume applications. Extracts JD essentials, writes a minimal reference file, then hands off to `/resume-tailor` in lightweight mode. Trades depth for speed.

## Input

JD text, URL (fetched via WebFetch), or pasted content.

## Step 1: Extract JD Essentials

1. If URL, fetch via WebFetch. If pasted text or PDF, use directly.
2. Extract Job ID using the same logic as `/jd-analyze`: look for "Job ID", "Req ID", "Requisition #", "Posting ID", "Job Ref", or similar. If not found, generate a 6-char slug from role title and team/org name.

## Step 2: Fast Fit Screen

Read `materials/resume_master.md` and `materials/skills_inventory.md`. Count must-have requirements. Estimate how many are Strong, Partial, or Gap.

- **🔴 Likely Mismatch:** warn the user this is not a good match. Stop here. Write nothing to disk.
- **🟡 Stretch:** warn briefly but continue. Do not ask for confirmation.
- **🟢 Strong / 🔵 Moderate:** proceed.

## Step 3: Create Folder

- Folder name: `applications/{Company}_{Role}_{JobID}_{YYYY-MM-DD}/`
- Clean company name and role title (underscores, truncate role to 3 words max)
- Check for existing folder with same Job ID. If found, ask the user before overwriting.

## Step 4: Write `jd_quick.md`

Save a minimal JD reference file:

```
{emoji} {Label} — {Role Title} at {Company} | {X} of {N} must-haves matched | {Date}

# Quick Reference: {Role Title} at {Company}

**Job ID:** {ID}
**Location:** {location, work arrangement}
**Company:** {1-2 sentence description from JD intro}

## Key Responsibilities
- {up to 8 bullets}

## Must-Have Keywords
{comma-separated list of required technical terms, tools, methods}

## Nice-to-Have Keywords
{comma-separated list of preferred/bonus terms}

## Gaps
- {any must-have where match is Gap or weak Partial, one-line note each}
```

This file exists so the user can glance at it weeks later if they get a callback.

## Step 5: Run `/resume-tailor`

Hand off to `/resume-tailor` with the application folder name. Because the folder contains `jd_quick.md` (not `jd_analysis.md`), `/resume-tailor` automatically runs in lightweight mode: two reframing strategies, no bio.md voice matching, but full skills rewrite, bullet selection, publications, and DOCX generation.

## Step 6: Update Tracker

Auto, silent:
- If `tracker.csv` does not exist, create it with the full header row
- Header: `date_applied,company,role,folder,job_id,source,referral,fit_tier,status,interview_stage,next_interview_date,last_contact_date,follow_up_date,resume_version,cover_letter,notes,last_updated`
- If a row for this folder or Job ID already exists, update it
- If no row exists, create one with: `date_applied` = today, `status` = `quick_applied`, `fit_tier` from banner, `resume_version` = `Yes`, `cover_letter` = `No`, `notes` = `quick-apply`, `last_updated` = today

## Step 7: Summary

Display to the user:
- Company, role, fit tier
- Must-have gaps (if any)
- File paths for `jd_quick.md`, `resume_tailored.md`, and DOCX

Do not ask about cover letters, referral notes, or next steps. The user is in volume mode.

## Upgrade Path

If the user later gets a callback, they can run `/jd-analyze` on the same folder to produce a full `jd_analysis.md`. Then `/resume-tailor` again for a deeper rewrite (full mode with all four strategies, voice matching, and richer tailoring notes). The `jd_quick.md` file stays alongside the full analysis.

## Hard Rules

1. **Never fabricate experience.** Every bullet traces to `resume_master.md`.
2. **Never change job titles, company names, dates, or team sizes.**
3. **Apply writing rules from `profile.yml`.**
4. **Be transparent about gaps.** List them in `jd_quick.md`.
5. **ATS language exception:** learnable tool languages can be added to skills list if transferable basis exists.
