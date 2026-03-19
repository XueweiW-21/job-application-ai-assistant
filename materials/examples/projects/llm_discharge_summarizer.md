# Project: LLM Discharge Note Summarizer

## One-Line Summary
An internal tool using Claude API to summarize patient discharge notes, reducing clinician review time by 40%.

## Context
- **When:** September 2023 - January 2024
- **Where:** Lackawanna Health Partners
- **Team size:** Solo build, reviewed by clinical lead
- **My role:** Designed, built, and deployed the full pipeline

## Problem It Solved
Clinicians at partner hospitals were spending 15-20 minutes per patient reviewing discharge notes from referring facilities. The notes were unstructured, inconsistent in format, and buried critical information (medication changes, follow-up requirements) in narrative text.

## What I Built
- Python service calling Claude API with structured output prompts
- Extracts: medication changes, follow-up actions, risk flags, key diagnoses
- Outputs a standardized summary card displayed in the clinician dashboard
- Human-in-the-loop: clinicians review and approve before the summary enters the patient record

## Technical Details
- **Stack:** Python, Claude API (Anthropic SDK), PostgreSQL, internal React dashboard
- **Key design decisions:**
  - Structured JSON output from Claude for consistent parsing
  - Confidence scoring: flags low-confidence extractions for manual review
  - No PHI stored in API calls: de-identification pipeline runs before LLM processing
- **Hardest problem:** Handling the variance in discharge note formats across 4 hospital systems

## Outcomes & Impact
- Reduced average review time from 18 minutes to 11 minutes per patient
- Adopted by 12 clinicians across 3 partner hospitals
- Zero critical information missed in 6-month audit (4,200 notes processed)

## Skills Demonstrated
- LLM API integration and prompt engineering
- Healthcare data privacy (de-identification, PHI handling)
- Production system design with human-in-the-loop
- Stakeholder collaboration (clinician feedback loop)
