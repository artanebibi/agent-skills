# Humanize playbook: narrative moves away from the AI cluster

This playbook turns StoryScope's findings into writing moves. Each move names the core feature it shifts (see `core-features.md`) and the paper's human vs. AI numbers, so you can tell why it matters.

## Three principles before any move

1. **Change the structure, not just the sentences.** The paper ran a surface-level editor over AI stories that removed clichés, purple prose and redundant exposition. The narrative classifier still flagged them at 93.9% macro-F1, against 95.5% before editing. Swapping words leaves the AI shape intact. The moves below change what happens, in what order, who causes it and what the story says out loud.
2. **Aim for specific, not average.** Human stories aren't "the human mean on every axis". They are *more dispersed* and *rarer* than AI stories. A human story was the most unusual of six versions 57.8% of the time. Flipping all 30 features to their human-typical value just builds a new template. Pick the 4–6 moves that fit this story and its voice, and leave the rest alone.
3. **Serve the story.** Every move should make the piece better for a reader: less told, more trusted, more surprising. If a move fights the story's genre or purpose, skip it. A fable is allowed a moral, and a children's story is allowed a tidy ending. Say so in the change notes.

## Moves by theme

### A. Stop over-explaining the theme
AI-elevated: narratorial commentary 77% vs. 52%, explicitness 3.94 vs. 3.28, philosophical dialogue 59% vs. 34%.
- **Cut the lesson line.** Delete the sentence or paragraph where the narrator states what it all meant, usually near the end. End on an action, an image or a line of dialogue that implies it.
- **Turn the debate into conflict about something concrete.** Characters arguing about the nature of memory become characters arguing about whether to sell the house. The theme stays underneath.
- **Let something not serve the theme.** A running joke, an odd neighbor, a digression with its own life. It lowers `thematic_unity` (4.74 AI vs. 4.41 human) and adds texture.
- **Lower the moral pressure.** Not every story needs a central ethical question. Let the stakes be practical: money, a deadline, a lie that has to hold until Friday.

### B. Stop performing the body and the senses
AI-elevated: embodied emotion 81% vs. 38%, olfactory imagery 82% vs. 57%, setting-as-mirror 4.07 vs. 3.58.
- **Name some feelings.** "He was jealous, and he knew it was stupid." Humans use explicit emotion labels 29% of the time, AI 8%.
- **Use behavior instead of physiology.** Replace "her chest tightened" with what she *does*: hangs up, re-alphabetizes the spice rack, goes for a drive with no destination. Use this alongside named feelings, not instead of them.
- **Drop the smell beat** unless smell matters to the plot. Coffee, rain and antiseptic are the usual suspects.
- **Unhook the weather from the mood.** Let it be sunny at the funeral. Stop rooms dimming when characters feel low.
- **Thin the sensory layer and the nature writing**, unless the story is about the land.
- **Leave some interiors closed.** Don't narrate every motive. Let a character do something the narration doesn't explain.

### C. Make the structure less tidy
AI-elevated: no subplots 79% vs. 57%, protagonist-choice resolution 69% vs. 46%, internal-acceptance resolution 47% vs. 27%, external-description introduction 52% vs. 30%, causal continuity 4.20 vs. 3.92.
- **Add a thematically parallel subplot.** Humans have one 42% of the time, AI 21%. It should be a second line of action with its own stakes that rhymes with the main one, such as a sister's divorce running alongside the protagonist's business failing.
- **Let the world resolve, or complicate, the ending.** Instead of the protagonist's epiphany fixing things, let an outside event, another person's decision or luck settle it. Or leave the outcome open.
- **Avoid the acceptance ending.** "She finally made peace with…" is the AI-typical resolution. Change the external situation, or leave it unresolved.
- **Break the single causal chain.** Add a coincidence, a lead that goes nowhere, an interruption that doesn't pay off, an event that happens for reasons the story never explains.
- **Introduce the protagonist mid-conversation or through someone else's account**, not with a paragraph of appearance and bearing. The human fingerprint is introduction in dialogue.
- **Get to the trouble sooner** (pre-threat investment 2.99 vs. 2.76). Don't spend the first act making us love the character before anything happens.
- **Don't open with an establishing shot** every time. Opening spatial grounding is AI-elevated, so start with a voice, a line of talk or a situation.

