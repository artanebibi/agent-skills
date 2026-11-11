#!/usr/bin/env python3
"""Score a story annotation against the StoryScope core narrative features.

StoryScope (Russell et al., COLM 2026, arXiv:2604.03136) found 30 "core"
narrative features that separate human from AI fiction across five LLMs.
Table 16 of the paper reports the human mean and the AI mean (or prevalence)
for each one. This script turns a filled-in annotation of those 30 features
into a per-feature lean and an overall index.

How the score works (and what it is not):
  * Option features (binary / categorical / multi-select) use the paper's
    human-vs-AI prevalences as a naive-Bayes log-likelihood ratio.
  * Scale and ordinal features have no published variance, so they use a
    Gaussian log-likelihood ratio around the human and AI means with an
    assumed standard deviation (1.0 for 1-5 scales, 0.8 for 0-3 ordinals).
  * The features are correlated (they come in themes), so the summed log
    ratio is damped before it becomes a 0-100 index.
  * This is NOT the paper's XGBoost classifier and it is not calibrated.
    It is a transparent heuristic that says which way each narrative choice
    leans and by roughly how much. Positive = more typical of AI stories.

Usage:
  python score_story.py template            # print a blank annotation
  python score_story.py score ANNOTATION    # human-readable report
  python score_story.py score ANNOTATION --json
"""

import json
import math
import sys

SCALE_SD = 1.0      # assumed SD for 1-5 Likert features
ORDINAL_SD = 0.8    # assumed SD for 0-indexed ordinal features
PROB_FLOOR = 0.02   # keeps log ratios finite for near-zero prevalences
CLIP = 1.5          # max absolute contribution of one feature
DAMPING = 0.5       # shrinks the sum because the 30 features are correlated

THEMES = {
    "over_determination": "Thematic over-determination (AI-elevated)",
    "embodied": "Sensory & embodied performativity (AI-elevated)",
    "streamlining": "Structural streamlining (AI-elevated)",
    "intertext": "Intertextual richness (human-elevated)",
    "reader": "Reader engagement (human-elevated)",
    "temporal": "Temporal complexity (human-elevated)",
    "diversity": "Narrative diversity (human-elevated)",
}

