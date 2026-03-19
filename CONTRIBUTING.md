# Contributing

Thanks for considering contributing to this project. Here's how to help.

## What to Contribute

**Welcome:**
- Bug fixes in skills or the docx generator
- Improvements to skill instructions (clearer wording, better edge case handling)
- New example materials for different domains (design, law, marketing, etc.) in `materials/examples/`
- Documentation improvements

**Also welcome but discuss first (open an issue):**
- New skills
- Changes to the skill flow or trigger logic
- Changes to the materials schema

**Not accepted:**
- Personal data (resumes, cover letters, real JD analyses)
- API keys or credentials
- Domain-specific templates that change the materials schema (the schema is intentionally universal)

## Non-Negotiable Rules

These are the project's identity. PRs that violate them will not be merged:

1. **No fabrication.** Skills must never invent experience, skills, or achievements. Reframing is fine. Making things up is not.
2. **Transparent gap handling.** When the user's materials don't match a JD requirement, the skill must say so clearly. Never hide or paper over a gap.
3. **User's voice.** Generated text must reflect the user's writing style (from `bio.md`), not a generic AI tone.

## How to Submit

1. Fork the repo
2. Create a branch: `git checkout -b your-feature`
3. Make your changes
4. If you changed a SKILL.md, test it: paste a sample JD and show the before/after output in your PR description
5. Submit a PR with:
   - What you changed and why
   - Any test output showing the change works

## Code Style

- Skills are markdown files. Keep them scannable. Use short sentences and clear structure.
- Python code (generate_docx.py): follow existing patterns. No new dependencies without discussion.
- No hyphens or dashes in example generated text (this is a writing rule enforced across the project).

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
