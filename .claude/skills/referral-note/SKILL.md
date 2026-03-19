---
name: referral-note
description: Write a short third-person referral blurb summarizing why the user is a strong fit for a specific role
argument-hint: "application folder name, e.g. Acme_DataScientist_R12345_2026-03-17"
---

# Referral Note Generator

Write a concise third-person blurb (150 to 200 words) that a referrer can forward to the hiring manager. Grounded in the user's real experience and the specific fit reasons from the JD analysis.

## Steps

1. Read `profile.yml` for the user's name
2. Read `applications/{folder}/jd_analysis.md` — extract top strengths and the role's most valued requirements
3. Read `materials/resume_master.md` — for concrete facts (years, scale, tools, outcomes)
4. Write the note:
   - Third-person throughout ("{Name} has...", "They...")
   - Lead with experience breadth and depth most relevant to this role
   - Name 2 to 3 specific, concrete things (scale, publications, tools, outcomes) that map directly to the JD's priorities
   - Close with 1 sentence on why the match is strong and an offer to introduce
   - Apply writing rules from `profile.yml`
   - Professional but not stiff — written as something a real person would actually send

5. Save to `applications/{folder}/referral_note.md` and display to the user