# kind:
#   scale    1-5 integer; params = (human_mean, ai_mean)
#   ordinal  0-indexed integer code into `levels`; params = (human_mean, ai_mean)
#   binary   true/false; probs = (p_human, p_ai) for true
#   cat      one option; probs = {option: (p_human, p_ai)} for the options the
#            paper reports; all other options share the residual probability
#   multi    list of options; probs = {option: (p_human, p_ai)}
FEATURES = [
    # --- Thematic over-determination (AI-elevated) ---
    dict(key="thematic_explicitness", name="Thematic Explicitness & Moralizing",
         dim="SIT", theme="over_determination", kind="scale", params=(3.28, 3.94),
         question="How explicitly does the story articulate its themes or morals? (1 = left entirely to the reader, 5 = stated outright)"),
    dict(key="moral_philosophical_weighting", name="Moral / Philosophical Weighting",
         dim="SIT", theme="over_determination", kind="scale", params=(3.26, 3.68),
         question="How heavily does the story foreground moral or philosophical questions? (1-5)"),
    dict(key="thematic_unity", name="Thematic Unity",
         dim="PLT", theme="over_determination", kind="scale", params=(4.41, 4.74),
         question="To what extent do subplots and flourishes serve a central thematic concern? (1-5)"),
    dict(key="narratorial_thematic_commentary", name="Narratorial Thematic Commentary",
         dim="SIT", theme="over_determination", kind="binary", probs=(0.52, 0.77),
         question="Does the narrator explicitly comment on themes beyond the characters' perspectives? (true/false)"),
    dict(key="dialogue_functions", name="Dialogue Function",
         dim="PER", theme="over_determination", kind="multi",
         options=["advance_plot", "reveal_character", "worldbuilding", "philosophical_debate", "comic"],
         probs={"philosophical_debate": (0.34, 0.59)},
         question="What main functions does dialogue serve? (list all that apply; [] if no dialogue)"),
    dict(key="reference_explicitness", name="Reference Explicitness",
         dim="SIT", theme="over_determination", kind="cat",
         options=["none", "explicit_named", "implicit_echoes", "balanced_mix"],
         probs={"implicit_echoes": (0.50, 0.72), "balanced_mix": (0.37, 0.16)},
         question="Are intertextual gestures primarily explicit or diffuse?"),
    # --- Sensory & embodied performativity (AI-elevated) ---
    dict(key="emotional_expression", name="Dominant Emotional Expression",
         dim="AGENT", theme="embodied", kind="cat",
         options=["explicit_labels", "embodied_metaphors", "behavioral_cues", "ambiguous"],
         probs={"embodied_metaphors": (0.38, 0.81), "explicit_labels": (0.29, 0.08)},
         question="How are characters' emotions most commonly conveyed?"),
    dict(key="setting_as_psychological_mirror", name="Setting as Psychological Mirror",
         dim="SET", theme="embodied", kind="scale", params=(3.58, 4.07),
         question="To what degree does the physical environment mirror characters' inner states? (1-5)"),
    dict(key="environmental_emphasis", name="Environmental & Ecological Emphasis",
         dim="SET", theme="embodied", kind="scale", params=(2.83, 3.21),
         question="How prominent is the natural environment or ecology in the narrative? (1-5)"),
    dict(key="sensory_modalities", name="Dominant Sensory Modalities",
         dim="SET", theme="embodied", kind="multi",
         options=["visual", "auditory", "olfactory", "tactile", "gustatory", "kinesthetic"],
         probs={"olfactory": (0.57, 0.82)},
         question="Which sensory modalities does the story most frequently engage? (list)"),
    dict(key="sensory_density", name="Sensory Density",
         dim="SET", theme="embodied", kind="scale", params=(3.66, 3.93),
         question="How dense is sensory description across the narrative? (1 = minimal, 5 = lush)"),
    dict(key="interior_access_depth", name="Depth of Interior Access",
         dim="PER", theme="embodied", kind="scale", params=(3.67, 3.93),
         question="How deep into characters' inner life does narration go? (1-5)"),
    # --- Structural streamlining (AI-elevated) ---
    dict(key="causal_chain_continuity", name="Continuity of Causal Chain",
         dim="EVT", theme="streamlining", kind="scale", params=(3.92, 4.20),
         question="How continuous is the single causal chain from inciting incident to ending? (1-5)"),
    dict(key="spatial_granularity", name="Spatial Granularity Level",
         dim="SET", theme="streamlining", kind="ordinal", params=(2.27, 2.53),
         levels=["very_low", "low", "moderate", "high"],
         question="How fine-grained is the story's depiction of physical space? (0 = very_low ... 3 = high)"),
    dict(key="resolution_agency", name="Agency in Resolution",
         dim="PLT", theme="streamlining", kind="cat",
         options=["protagonist_choice", "mixed", "external_fate"],
         probs={"protagonist_choice": (0.46, 0.69)},
         question="Is the resolution driven by the protagonist's choices or by external events?"),
    dict(key="character_introduction", name="Character Introduction",
         dim="AGENT", theme="streamlining", kind="cat",
         options=["external_description", "in_action", "inner_thought", "dialogue", "others_reports"],
         probs={"external_description": (0.30, 0.52)},
         question="What narrative device primarily introduces the central character?"),
    dict(key="subplot_integration", name="Subplot Integration",
         dim="PLT", theme="streamlining", kind="cat",
         options=["no_subplots", "thematically_parallel", "contrasting", "independent"],
         probs={"no_subplots": (0.57, 0.79), "thematically_parallel": (0.42, 0.21)},
         question="How directly do subplots echo the central theme?"),
    dict(key="resolution_mode", name="Mode of Resolution",
         dim="EVT", theme="streamlining", kind="cat",
         options=["resolved_externally", "resolved_internally", "unresolved"],
         probs={"resolved_internally": (0.27, 0.47)},
         question="Is the main event chain resolved through internal acceptance/understanding or external action?"),
    dict(key="opening_spatial_grounding", name="Opening Spatial Grounding",
         dim="SET", theme="streamlining", kind="ordinal", params=(2.12, 2.33),
         levels=["none_or_vague", "minimal", "clear_local", "clear_local_and_global"],
         question="How clearly does the opening ground the reader in a specific physical setting? (0-3)"),
    dict(key="pre_threat_investment", name="Pre-Threat Character Investment",
         dim="REV", theme="streamlining", kind="scale", params=(2.76, 2.99),
         question="How much does the story build investment in characters before major jeopardy? (1-5)"),
    # --- Intertextual richness (human-elevated) ---
    dict(key="intertextual_strategies", name="Intertextual Strategy Types",
         dim="SIT", theme="intertext", kind="multi",
         options=["explicit_named_reference", "retelling", "pastiche", "myth_or_religion", "self_referential"],
         probs={"explicit_named_reference": (0.47, 0.24)},
         question="What kinds of intertextual engagement does the story employ? (list; [] if none)"),
    # --- Reader engagement (human-elevated) ---
    dict(key="fourth_wall_permeability", name="Fourth-Wall Permeability",
         dim="SIT", theme="reader", kind="ordinal", params=(0.67, 0.39),
         levels=["none", "subtle", "overt", "radical"],
         question="To what extent does the story break the boundary between story-world and reader? (0-3)"),
    dict(key="direct_reader_address", name="Frequency of Direct Reader Address",
         dim="PER", theme="reader", kind="ordinal", params=(0.28, 0.07),
         levels=["never", "occasional_asides", "frequent_or_structural"],
         question="How often does the text directly address the reader? (0-2)"),
    # --- Temporal complexity (human-elevated) ---
    dict(key="recontextualization_depth", name="Depth of Recontextualization After Surprise",
         dim="REV", theme="temporal", kind="scale", params=(3.28, 2.95),
         question="How extensively does a revelation force reinterpretation of earlier scenes? (1 = none, 5 = complete rereading)"),
    dict(key="chronological_discontinuity", name="Degree of Chronological Discontinuity",
         dim="TMP", theme="temporal", kind="scale", params=(2.40, 2.12),
         question="How often does the narrative jump across time? (1-5)"),
    dict(key="nonlinear_delayed_disclosure", name="Nonlinear Framing for Delayed Disclosure",
         dim="REV", theme="temporal", kind="scale", params=(1.96, 1.68),
         question="To what extent does the story use time jumps to stage revelations? (1 = linear, 5 = heavily fragmented)"),
    dict(key="anachrony_intensity", name="Anachrony Intensity",
         dim="TMP", theme="temporal", kind="scale", params=(2.58, 2.31),
         question="How heavily does the narrative rely on flashbacks or flash-forwards? (1 = absent, 5 = dominant)"),
    # --- Narrative diversity (human-elevated) ---
    dict(key="location_variety", name="Location Variety Scope",
         dim="SET", theme="diversity", kind="ordinal", params=(1.34, 1.08),
         levels=["single", "few", "many", "multiworld"],
         question="How many distinct physical locales does the story inhabit? (0 = single, 1 = a few, 2 = many, 3 = multiple worlds/realms)"),
    dict(key="dialogue_proportion", name="Dialogue-to-Narration Proportion",
         dim="PER", theme="diversity", kind="scale", params=(2.95, 2.70),
         question="What proportion of the text is direct dialogue vs. narration? (1 = no dialogue, 5 = dialogue dominates)"),
    dict(key="moral_polarity", name="Moral Polarity Toward Protagonist",
         dim="PLT", theme="diversity", kind="cat",
         options=["clearly_positive", "ambivalent", "clearly_negative"],
         probs={"ambivalent": (0.59, 0.38)},
         question="Does the narrative frame the protagonist's choices as morally clear or ambiguous?"),
]


