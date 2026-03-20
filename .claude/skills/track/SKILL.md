---
name: track
description: Log, query, and update job applications in tracker.csv
argument-hint: "add|update|list|summary [folder] [status]"
---

# Application Tracker

Maintain a single `tracker.csv` at the project root to log every application and track its lifecycle.

## Auto-Add Integration

This tracker is updated automatically by other skills:
- **`/jd-analyze`** — when a new `jd_analysis.md` is written, add a row with status `analyzed` and populate company, role, folder, fit_tier, and date fields
- **`/quick-apply`** — when `jd_quick.md` and `resume_tailored.md` are written, add a row with status `quick_applied`, `resume_version` = `Yes`, `notes` = `quick-apply`
- **`/resume-tailor`** — when `resume_tailored.md` is written, update the row: set `resume_version` to `Yes`
- **`/cover-letter`** — when `cover_letter.md` is written, update the row: set `cover_letter` to `Yes`
- **`/interview-prep`** — when interview prep is generated, update: set `interview_stage` to the type (screening / HM / technical / behavioral / final), set `next_interview_date` if the user provides one, and append the interview type to `notes`

When auto-adding, if a row for the folder already exists, update it rather than creating a duplicate.

## CSV Columns

```
date_applied,company,role,folder,job_id,source,referral,fit_tier,status,interview_stage,next_interview_date,last_contact_date,follow_up_date,resume_version,cover_letter,notes,last_updated
```

| Column | Type | Source | Description |
|---|---|---|---|
| date_applied | YYYY-MM-DD | Today when row is created | Date the application was submitted (may differ from analysis date) |
| company | text | Parsed from folder name | Company name |
| role | text | Parsed from folder name | Role title |
| folder | text | Application folder name | Links to the application directory |
| job_id | text | Extracted from JD or generated slug | Requisition/posting ID — use this to search for a specific role later |
| source | text | User input | How found: LinkedIn, referral, company site, recruiter outreach, etc. |
| referral | text | User input, optional | Name of referring employee if applicable |
| fit_tier | text | From jd_analysis.md banner | e.g., 🟢 Strong Fit, 🔵 Moderate Fit |
| status | text | User updates | One of: analyzed, quick_applied, applied, screening, interview, offer, rejected, withdrawn, ghosted |
| interview_stage | text | From /interview-prep | Latest stage: screening, HM, technical, behavioral, final, or blank |
| next_interview_date | YYYY-MM-DD | User input | Date of the next scheduled interview |
| last_contact_date | YYYY-MM-DD | User updates | Last date of any communication with the company |
| follow_up_date | YYYY-MM-DD | Computed or user input | When to follow up next (see Follow-Up Logic) |
| resume_version | Yes/No | Auto from /resume-tailor | Whether a tailored resume exists |
| cover_letter | Yes/No | Auto from /cover-letter | Whether a cover letter exists |
| notes | text | User input + auto-appended | Free text; interview types are auto-appended |
| last_updated | YYYY-MM-DD | Auto-set on any change | Timestamp of most recent update |

## Operations

### `/track add [folder]`

Add a new row manually. Steps:
1. Parse company and role from the folder name (split on underscores, last segment is date)
2. Check if `applications/{folder}/jd_analysis.md` exists; if so, extract fit_tier from the banner line
3. Check if `resume_tailored.md` and `cover_letter.md` exist in the folder
4. Ask the user for: source, referral (optional), status (default: `applied`), notes (optional)
5. Set `date_applied` to today, `last_updated` to today
6. Compute `follow_up_date` per Follow-Up Logic
7. Append the row to `tracker.csv`

If the row already exists (matched by folder), update it instead of duplicating.

### `/track update [folder] [field=value]`

Update one or more fields for an existing row. Common patterns:
- `/track update Infosys_AIEngineer_2026-03-17 status=interview`
- `/track update Infosys_AIEngineer_2026-03-17 status=interview next_interview_date=2026-03-20`
- `/track update Infosys_AIEngineer_2026-03-17 status=rejected`

Always:
- Set `last_updated` to today
- If `status` changes to `interview`, prompt for `interview_stage` and `next_interview_date` if not provided
- If `status` changes to `rejected`, `withdrawn`, or `offer`, clear `follow_up_date` and `next_interview_date`
- If `last_contact_date` is updated, recompute `follow_up_date` per Follow-Up Logic

### `/track list [filter]`

Display all applications as a formatted table, sorted by `last_updated` descending.

Optional filters:
- `/track list` — show all
- `/track list interview` — filter by status
- `/track list follow-up` — show only rows where `follow_up_date` is today or past due

Table display should include: company, role, status, interview_stage, fit_tier, next_interview_date, follow_up_date, last_contact_date. Omit folder, notes, and other columns for readability. The user can ask for full details on a specific row.

### `/track summary`

Show quick stats:
- Total applications
- Breakdown by status (analyzed: X, applied: X, screening: X, interview: X, offer: X, rejected: X, withdrawn: X, ghosted: X)
- Breakdown by fit tier
- Applications with overdue follow-ups (follow_up_date before today)
- Upcoming interviews (next_interview_date within 7 days)

## Follow-Up Logic

When computing `follow_up_date`:

| Status | Follow-up rule |
|---|---|
| quick_applied | 7 days after `date_applied` |
| applied | 7 days after `date_applied` |
| screening | 5 days after `last_contact_date` |
| interview | 3 days after `last_contact_date` or `next_interview_date` (whichever is later) |
| offer | No auto follow-up |
| rejected | No follow-up |
| withdrawn | No follow-up |
| ghosted | No follow-up |
| analyzed | No follow-up (not yet applied) |

The user can override `follow_up_date` manually at any time.

## File Handling

- If `tracker.csv` does not exist, create it with the header row on first use
- Use comma as delimiter; quote fields that contain commas
- When reading/writing CSV, preserve existing data exactly
- When displaying to the user, render as a markdown table for readability
- The CSV should be valid and openable in Excel or Google Sheets

## Hard Rules

1. **Never delete rows.** Status updates handle lifecycle (rejected, withdrawn, ghosted). The full history is valuable.
2. **No duplicate folders.** Always check before adding. Update if exists.
3. **Dates in YYYY-MM-DD format.** Always. No exceptions.
4. **Auto-updates are silent.** When other skills update the tracker, do not interrupt the user's flow. Just update and continue.
5. **User data is authoritative.** If the user provides a value that conflicts with auto-populated data, the user's value wins.
