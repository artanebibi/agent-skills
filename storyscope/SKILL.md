---
name: storyscope
description: Flag AI-written fiction, or make fiction read more human, using the narrative-level markers from the StoryScope paper (Russell et al., COLM 2026, arXiv 2604.03136). These are 30 core features such as thematic over-explaining, embodied emotion, tidy single-track plots, linear time and missing named references, plus per-model fingerprints for Claude, GPT, Gemini, DeepSeek and Kimi. Use this whenever someone asks if a story, chapter, fan fiction, novel excerpt or creative-writing submission "sounds AI" or was written by ChatGPT or Claude. Also use it when they want to audit fiction for AI tells, ask why a story feels generic or machine-made, or want a story written or revised to feel more human, less formulaic or less "AI slop". Use it even if they don't name the paper. Not for non-fiction, essays, emails or code.
---

# StoryScope: narrative-level AI fiction analysis

StoryScope compared 61,608 stories of about 5,000 words each. For each of 10,272 writing prompts, there was one human story and one each from Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2 and Kimi K2.5. Its central finding: AI fiction differs from human fiction in **how the story is built**, not just in word choice.
- Narrative features alone, with no style cues, separated human from AI at 93.2% macro-F1.
- A compact set of **30 core features** reached 84.8%.
- AI stories over-explain their themes, render emotion through the body and senses, and favor tidy, single-track, linear plots.
- Human stories are more temporally complex, name real works and places, talk to the reader, and leave protagonists morally ambiguous.

Because these are structural choices, surface edits barely hide them. Removing clichés and purple prose only moved detection from 95.5% to 93.9%.

This skill uses those findings three ways:

| Mode | Use when the user… | Output |
|---|---|---|
| **Detect** | asks whether a story is AI-written, wants it audited, or asks why it feels generic | an evidence-backed report with an AI-lean index |
| **Humanize** | gives you a draft and wants it to read more human | a structurally revised story, change notes and before/after scores |
| **Write** | asks for a new story and cares that it not read as AI | a story planned against the AI defaults |

Detect is the first step of Humanize. If the request is ambiguous ("can you look at my story, it feels off"), start with Detect and offer Humanize at the end.

## Files in this skill

- `references/core-features.md`: the 30 features, with the exact questions, allowed values, the paper's human vs. AI numbers and annotation notes. Read it in full before annotating.
- `references/fingerprints.md`: per-model fingerprints. Read it for Detect when attribution comes up, and for Humanize or Write to know your own habits.
- `references/humanize-playbook.md`: writing moves for each feature, the revision loop and a planning sheet. Read it for Humanize and Write.
- `scripts/score_story.py`: turns an annotation into per-feature leans and a 0–100 AI-lean index.
  - `python3 scripts/score_story.py template` prints a blank annotation.
  - `python3 scripts/score_story.py score FILE.json` prints the report. Add `--json` for machine-readable output.

  Run it with the skill directory's path. Save annotation files somewhere temporary, not in the user's project, unless they ask.

## Detect

1. **Check fit.** The features come from narrative fiction of about 5,000 words.
   - If the text isn't narrative fiction, say this skill doesn't apply, and don't force it.
   - Under about 1,500 words, features like subplots, location variety and anachrony have little room to show. Still run it, but mark confidence low.
2. **Read the whole story first.** Then annotate all 30 features, following `references/core-features.md`, into a copy of the template. Give every answer a short quote or scene pointer as evidence.
   - Annotate **before** you score, and don't go back and adjust answers after seeing the number. The score is only as honest as the annotation.
   - If you wrote the story yourself, earlier in this conversation, say so in the report, because self-annotation is biased.
3. **Score it** with `score_story.py score`.
4. **Check fingerprints** in `references/fingerprints.md`. Only mention a likely model if several fingerprints co-occur. Even then, call it a weak hint: the paper's six-way attribution was 68% at best with narrative features.
5. **Write the report** in this shape:

```markdown
## StoryScope read: <title or first line>

**Narrative AI-lean index:** <N>/100, <verdict> (<k>/30 features scored)
**Confidence:** <low / moderate>, because <length, genre, self-annotation, mixed signals…>

### Most AI-typical choices
- **<Feature>.** <what the story does, with a short quote>. <paper: human X vs. AI Y>
- … (3–6 items, the largest positive contributions)

### Most human-typical choices
- … (2–5 items, the largest negative contributions)

### Possible model fingerprint
<one or two sentences, or "none that stand out">

### What this means
<2–4 sentences. This is a pattern match against population averages from one study, not proof of authorship. Note genre effects, for example fables and children's stories are meant to moralize. If the user is a writer, point to Humanize.>
```

Keep the report tight. Readers want the strongest evidence, not all 30 rows. Offer the full table if they want it.

## Humanize (revise a draft)

1. Run Detect, silently or shown, depending on whether the user wants the diagnosis.
2. Read `references/humanize-playbook.md`. From the AI-leaning features with the largest contributions, pick the **4–6 moves** that suit this story. Don't flip all 30. Human stories are distinctive because they are *more varied*, and a story pushed to the human average on every axis is just a new template.
3. Revise **structure**: scene order, who resolves the ending, a subplot, which explanations get cut, what's named, how emotion is carried. Sentence polish alone won't change these features. That is the paper's editing result.
4. Keep the user's plot, characters and voice unless they've asked for bigger changes. It's their story. If a move would change the premise, propose it rather than doing it.
5. Re-annotate the revision honestly and score it again.
6. Deliver:
   - the revised story
   - short change notes, each one naming the feature, what changed and why
   - before and after index, plus any features that didn't move

## Write (new story)

1. Fill in the planning sheet at the end of `references/humanize-playbook.md` before drafting. Left unplanned, the defaults drift toward the AI cluster: linear, single-track, moralizing, ending in acceptance.
2. Check `references/fingerprints.md` for your own model's habits. Claude's are flat escalation, epilogues, uniform voice and reverence for convention.
3. Write the story.
4. Self-check: annotate, score and revise the two or three most AI-typical choices once.
5. Deliver the story. Add a few lines of notes only if the user wants to see the craft choices.

## Limits

State these honestly, especially in Detect.
- **This isn't the paper's classifier.** The paper trained XGBoost on 257 narrative features, with Gemini 3 Flash as annotator. This skill uses the 30 core features, the paper's published human/AI means and an uncalibrated naive-Bayes-style score with assumed variances. Expect weaker accuracy than the paper's 84.8% core-only result.
- **The averages overlap.** The paper notes per-story distributions "overlap substantially". Plenty of human stories are tidy and moralizing, and some AI stories aren't.
- **Genre and purpose matter.** Fables, parables, children's books, devotional fiction and some genre fiction are built on explicit morals and clean resolutions.
- **Model drift.** The findings describe 2026 model versions. Newer models, or a human-AI collaboration, may look different.
- **Style isn't covered.** The paper notes surface tells (em-dashes, "delve", "tapestry") are fading as models update. This skill looks deliberately at narrative structure instead.
- **Never present a result as proof of authorship.** Don't use it on its own to accuse a student, author or contest entrant. It is one signal, best combined with context and other evidence.

Humanizing improves the craft of a story along the dimensions where AI fiction is predictable. It doesn't change who wrote it, and any disclosure rules the user is under still apply.