def _p(x):
    return min(max(x, PROB_FLOOR), 1 - PROB_FLOOR)


def _llr(p_h, p_a):
    return math.log(_p(p_a) / _p(p_h))


def _gauss_llr(x, h, a, sd):
    # log N(x; a, sd) - log N(x; h, sd)
    return (a - h) * (x - (a + h) / 2.0) / (sd * sd)


def _clip(v):
    return max(-CLIP, min(CLIP, v))


def _unwrap(entry):
    if isinstance(entry, dict) and "value" in entry:
        return entry["value"], entry.get("evidence", "")
    return entry, ""


def _ordinal_code(f, value):
    if isinstance(value, str):
        if value not in f["levels"]:
            raise ValueError(f"{f['key']}: '{value}' is not one of {f['levels']}")
        return f["levels"].index(value)
    code = int(value)
    if not 0 <= code < len(f["levels"]):
        raise ValueError(f"{f['key']}: code {code} outside 0-{len(f['levels']) - 1}")
    return code


def score_feature(f, value):
    """Return (contribution, explanation) for one feature value."""
    kind = f["kind"]
    if kind == "scale":
        x = float(value)
        if not 1 <= x <= 5:
            raise ValueError(f"{f['key']}: scale value {x} outside 1-5")
        h, a = f["params"]
        return _gauss_llr(x, h, a, SCALE_SD), f"{x:g} (human mean {h}, AI mean {a})"
    if kind == "ordinal":
        x = _ordinal_code(f, value)
        h, a = f["params"]
        return (_gauss_llr(x, h, a, ORDINAL_SD),
                f"{f['levels'][x]} = {x} (human mean {h}, AI mean {a})")
    if kind == "binary":
        if not isinstance(value, bool):
            raise ValueError(f"{f['key']}: expected true/false, got {value!r}")
        p_h, p_a = f["probs"]
        c = _llr(p_h, p_a) if value else _llr(1 - p_h, 1 - p_a)
        return c, f"{'yes' if value else 'no'} (yes: human {p_h:.0%}, AI {p_a:.0%})"
    if kind == "cat":
        if value not in f["options"]:
            raise ValueError(f"{f['key']}: '{value}' is not one of {f['options']}")
        if value in f["probs"]:
            p_h, p_a = f["probs"][value]
            return _llr(p_h, p_a), f"{value} (human {p_h:.0%}, AI {p_a:.0%})"
        rest_h = 1 - sum(p[0] for p in f["probs"].values())
        rest_a = 1 - sum(p[1] for p in f["probs"].values())
        return (_llr(rest_h, rest_a),
                f"{value} (other options: human {max(rest_h, 0):.0%}, AI {max(rest_a, 0):.0%})")
    if kind == "multi":
        if not isinstance(value, list):
            raise ValueError(f"{f['key']}: expected a list, got {value!r}")
        bad = [v for v in value if v not in f["options"]]
        if bad:
            raise ValueError(f"{f['key']}: {bad} not in {f['options']}")
        total, parts = 0.0, []
        for opt, (p_h, p_a) in f["probs"].items():
            if opt in value:
                total += _llr(p_h, p_a)
                parts.append(f"has {opt} (human {p_h:.0%}, AI {p_a:.0%})")
            else:
                total += _llr(1 - p_h, 1 - p_a)
                parts.append(f"no {opt} (human {p_h:.0%}, AI {p_a:.0%} have it)")
        return total, "; ".join(parts)
    raise ValueError(f"unknown kind {kind}")