### D. Engage the outside world
Human-elevated: named references 47% vs. 24%, balanced explicit/implicit mix 37% vs. 16%.
- **Name real things.** The actual song, the actual book, the brand of cigarettes, the street, the TV show from 1994. AI tends to fall back on "an old song", "a novel she'd loved".
- **Mix named references with quieter echoes** instead of relying only on vague allusion.

### E. Acknowledge the reader, when the voice allows it
Human-elevated: fourth-wall permeability 0.67 vs. 0.39, direct reader address 0.28 vs. 0.07.
- A narrator who knows they're telling a story: "I'm getting ahead of myself." "You'll want to know about the dog."
- Use sparingly and only if the voice supports it. One aside can change the texture of a whole piece. Ten becomes a gimmick.

### F. Complicate time
Human-elevated: chronological discontinuity 2.40 vs. 2.12, anachrony 2.58 vs. 2.31, delayed disclosure 1.96 vs. 1.68, recontextualization 3.28 vs. 2.95.
- **Reorder the telling.** Open at the end, at the funeral or the arrest, then go back. Or braid two timelines.
- **Use a flashback or flash-forward that does work.** It should withhold or reveal something, not just supply backstory.
- **Plant, then recontextualize.** Design a late revelation that changes what an earlier scene meant, so a reader would want to reread it. The human fingerprint is back-loaded revelation pacing.
- **Jump over time.** Skip weeks or years between sections instead of narrating continuously.

### G. Widen the range
Human-elevated: more locales (1.34 vs. 1.08), more dialogue (2.95 vs. 2.70), ambivalent protagonist (59% vs. 38%).
- **Make the protagonist's choices morally mixed.** Let them do something the story doesn't forgive or condemn.
- **Move the story through more places.**
- **Let people talk more**, and let dialogue carry scenes the narration would otherwise summarize.

## Know your own fingerprint

If you are the model writing, check the habits the paper attributes to you. Claude is listed first because this skill most often runs on Claude. See `fingerprints.md` for the full lists.
- **Claude:** flat escalation. Let events actually build and break, and allow an "avalanche" ending. Vary the event types. Skip the epilogue. Try subverting a convention instead of honoring it. Vary the narrative voice.
- **GPT:** gossip as the engine, and a narrator looking back across decades. Try present-tense immediacy and different plot mechanisms.
- **Gemini:** tidy endings, long denouements, bleak and oppressive settings, external description of characters.
- **DeepSeek:** front-loaded context, and story-within-a-story scenes.
- **Kimi:** in medias res with in-action introductions, and generic choices overall.

## Revision loop

1. Annotate the draft with `core-features.md` and run `python scripts/score_story.py score annotation.json`.
2. From the AI-leaning features with the largest contributions, choose the 4–6 moves that best fit the story.
3. Rewrite at the level of scenes and structure.
4. Re-annotate the revision honestly and score it again. Report the before and after. If a feature didn't move, say so. Don't inflate the second annotation.
5. Stop when the story reads better and the main AI-typical patterns are gone. A low index isn't the goal in itself.

## Planning sheet for a new story

Before drafting, decide these on purpose and write them down. Otherwise the defaults drift toward the AI cluster.
- **Order of telling:** linear, or where does it start and what does it withhold?
- **Subplot:** what is the second line of action, and how does it rhyme with the main one?
- **Ending:** who or what resolves it, and does the external situation change? What is left open?
- **Theme:** state it to yourself in one line, then decide where it will *not* appear on the page.
- **Protagonist:** what do they do that a reader could disagree with?
- **First appearance:** how do we meet them? Not a description paragraph.
- **Named references:** two or three real names (songs, places, books, brands) that belong in this world.
- **Emotion:** which feelings get named outright, which are shown through behavior, and which are kept unreadable?
- **Narrator:** does the narrator know there is a reader?
