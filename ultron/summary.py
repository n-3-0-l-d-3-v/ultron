"""Deterministic post-analysis summary for the vault (no model involved).

Every line of the summary is a claim's own statement with its claim id, so the
note stays inside Ultron's evidence discipline: it never says anything the
claim store does not already say. The note is written to the vault's
``pending/`` folder, so a human reviews it before it counts as knowledge.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

# Security-relevant predicates, in the order a reviewer should read them.
HIGHLIGHT = (
    "contains_hardcoded_secret",
    "uses_risky_api",
    "suspicious_string",
    "binary_hardening",
    "embeds_component",
)
PER_PREDICATE = 5


def _fmt(statement: Any) -> str:
    if isinstance(statement, dict):
        return ", ".join(f"{k.replace('_', ' ')}: {v}" for k, v in statement.items()) or "(empty)"
    return str(statement or "(no statement)")


def _conf(conf: Any) -> str:
    if isinstance(conf, dict):
        conf = conf.get("combined", conf.get("max"))
    try:
        return f"{float(conf):.2f}"
    except (TypeError, ValueError):
        return "?"


def summarize(claims: list[dict[str, Any]], label: str) -> tuple[str, str, list[str]]:
    """Return (title, markdown body, cited claim ids)."""
    counts = Counter(c["predicate"] for c in claims)
    title = f"RE summary: {label}"
    lines = [f"Analysis of `{label}`: {len(claims)} claims across {len(counts)} predicates.", ""]
    lines.append("| predicate | claims |")
    lines.append("|---|---|")
    for pred, n in counts.most_common():
        lines.append(f"| {pred} | {n} |")
    cited: list[str] = []
    for pred in HIGHLIGHT:
        items = [c for c in claims if c["predicate"] == pred][:PER_PREDICATE]
        if not items:
            continue
        lines += ["", f"## {pred.replace('_', ' ')}"]
        for c in items:
            lines.append(f"- {_fmt(c.get('statement'))} [{c['id']}] (confidence {_conf(c.get('confidence'))})")
            cited.append(c["id"])
        extra = counts[pred] - len(items)
        if extra > 0:
            lines.append(f"- ...and {extra} more (`ultron query claims --predicate {pred}`)")
    lines += ["", "Every line above is a stored claim; verify with `ultron query claim <id>` before relying on it."]
    return title, "\n".join(lines), cited