def band(index):
    if index >= 85:
        return "strongly AI-typical narrative choices"
    if index >= 65:
        return "leans AI-typical"
    if index > 35:
        return "mixed / inconclusive"
    if index > 15:
        return "leans human-typical"
    return "strongly human-typical narrative choices"


def score(annotation):
    feats = annotation.get("features", annotation)
    rows, skipped = [], []
    for f in FEATURES:
        if f["key"] not in feats:
            skipped.append(f["key"])
            continue
        value, evidence = _unwrap(feats[f["key"]])
        if value is None:
            skipped.append(f["key"])
            continue
        raw, explanation = score_feature(f, value)
        rows.append(dict(key=f["key"], name=f["name"], theme=f["theme"],
                         contribution=round(_clip(raw), 3), detail=explanation,
                         evidence=evidence))
    total = sum(r["contribution"] for r in rows)
    index = 100.0 / (1.0 + math.exp(-DAMPING * total))
    themes = {}
    for r in rows:
        themes.setdefault(r["theme"], 0.0)
        themes[r["theme"]] += r["contribution"]
    return dict(
        features_scored=len(rows),
        features_skipped=skipped,
        total_log_ratio=round(total, 3),
        ai_lean_index=round(index, 1),
        verdict=band(index),
        ai_leaning_features=sum(1 for r in rows if r["contribution"] > 0.05),
        human_leaning_features=sum(1 for r in rows if r["contribution"] < -0.05),
        themes={THEMES[k]: round(v, 3) for k, v in themes.items()},
        features=sorted(rows, key=lambda r: -r["contribution"]),
        note=("Heuristic built from StoryScope Table 16 means; not the paper's "
              "classifier and not calibrated. Positive contribution = more "
              "typical of AI stories. Never treat this as proof of authorship."),
    )


