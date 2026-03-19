---
name: interview-prep
description: Generate focused interview prep for a specific round, calibrated to interviewer role and JD priority signals
argument-hint: "application folder name, e.g. Acme_DataScientist_R12345_2026-03-17"
---

# Interview Prep

Generate a focused, scannable prep document for a specific interview round. Each document should be reviewable in 10 to 15 minutes before the call.

## Step 1: Gather Context from User

Before generating any prep, collect the following. If the user does not provide these upfront, ask before proceeding:

### Required
- **Application folder** (to load JD analysis and tailored resume)
- **Interview type:** screening / HM / technical / behavioral / final / other
- **Who are you meeting?** Name and title if known

### Helpful (ask if not provided)
- Did the recruiter or coordinator share anything about the format? (duration, topics, panel vs. 1:1)
- Do you have the scheduling email or message? (paste it; often contains hints about what to expect)
- Any specific topics you want to prepare for?
- Is this your first contact with the company or have you spoken to someone before?
- Timeline context: other active interviews, deadlines, competing offers?

If the user provides a scheduling email or recruiter message, extract all useful details: interviewer names, titles, duration, format hints, topics mentioned.

## Step 2: Research the Interviewer

If the user provides the interviewer's name:
1. Use WebSearch to find their LinkedIn profile or company bio
2. Look for: current title, team, how long they have been at the company, prior roles, any publications or talks
3. Use this to calibrate the prep:
   - A senior engineer will probe technical depth differently than a director
   - A data science manager will ask about methodology; an engineering manager will ask about systems
   - A VP or director will focus on impact, communication, and strategic thinking
   - A recruiter will focus on qualification checks and logistics
4. Note any connection points: shared tools, overlapping domains, similar career paths

If the name is not available or WebSearch returns nothing useful, proceed with the interview type as the primary signal.

## Step 3: Load Application Context

Read:
1. `applications/{folder}/jd_analysis.md` — **required**
2. `applications/{folder}/resume_tailored.md` — if available
3. `materials/resume_master.md` — source of truth for experience details
4. `materials/bio.md` — career story and motivations
5. `materials/papers/*.md` — scan if the role values research

Extract from `jd_analysis.md`:
- Must-have requirements and match ratings
- Gaps and suggested framings
- Company and culture signals
- Impact Alignment (if present)
- Red flags and considerations

## Step 4: Identify JD Priority Signals

Scan the original JD requirements and the analysis for **repeated themes**. Count how many times key terms or concepts appear across:
- Job title
- Responsibilities section
- Requirements section
- Nice-to-haves

Rank by frequency. The top 3 to 5 repeated themes are the questions they are most likely to ask. For each, draft the probable question:

Example:
- "data pipeline" appears 4x -> "Tell me about the most complex data pipeline you have built"
- "cross-functional" appears 3x -> "Give me an example of working with non-technical stakeholders"
- "large-scale data" appears 3x -> "How have you handled data processing at scale?"

## Step 5: Generate Prep Document

Output file: `applications/{folder}/interview_prep_{type}.md`
Where `{type}` is: `screening`, `hm`, `technical`, `behavioral`, `final`, or a custom label.

### Document Structure

