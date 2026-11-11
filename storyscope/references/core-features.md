# The 30 StoryScope core features: annotation guide

Source: Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction* (COLM 2026, arXiv:2604.03136), Tables 1, 14, 15 and 16. The paper found these 30 features separate human from AI fiction consistently across five models: Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2 and Kimi K2.5. A classifier on these 30 alone reached 84.8% macro-F1 for human vs. AI on stories of about 5,000 words.

How to use this file: read the whole story first. Then answer each question below about the **whole story**, not one scene. Put a short quote or scene pointer in `evidence` for every answer. The key in `code` is the key `scripts/score_story.py` expects. Use `null` only when a feature truly cannot apply, for example `dialogue_functions` in a story with no dialogue.

The numbers are the paper's human vs. AI averages: means for 1–5 scales and 0-indexed ordinals, prevalence for options. They describe populations. A single human story can sit on the AI side of several features, so judge what is on the page and don't nudge answers toward a verdict.

Contents: [A. Thematic over-determination](#a-thematic-over-determination-ai-elevated) · [B. Sensory & embodied performativity](#b-sensory--embodied-performativity-ai-elevated) · [C. Structural streamlining](#c-structural-streamlining-ai-elevated) · [D. Intertextual richness](#d-intertextual-richness-human-elevated) · [E. Reader engagement](#e-reader-engagement-human-elevated) · [F. Temporal complexity](#f-temporal-complexity-human-elevated) · [G. Narrative diversity](#g-narrative-diversity-human-elevated)

NarraBench dimension codes: SIT = situatedness, PLT = plot, EVT = event, SET = setting, AGENT = agent, PER = perspective, REV = revelation, TMP = time.

---

## A. Thematic over-determination (AI-elevated)

The paper's summary: "AI spells out meaning rather than trusting the reader to infer it."

| code | question | values | human | AI |
|---|---|---|---|---|
| `thematic_explicitness` (SIT, scale) | How explicitly does the story articulate its themes or morals? | 1 = left entirely to inference … 5 = stated outright | 3.28 | 3.94 |
| `moral_philosophical_weighting` (SIT, scale) | How heavily does the story foreground moral or philosophical questions? | 1–5 | 3.26 | 3.68 |
| `thematic_unity` (PLT, scale) | To what extent do subplots and flourishes serve a central thematic concern? | 1–5 | 4.41 | 4.74 |
| `narratorial_thematic_commentary` (SIT, binary) | Does the narrator explicitly comment on themes beyond the characters' perspectives? | true / false | 52% yes | 77% yes |
| `dialogue_functions` (PER, multi) | What main functions does dialogue serve? | advance_plot, reveal_character, worldbuilding, philosophical_debate, comic | 34% philosophical | 59% philosophical |
| `reference_explicitness` (SIT, cat) | Are intertextual gestures primarily explicit or diffuse? | none, explicit_named, implicit_echoes, balanced_mix | 50% implicit · 37% balanced | 72% implicit · 16% balanced |

Annotation notes:
- **Thematic explicitness:** look for sentences that name the lesson, such as "She understood now that grief was just love with nowhere to go." One such line near the end is already a 4. Several, or a closing paragraph of reflection, makes it a 5.
- **Narratorial commentary:** `true` when the *narrator*, not a character in dialogue, generalizes about life, love, memory or the theme. The paper's example: "a grieving character's arc will typically end with the narrator stating the lesson learned."
- **Thematic unity:** 5 when every scene, image and minor character points at the same idea. Lower when material is there for texture, comedy or its own sake.
- **Philosophical debate:** include it when characters trade positions about meaning, ethics, memory or what it is to be human. Ordinary disagreement about events doesn't count.
- **Reference explicitness:** `implicit_echoes` means vague allusion ("a story her grandmother used to tell", "an old song") with nothing named. `explicit_named` means real, named works, brands, places or people. `balanced_mix` means both. `none` means no intertextual gestures at all.

## B. Sensory & embodied performativity (AI-elevated)

The paper: "Where a human author might write that a character 'felt afraid,' AI renders fear as a tightening chest, cold sweat, and dimming lamplight."

| code | question | values | human | AI |
|---|---|---|---|---|
| `emotional_expression` (AGENT, cat) | How are characters' emotions most commonly conveyed? | explicit_labels, embodied_metaphors, behavioral_cues, ambiguous | 38% embodied · 29% labels | 81% embodied · 8% labels |
| `setting_as_psychological_mirror` (SET, scale) | To what degree does the physical environment mirror characters' inner states? | 1–5 | 3.58 | 4.07 |
| `environmental_emphasis` (SET, scale) | How prominent is the natural environment or ecology in the narrative? | 1–5 | 2.83 | 3.21 |
| `sensory_modalities` (SET, multi) | Which sensory modalities does the story most frequently engage? | visual, auditory, olfactory, tactile, gustatory, kinesthetic | 57% olfactory | 82% olfactory |
| `sensory_density` (SET, scale) | How dense is sensory description across the narrative? | 1 = minimal … 5 = lush | 3.66 | 3.93 |
| `interior_access_depth` (PER, scale) | How deep into characters' inner life does narration go? | 1–5 | 3.67 | 3.93 |

Annotation notes:
- **Emotional expression:** pick the *dominant* mode.
  - `embodied_metaphors`: emotion as physical sensation or bodily figure ("her throat tightened", "something cold settled in his stomach").
  - `explicit_labels`: the feeling is named ("he was furious", "she felt ashamed").
  - `behavioral_cues`: we infer the feeling from actions and choices (he washes the same cup three times), not from body sensation.
  - `ambiguous`: the feeling is deliberately left unreadable.
- **Setting as mirror:** rain at the funeral and a storm breaking as the argument peaks score high. Weather and rooms that ignore the characters' moods score low.
- **Olfactory:** list it when smell recurs or is used for effect, such as coffee, rain on asphalt, old paper or antiseptic. One passing mention doesn't make it a dominant modality.

## C. Structural streamlining (AI-elevated)

The paper: "AI favors single-track narratives with fewer loose ends; human stories are messier."

| code | question | values | human | AI |
|---|---|---|---|---|
| `causal_chain_continuity` (EVT, scale) | How continuous is the single causal chain from inciting incident to ending? | 1–5 | 3.92 | 4.20 |
| `spatial_granularity` (SET, ordinal) | How fine-grained is the story's depiction of physical space? | 0 very_low · 1 low · 2 moderate · 3 high | 2.27 | 2.53 |
| `resolution_agency` (PLT, cat) | Is the resolution driven by the protagonist's choices or by external events? | protagonist_choice, mixed, external_fate | 46% choice | 69% choice |
| `character_introduction` (AGENT, cat) | What narrative device primarily introduces the central character? | external_description, in_action, inner_thought, dialogue, others_reports | 30% external | 52% external |
| `subplot_integration` (PLT, cat) | How directly do subplots echo the central theme? | no_subplots, thematically_parallel, contrasting, independent | 57% none · 42% parallel | 79% none · 21% parallel |
| `resolution_mode` (EVT, cat) | Is the main event chain resolved through internal acceptance or external action? | resolved_externally, resolved_internally, unresolved | 27% internal | 47% internal |
| `opening_spatial_grounding` (SET, ordinal) | How clearly does the opening ground the reader in a specific physical setting? | 0 none_or_vague · 1 minimal · 2 clear_local · 3 clear_local_and_global | 2.12 | 2.33 |
| `pre_threat_investment` (REV, scale) | How much does the story build investment in characters before major jeopardy? | 1–5 | 2.76 | 2.99 |

Annotation notes:
- **Causal chain:** 5 means every event is caused by the previous one, from the first clue to the grand reveal. Lower it for coincidences, dead ends, unrelated interruptions, parallel threads or events that never pay off.
- **Resolution mode:** `resolved_internally` means the ending is an acceptance, an understanding, forgiveness or making peace, while the external situation barely changes.
- **Subplot integration:** a subplot is a second line of action with its own stakes, not just a backstory flashback. `thematically_parallel` means it mirrors the main theme from another angle.
- **Character introduction:** how the reader first meets the protagonist. A paragraph of appearance and bearing is `external_description`. Meeting them mid-conversation is `dialogue`.
- Spatial granularity levels 0–3 and opening-grounding level names are reconstructed from the paper's "very_low–high" and "none/vague … clear local+global" ranges. The means are over 0-indexed integer codes (Table 16).

## D. Intertextual richness (human-elevated)

The paper: AI "avoids naming real brands, places, or works."

| code | question | values | human | AI |
|---|---|---|---|---|
| `intertextual_strategies` (SIT, multi) | What kinds of intertextual engagement does the story employ? | explicit_named_reference, retelling, pastiche, myth_or_religion, self_referential | 47% named | 24% named |

(`reference_explicitness` → `balanced_mix`, from section A, is the other human-elevated intertextual signal: 37% vs. 16%.)

- `explicit_named_reference`: the story names a real book, song, film, author, artist, brand or historical text, such as a character humming Patsy Cline or a copy of *Middlemarch* on the nightstand.

## E. Reader engagement (human-elevated)

The paper: "Human writing acknowledges its audience as a co-participant (e.g., an aside to 'you, dear reader'); AI writes as though no one is watching."

| code | question | values | human | AI |
|---|---|---|---|---|
| `fourth_wall_permeability` (SIT, ordinal) | To what extent does the story break the boundary between story-world and reader? | 0 none · 1 subtle · 2 overt · 3 radical | 0.67 | 0.39 |
| `direct_reader_address` (PER, ordinal) | How often does the text directly address the reader? | 0 never · 1 occasional_asides · 2 frequent_or_structural | 0.28 | 0.07 |

- **Fourth wall:** `subtle` covers a narrator who is aware of telling a story ("I'll get to the dog in a minute", "you'll have guessed by now"). `overt` means the story openly talks about being a story. `radical` means metafiction that collapses the frame.
- The level names between the endpoints are reconstructed. The paper gives "1 (no breaking)–4 (radical violations)" and reports means over 0-indexed codes.

## F. Temporal complexity (human-elevated)

The paper: "a human mystery might open at the funeral and spiral backward through decades, while AI tells the same story from first clue to the grand reveal."

| code | question | values | human | AI |
|---|---|---|---|---|
| `recontextualization_depth` (REV, scale) | How extensively does a revelation force reinterpretation of earlier scenes? | 1 = none … 5 = complete rereading | 3.28 | 2.95 |
| `chronological_discontinuity` (TMP, scale) | How often does the narrative jump across time? | 1–5 | 2.40 | 2.12 |
| `nonlinear_delayed_disclosure` (REV, scale) | To what extent does the story use time jumps to stage revelations? | 1 = linear … 5 = heavily fragmented | 1.96 | 1.68 |
| `anachrony_intensity` (TMP, scale) | How heavily does the narrative rely on flashbacks or flash-forwards? | 1 = absent … 5 = dominant | 2.58 | 2.31 |

- **Recontextualization:** don't count a twist that only adds information. Count one that changes what earlier scenes *meant*.
- **Delayed disclosure:** the order of telling is arranged so that a key fact arrives late *because* of the structure. A character simply not mentioning something doesn't count.

## G. Narrative diversity (human-elevated)

The paper: human stories "resist the pull to a narrow set of defaults."

| code | question | values | human | AI |
|---|---|---|---|---|
| `location_variety` (SET, ordinal) | How many distinct physical locales does the story inhabit? | 0 single · 1 few · 2 many · 3 multiworld | 1.34 | 1.08 |
| `dialogue_proportion` (PER, scale) | What proportion of the text is direct dialogue vs. narration? | 1 = no dialogue … 5 = dialogue dominates | 2.95 | 2.70 |
| `moral_polarity` (PLT, cat) | Does the narrative frame the protagonist's choices as morally clear or ambiguous? | clearly_positive, ambivalent, clearly_negative | 59% ambivalent | 38% ambivalent |

(`subplot_integration` → `thematically_parallel` at 42% vs. 21% and `emotional_expression` → `explicit_labels` at 29% vs. 8% also sit in this theme in Table 16.)

- **Location variety:** "few" means two or three distinct places. "Many" means four or more. "Multiworld" means separate worlds, realms or radically distinct planes. These intermediate labels are reconstructed from the paper's "single–multiworld" range.
- **Moral polarity:** `clearly_positive` means the story endorses the protagonist's choices. `ambivalent` means it leaves real doubt about whether they did right.

---

## Output format for an annotation

Get a blank copy with `python scripts/score_story.py template`. It produces this shape:

```json
{
  "meta": {"title": "…", "word_count": 2400, "annotator_notes": "…"},
  "features": {
    "thematic_explicitness": {"value": 4, "evidence": "Final paragraph: 'She finally understood that…'"},
    "dialogue_functions": {"value": ["advance_plot", "philosophical_debate"], "evidence": "Kitchen scene debate about memory"},
    "fourth_wall_permeability": {"value": 0, "evidence": "Closed third-person, no narrator awareness"}
  }
}
```

Ordinals accept the integer code or the level name. Extra fields such as `question` and `allowed` are ignored.