def template():
    out = {"meta": {"title": "", "word_count": 0, "annotator_notes": ""}, "features": {}}
    for f in FEATURES:
        if f["kind"] == "scale":
            allowed = "integer 1-5"
        elif f["kind"] == "ordinal":
            allowed = " | ".join(f"{i}={lvl}" for i, lvl in enumerate(f["levels"]))
        elif f["kind"] == "binary":
            allowed = "true | false"
        elif f["kind"] == "cat":
            allowed = " | ".join(f["options"])
        else:
            allowed = "list of: " + ", ".join(f["options"])
        out["features"][f["key"]] = {
            "question": f["question"], "allowed": allowed,
            "value": None, "evidence": "",
        }
    return out


def render(result):
    lines = [
        f"AI-lean index: {result['ai_lean_index']}/100  ->  {result['verdict']}",
        f"Features scored: {result['features_scored']}/30  "
        f"(AI-leaning {result['ai_leaning_features']}, human-leaning {result['human_leaning_features']})",
    ]
    if result["features_skipped"]:
        lines.append("Skipped (null/missing): " + ", ".join(result["features_skipped"]))
    lines.append("")
    lines.append("By theme (sum of contributions; + = AI-typical):")
    for name, v in sorted(result["themes"].items(), key=lambda kv: -kv[1]):
        lines.append(f"  {v:+.2f}  {name}")
    lines.append("")
    lines.append("Per feature (most AI-typical first):")
    for r in result["features"]:
        lines.append(f"  {r['contribution']:+.2f}  {r['name']}: {r['detail']}")
    lines.append("")
    lines.append(result["note"])
    return "\n".join(lines)


def main(argv):
    if len(argv) < 2 or argv[1] not in ("template", "score"):
        print(__doc__)
        return 2
    if argv[1] == "template":
        print(json.dumps(template(), indent=2))
        return 0
    if len(argv) < 3:
        print("usage: score_story.py score ANNOTATION.json [--json]")
        return 2
    with open(argv[2], encoding="utf-8") as fh:
        annotation = json.load(fh)
    try:
        result = score(annotation)
    except ValueError as exc:
        print(f"annotation error: {exc}", file=sys.stderr)
        return 1
    if "--json" in argv:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
