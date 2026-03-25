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
- Do you have any insider info? (friend on the team, recruiter hints, coffee chat notes, question lists shared by the company)
- Timeline context: other active interviews, deadlines, competing offers?

If the user provides a scheduling email or recruiter message, extract all useful details: interviewer names, titles, duration, format hints, topics mentioned.

If the user provides insider intel (coffee chat transcript, recruiter notes, friend's advice), analyze it for: team values, likely question themes, technical focus areas, cultural signals not visible in the JD, and any specific questions or topics flagged.

## Step 2: Search for Interview Questions Online

Proactively search for real interview questions and experiences for this company and role. Do not wait for the user to provide a question list — go find what exists.

### Search sources (try in this order)

1. **WebSearch:** `"{company}" "{role}" interview questions`
2. **WebSearch:** `"{company}" interview experience {year}` (use the current year and the previous year)
3. **Glassdoor:** `site:glassdoor.com "{company}" "{role}" interview`
4. **小红书 (Red Note / Xiaohongshu):** Search `{company} 面试` or `{company} interview` — people frequently post detailed question lists after interviews, especially for tech, finance, and data roles
5. **一亩三分地 (1point3acres.com):** Search `{company} 面经` — a Chinese-language BBS where people share interview experiences. Note: full posts may require credits to view, but titles and partial content are often visible and still useful
6. **Other sources:** Blind/Teamblind, Fishbowl, InterviewQuery, DataLemur, Wall Street Oasis (for finance roles), LeetCode Discuss

### What to extract
- Specific questions that were asked (especially if multiple people report similar questions — these are likely from the company's standard question bank)
- Interview format and structure (how many rounds, duration, panel vs 1:1)
- Topics or themes that appear repeatedly
- Any tips from candidates about what the interviewers seemed to value

### How to use the results
- If specific questions are found, incorporate them into the JD Priority Signals (Step 5) and generate prepared answers for them
- If format details are found, update the Call Context section
- If nothing useful is found, say so and proceed with JD-based prediction only
- Always cite the source so the user can check the original if they want

## Step 3: Load Previous Round Context

Check for existing prep docs and debrief notes in the application folder. If this is round 2 or later, load what was already covered and explicitly differentiate.

### Read (if they exist)
- `applications/{folder}/interview_prep_*.md` — all previous prep documents
- `applications/{folder}/debrief_*.md` — post-interview debrief notes from previous rounds

### Extract from previous rounds
- Which STAR stories were already used (do not repeat them unless the user asks)
- Which topics and questions were already covered
- What the user learned from the debrief (what went well, what surprised them, what the interviewer said about next steps)
- Any feedback or hints about what this round will focus on

### Apply to this round
- State at the top of the new prep document: what previous rounds covered and what this round will focus on differently
- Choose fresh stories and angles that have not been used yet
- If the debrief from the previous round contains hints about this round's focus, prioritize those

If this is the first round, skip this step.

## Step 4: Research the Interviewer

If the user provides the interviewer's name:
1. Use WebSearch to find their LinkedIn profile or company bio
2. Look for: current title, team, how long they have been at the company, prior roles, any publications or talks

### How to use interviewer research

The interviewer's background is for **tone and depth calibration**, not for predicting specific questions. Companies typically have standardized question sets that reflect what the company values. The interviewer's personal domain expertise does not reliably predict what they will ask.

Use the research to:
- **Calibrate depth:** A senior engineer will probe differently than a director. A recruiter will focus on logistics. Adjust the level of technical detail accordingly.
- **Calibrate tone:** A peer interview is more collegial. An executive interview is more about impact and strategic thinking.
- **Identify rapport points:** Shared tools, overlapping domains, similar career paths — useful for natural conversation, not for predicting questions.
- **Inform questions to ask:** Tailor your "questions to ask" section to what this person would know and care about.

Do NOT assume the interviewer will ask about their own specialization. If the online search from Step 2 found company question templates, those outrank interviewer-background predictions.

If the name is not available or WebSearch returns nothing useful, proceed with the interview type as the primary signal.

## Step 5: Load Application Context

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

## Step 6: Identify JD Priority Signals

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

**Merge with online search results:** If Step 2 found specific questions from real candidates, add those to the priority signals list. Real reported questions take priority over JD-inferred ones.

## Step 7: Generate Prep Document

Output file: `applications/{folder}/interview_prep_{type}.md`
Where `{type}` is: `screening`, `hm`, `technical`, `behavioral`, `final`, or a custom label.

### Document Structure

```
# Interview Prep: {Role} at {Company} — {Type} Round

## Pronunciation Guide
{Include if any technical terms, notation, acronyms, or company-specific jargon might come up.
List each term with how to say it naturally in conversation.
This section helps users who speak English as a second or third language.
Omit this section for screening rounds or if no technical terms are relevant.}

## Call Context
- **Date:** {if known}
- **Duration:** {if known}
- **Format:** {1:1 / panel / if known}
- **Interviewer:** {name, title, background summary from research}
- **What to expect:** {based on interview type, intel, and any hints from recruiter}
- **Previous rounds covered:** {summary of what prior rounds already discussed, if applicable}

## JD Priority Signals
{Ranked list of repeated themes with the likely question each one triggers}
{Include any real questions found from online search, with source noted}

## Prepared Answers

### 1. {Likely question based on top priority signal}

**How to say it:**

{Write the answer in first person, conversational paragraphs — as if the user is speaking
naturally on a phone call. Use short sentences. Include natural transitions between ideas.
This is not a script to memorize — it is a rehearsal draft that sounds like a real person talking.}

**Key detail to mention:** {the specific fact that makes this answer memorable}

### 2. {Next likely question}
...

### 3. {Next likely question}
...

{3 to 5 prepared answers total, each tied to a JD priority signal or known gap}

## Gap Responses
{Only gaps relevant to this specific round. For each:}
- **If they ask about:** {the gap topic}
- **How to say it:** {1 to 3 sentences written in first person, conversational tone, that acknowledge the gap and connect adjacent experience}

## Questions to Ask
{3 to 5 questions calibrated to the interviewer's role and seniority}
{Each question should signal depth, genuine curiosity, or strategic thinking}
{Avoid questions easily answered by the company website}

## Logistics Cheat Sheet
- **Salary framing:** {strategy, not a number — unless the user provides a target}
- **Timeline:** {other active processes if user wants to mention}
- **Availability:** {start date framing}
- **Follow-up plan:** {send thank-you email same day, reference a specific topic from the conversation}
```

### Writing Style for Prepared Answers

All prepared answers must be written in **speakable format**:
- First person, conversational paragraphs — how the user would actually say it on a call
- Short sentences. Natural transitions. No bullet-point lists to "read off."
- Include the user's project names and specific details so the answer sounds grounded, not generic
- The user may be speaking in their second or third language. Prioritize natural phrasing, clear sentence structure, and simple transitions over dense or compressed language.
- If technical terms, notation, or jargon might come up in the conversation, include them in the Pronunciation Guide at the top of the document

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

## Step 7b: Study Plan (Optional — Technical Rounds)

After generating the prep document for a **technical or final round**, ask the user:

> "Do you want a study plan for this round? If so, how much time do you have before the call?"

### If the user wants a study plan:

1. Identify technical concepts likely to come up based on: JD requirements, questions found in online search (Step 2), insider intel, and interviewer background
2. Organize by priority:
   - **Priority 1 — Almost certain:** Topics confirmed from intel, real question lists, or JD must-haves
   - **Priority 2 — Likely:** Topics strongly implied by JD or role type
   - **Priority 3 — Good to know:** General topics for the field that round out preparation
3. For each topic: what to review, estimated study time, and whether it needs a deep review or a quick refresher
4. **Budget to the user's available time.** If the user has 2 hours, cut to Priority 1 only and estimate times that fit within 2 hours. If they have a full day, include all priorities.
5. Organize into a day-by-day or session-by-session schedule if the user has multiple days before the interview

### If the user does not want a study plan or this is not a technical round, skip this step.

## Step 8: Update Tracker

After writing the prep document, update `tracker.csv`:
- Set `interview_stage` to the interview type
- Set `next_interview_date` if the user provided one
- Set `last_updated` to today
- Append interview type to `notes` (e.g., "HM prep generated 2026-03-17")

## Step 9: Show Summary

Display to the user:
- Interviewer background (if researched)
- Online search findings (if any real questions or format details were found)
- Top 3 JD priority signals identified
- Number of prepared answers generated
- Gaps that may come up and the framing strategy
- File path for the prep document
- Reminder: review 15 minutes before the call, not the night before
- If technical round: ask if the user wants a study plan

## Step 10: Post-Round Debrief (After the Interview)

This step is triggered when the user returns after an interview and says something like "the call went well," "just finished the interview," "I think I will move to the next round," or similar.

### Prompt the user:
- How did it go overall?
- What questions did they actually ask? (capture these — they reveal the company's question bank and are valuable for future rounds)
- Anything that surprised you?
- Did any gaps come up? How did you handle them?
- Did they mention next steps, what the next round focuses on, or who you will meet next?
- Anything you wish you had prepared better?

### Save the debrief:
Output file: `applications/{folder}/debrief_{type}.md`

Structure:
```
# Debrief: {Role} at {Company} — {Type} Round
> Date: {today}

## Overall impression
{user's assessment}

## Questions actually asked
{list of questions — these are gold for future rounds and for other users applying to the same company}

## What went well
{what the user felt good about}

## What surprised or challenged
{unexpected topics, harder-than-expected questions}

## Gaps that came up
{what gaps surfaced and how the user handled them}

## Next steps
{what the interviewer or recruiter said about next steps, next round details, who they will meet}

## Notes for next round prep
{anything the user wants to remember or prepare differently}
```

### Update tracker:
- Update `interview_stage` and `last_contact_date`
- Add debrief summary to `notes`
- If next round info is available, update `next_interview_date`

## Hard Rules

1. **Never fabricate experience.** Every prepared answer must trace to real experience in `materials/`. Reframe emphasis, not facts.
2. **Never fabricate interviewer details.** If WebSearch returns nothing, say so and proceed without.
3. **Apply writing rules from profile.yml** in all generated text.
4. **Keep it scannable.** The entire document should be reviewable in 10 to 15 minutes. If it is too long, cut the lowest-priority prepared answer.
5. **Write answers as spoken words, not reading notes.** The user may be speaking in their second or third language. Natural phrasing, short sentences, and clear transitions matter more than comprehensiveness. Every prepared answer should sound like a real person talking on a phone call.
6. **Be transparent about gaps.** If a gap is likely to come up in this round, prepare an honest response. Never suggest the user bluff.
7. **Preserve the user's voice.** The answers should sound like the user talking, not a career coach's template. Read `materials/bio.md` Writing Style Notes for voice guidance.
8. **Do not over-index on interviewer specialization.** Research the interviewer for calibration (depth, tone, rapport), but do not assume they will ask about their own domain. Company question banks drive what gets asked.
9. **Differentiate across rounds.** If previous prep or debrief docs exist, use fresh stories and angles. Never regenerate the same material the user has already reviewed.
