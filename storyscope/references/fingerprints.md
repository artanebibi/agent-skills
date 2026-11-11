# Per-source narrative fingerprints

Source: StoryScope (arXiv:2604.03136), Section 5 and Table 17. A fingerprint feature is one whose importance in the paper's six-way classifier (human vs. five LLMs) is concentrated in one source, and whose values for that source visibly differ from the rest. The number of fingerprints found per source: Human 32, Claude 26, GPT 11, Gemini 11, DeepSeek 7, Kimi 3.

**Read this as a weak hint, not attribution.**
- With every narrative feature and a trained classifier, the paper's six-way attribution reached only 68.4% macro-F1. It reached 77.3% once style was added.
- Per source, with narrative features only, F1 was: Human 88.5, Claude 77.1, GPT 73.0. DeepSeek, Gemini and Kimi came in at 55.2–59.6 and are mostly confused with each other, Gemini↔DeepSeek most of all.
- The models studied were Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2 and Kimi K2.5. Newer versions may differ.

Only name a likely model when several of its fingerprints show up together, and say how confident you are.

## Human

The paper calls human the most distinctive source. Its top fingerprints by uniqueness:
1. **Character introduction → in dialogue.** We first meet the protagonist through talk.
2. **Breadth of focalization → single focal character.**
3. **Narrator address mode → no direct address.** This is a narrower feature than the core "direct reader address" one. Human stories are still more likely overall to address the reader.
4. **Overall revelation pacing → back-loaded.** Key information arrives late.
5. **Literary ambition → crossover genre.**

Plus 27 more, including visibility of withholding, atmospheric techniques, subplot density, naming and twist placement.

Human stories are also **rarer** in narrative feature space. Their mean rarity percentile is 0.71, against 0.49 for AI stories. For a given prompt, the human version was the most unusual of the six 57.8% of the time, where chance is 16.7%.

## Claude: "keeps it cool"

The most distinctive of the five LLMs. Its stories are defined by restraint.
1. **Weak event escalation.** Intensity escalates less than in any other source. Expect quiet endings, not "avalanche" endings.
2. **Distinctive event-type diversity.** Table 17 doesn't say which direction, but the paper describes Claude's narrative voice as "the most uniform".
3. **Ending temporal scope → epilogue or flash-forward.** Claude favors epilogues.
4. **Dreams or visions as temporal distortion → no.** Claude avoids dream sequences.
5. **Setting mood → uncanny or haunted.**

It also takes a **reverent, continuist approach to literary tradition**, extending conventions rather than subverting them: 62% of Claude stories, against 39–56% for the other sources. Plus 21 more fingerprints, including event density, conflict modality, relationship trajectory, heteroglossia (Bakhtin's term for a mix of distinct voices and registers) and closure.

## GPT: "likes to gossip"

Socially oriented storytelling.
1. **Gossip and rumor as a plot mechanism**: 64%, against 44–55% for the others.
2. **Narrator temporal distance → distant retrospective.** The story is framed as a look back on events from years or decades ago.
3. **Reader-expectation strategy → subverts**: 41%, against 27–36% for other AI.
4. **Iterative or habitual narration → no.**
5. **Reconciliation or forgiveness → partial or ambiguous.**

It also has ensemble-heavy social networks, at roughly human levels. Plus 6 more: community salience, social emphasis, reader competence, individualization and psychological depth.

## Gemini, DeepSeek and Kimi: "triplets"

These three form a confused cluster, but each has quirks.

**Gemini**
- Protagonist's social circle expands over the story.
- Speech is primarily direct.
- Global schema is a siege or ordeal.
- Characters are named with personal names.
- Frequent flashbacks.
- The tidiest endings and extended denouements.
- The bleakest settings: 88% tagged bleak and oppressive.
- The abstract adds that Gemini "defaults to external character description".

**DeepSeek**
- A visible, present narrator.
- Emotions shown through behavioral cues.
- A distinctive balance of plot against atmosphere.
- Backstory evenly interleaved.
- Embedded storytelling scenes, where characters tell stories.
- Crucial context front-loaded where other sources hold it back.
- Seasonal or cyclical time.

**Kimi**
- Character introduced in an action event.
- Opens in medias res.
- No explicit trait labeling.
- Kimi has the fewest fingerprints. The paper places it at "the generic center of the AI distribution", with no distinctive narrative choices.

## The shared AI cluster

All five models sit in one overlapping region of narrative space, apart from human stories.
- The mean distance between the human centroid and an AI centroid is 1.6× the mean distance between two AI centroids.
- Even the closest human–AI pair of centroids is farther apart than the most distant AI–AI pair.
- The six most-confused source pairs are all AI↔AI.

In practice: an AI-written story can usually be told from a human one far more reliably than one model's story can be told from another's.