```
# Interview Prep: {Role} at {Company} — {Type} Round

## Call Context
- **Date:** {if known}
- **Duration:** {if known}
- **Format:** {1:1 / panel / if known}
- **Interviewer:** {name, title, background summary from research}
- **What to expect:** {based on interview type and any hints from recruiter}

## JD Priority Signals
{Ranked list of repeated themes with the likely question each one triggers}

## Prepared Answers

### 1. {Likely question based on top priority signal}
**Situation:** {one sentence — where, when, what was the context}
**What I did:** {two to three sentences — specific actions, tools, decisions}
**Outcome:** {one sentence — quantified result or concrete impact}
**Key detail to mention:** {the specific fact that makes this answer memorable}

### 2. {Next likely question}
...

### 3. {Next likely question}
...

{3 to 5 prepared answers total, each tied to a JD priority signal or known gap}

## Gap Responses
{Only gaps relevant to this specific round. For each:}
- **If they ask about:** {the gap topic}
- **Honest framing:** {1 to 2 sentences that acknowledge the gap and connect adjacent experience}

## Questions to Ask
{3 to 5 questions calibrated to the interviewer's role}
{Each question should signal depth, genuine curiosity, or strategic thinking}
{Avoid questions easily answered by the company website}

## Logistics Cheat Sheet
- **Salary framing:** {strategy, not a number — unless the user provides a target}
- **Timeline:** {other active processes if user wants to mention}
- **Availability:** {start date framing}
- **Follow-up plan:** {send thank-you email same day, reference a specific topic from the conversation}
```

## Interview Type Calibration

Adjust emphasis based on interview type:

### Screening (Recruiter / HR)
- Prepared answers: shorter (60 seconds each), less technical jargon
- Emphasize: qualification match, motivation, logistics readiness
- Gap responses: keep brief, do not over-explain
- Questions to ask: process, timeline, team size, what the HM is looking for
- Logistics cheat sheet: full detail (salary, timeline, availability)

### Hiring Manager
- Prepared answers: full depth (90 seconds each), technical but not whiteboard-level
- Emphasize: judgment, problem-solving approach, how you think about tradeoffs
- Include a "walk me through your resume" narrative (2 minutes, connects the dots, lands on why this role)
- Gap responses: more nuanced framing, show self-awareness
- Questions to ask: team challenges, tech stack, success criteria, how the team works
- Logistics cheat sheet: lighter (HM usually does not negotiate comp)

### Technical
- Prepared answers: deep technical detail, specific tools and methods, architecture decisions
- Emphasize: system design thinking, debugging stories, scale challenges
- Include: "tell me about a time something broke" and "walk me through your architecture for X"
- Gap responses: technical gaps only, show learning trajectory
- Questions to ask: technical debt, deployment practices, data infrastructure, code review culture

### Behavioral
- Prepared answers: pure STAR format, emphasize collaboration, conflict resolution, leadership
- Emphasize: cross-functional work, stakeholder communication, handling disagreement
- Include: "tell me about a time you disagreed with a teammate" and "describe a project that failed"
- Questions to ask: team culture, how disagreements are resolved, mentorship

### Final / Executive
- Prepared answers: high-level impact framing, strategic thinking
- Emphasize: why you want this specific company, long-term career alignment, what you bring that others do not
- Questions to ask: company direction, team growth plans, biggest opportunity the team has not tackled yet

## Step 6: Update Tracker

After writing the prep document, update `tracker.csv`:
- Set `interview_stage` to the interview type
- Set `next_interview_date` if the user provided one
- Set `last_updated` to today
- Append interview type to `notes` (e.g., "HM prep generated 2026-03-17")

## Step 7: Show Summary

Display to the user:
- Interviewer background (if researched)
- Top 3 JD priority signals identified
- Number of prepared answers generated
- Gaps that may come up and the framing strategy
- File path for the prep document
- Reminder: review 15 minutes before the call, not the night before

## Hard Rules

1. **Never fabricate experience.** Every prepared answer must trace to real experience in `materials/`. Reframe emphasis, not facts.
2. **Never fabricate interviewer details.** If WebSearch returns nothing, say so and proceed without.
3. **Apply writing rules from profile.yml** in all generated text.
4. **Keep it scannable.** The entire document should be reviewable in 10 to 15 minutes. If it is too long, cut the lowest-priority prepared answer.
5. **Prepared answers are conversation starters, not scripts.** Write them as structured notes to rehearse from, not paragraphs to memorize.
6. **Be transparent about gaps.** If a gap is likely to come up in this round, prepare an honest response. Never suggest the user bluff.
7. **Preserve the user's voice.** The answers should sound like the user talking, not a career coach's template.
