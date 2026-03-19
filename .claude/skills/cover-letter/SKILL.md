---
name: cover-letter
description: Write a cover letter in the user's voice using JD analysis, company research, and career narrative
argument-hint: "application folder name, e.g. Acme_DataScientist_R12345_2026-03-17"
---

# Cover Letter Generator

Write a concise, high-signal cover letter that gives the hiring manager context a resume cannot: why this company, why this role, why now, and why the career trajectory makes sense.

## When to Use

This skill is opt-in. Many applications do not accept or require a cover letter. Use it when:
- The application has a cover letter upload field
- A referral or warm intro makes it likely a human will read it
- The role is at a smaller company, academic institution, or government agency where CLs are standard
- The user explicitly asks for one

## Input

The user provides an application folder name (e.g. `Acme_DataScientist_R12345_2026-03-17`).

Optional additional context the user may provide:
- **Referral:** name and team of the referring employee
- **Company research notes:** anything the user has already learned about the company, team, product, or culture
- **Specific angle:** a particular story or connection the user wants to lead with

## Step 1: Load Context

Read all of these before writing anything:

1. `profile.yml` — user's name and writing rules
2. `applications/{folder}/jd_analysis.md` — **required**. If missing, stop and tell the user to run `/jd-analyze` first.
3. `applications/{folder}/resume_tailored.md` — if available, use to see what the resume already covers (avoid restating the same bullets)
4. `materials/bio.md` — career story, motivations, writing style notes, unique differentiators
5. `materials/resume_master.md` — source of truth for experience details
6. `materials/papers/*.md` — scan for relevant publications if the role values research

From `jd_analysis.md`, extract:
- Cover Letter Angle section (opening hook, story, company connection, tone)
- Company and Culture Signals (industry, values, tone)
- Fit Assessment (strengths, gaps, positioning strategy)
- Impact Alignment (if present; which impact type the role values most)

## Step 2: Company and Role Context

**The JD is the primary source.** The company intro, "About the Role" section, and listed responsibilities are the hiring manager's own framing of what matters. Use that language and those priorities first.

Extract from the JD:
- Company mission and what they actually do (from the JD intro)
- Team name, topic, and what the role works on (from "About the Role" or equivalent)
- The specific responsibilities listed — these are what the cover letter must map experience to

**Web research is supplementary, not primary.** Only use WebFetch if the JD is thin on company or team context. When used, look for:
- A concrete, specific detail that shows genuine familiarity (not "I admire your mission")
- A connection point between the company's work and the user's experience

Do not let web-researched details displace or outweigh what the JD itself says.

## Step 3: Build the Narrative

Identify the three pillars of the letter:

### Pillar 1: The Hook
- If there is a referral: lead with it. First sentence. "[Name] on your [Team] team suggested I reach out about the [Role] opening."
- If no referral: lead with the single strongest match between the user's experience and the role's biggest need. Make it concrete and specific, not generic.

### Pillar 2: Experience Mapped to Role Responsibilities
This is the CL's primary value add over the resume. Directly map specific past experiences to the role's listed responsibilities:
- Take the 2 to 3 most important responsibilities from the JD and show concrete evidence of having done similar work
- Name specific projects, datasets, methods, or publications that demonstrate the match
- Where the match is partial or adjacent, be honest about it and explain what transfers
- Use the Impact Alignment from `jd_analysis.md` to match the narrative to what the role values

### Pillar 3: The Company Connection
- Ground this in what the JD itself says about the company, team, and mission
- Tie the company's stated mission or team focus to a real experience or value from `bio.md`
- Only supplement with web research if the JD provides too little company context on its own
- This paragraph should make it clear this letter was written for *this* company, not copy-pasted

## Step 4: Write the Letter

### Structure (3 to 4 paragraphs, 250 to 350 words total)

**Paragraph 1: Opening (2 to 3 sentences)**
- Referral name drop (if applicable)
- Role title and company name
- One-sentence hook: the strongest match stated concretely

**Paragraph 2: Career Arc and Transferable Skills (4 to 6 sentences)**
- The pivot narrative: why the trajectory is an asset
- Connect two specific past experiences to the target role's needs
- Surface the transferable skills that the resume shows but doesn't explain
- Address the most significant gap from the fit assessment honestly if it is addressable

**Paragraph 3: Company Connection (2 to 4 sentences)**
- The specific detail from Step 2
- Why it resonates with the user's experience or goals
- What the user would bring to that specific context

**Paragraph 4: Close (1 to 2 sentences)**
- Direct and confident, not deferential
- "I would welcome the opportunity to discuss how my experience with [specific thing] could contribute to [specific team/initiative]."
- No groveling, no empty enthusiasm

### Tone Calibration
- **Read the JD's own tone first.** Match the JD's language and emphasis.
- Read the tone recommendation from `jd_analysis.md` Cover Letter Angle as a secondary input.
- **Enterprise/consulting:** formal but direct. Structured paragraphs. No contractions.
- **Startup/growth:** conversational but specific. Can use shorter sentences and more personality.
- **Scientific/research-driven:** lead with publications, methodology, and domain expertise. Can be longer (up to 400 words).
- **All tones:** match the user's voice from `bio.md` Writing Style Notes.

## Step 5: Quality Checks

Before saving:
- Every claim traces to a real experience in `materials/`
- Writing rules from `profile.yml` are applied
- Company-specific detail is accurate and sourced (not fabricated)
- The letter does not restate resume bullets verbatim; it adds narrative context
- Referral name is included only if the user provided one
- Word count is 250 to 350 (up to 400 for academic roles)
- The letter passes the "swap test": if you replaced the company name with a competitor, would the letter still make sense? If yes, the company connection is too generic. Rewrite Paragraph 3.

## Step 6: Write Output

Save the cover letter to:
```
applications/{folder}/cover_letter.md
```

## Step 6b: Update Tracker

After writing the file (auto, silent):
- Find the row in `tracker.csv` where `folder` matches the current folder
- Set `cover_letter` = `Yes` and `last_updated` = today
- If no row exists, create one (status = `analyzed`, fill what is available)

## Step 7: Show Summary

Display to the user:
- The hook used (referral or strongest match)
- The career arc angle chosen
- The company-specific connection point and its source
- Any gaps that were addressed or left unaddressed
- Tone chosen and why
- File path for the output

## Hard Rules

1. **Never fabricate experience.** Every claim must trace to `materials/`. Reframe emphasis, not facts.
2. **Never fabricate company details.** If research yields nothing useful, rely on what the JD itself says. Do not invent initiatives, products, or values.
3. **Apply writing rules from profile.yml** in all generated text.
4. **Referral only if provided.** Never invent or assume a referral. If the user does not mention one, do not include one.
5. **Do not restate resume bullets.** The CL adds context and narrative the resume cannot. If a sentence could be a resume bullet, rewrite it.
6. **Be transparent about gaps.** If a gap is addressed in the letter, the framing must be honest.
7. **Preserve the user's voice.** Read `materials/bio.md` Writing Style Notes for guidance. No corporate buzzword stacking.
