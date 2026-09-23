from ultron import summary


def _c(i, pred, st="s"):
    return {"id": f"clm_{i}", "predicate": pred, "statement": st, "confidence": 0.9}


def test_summary_cites_only_real_claims_and_orders_security_first():
    claims = [_c(1, "imports_symbol")] * 3 + [_c(2, "contains_hardcoded_secret", "api token in etc/x.conf"), _c(3, "uses_risky_api", "calls strcpy")]
    title, body, cited = summary.summarize(claims, "fw.bin")
    assert title == "RE summary: fw.bin"
    assert cited == ["clm_2", "clm_3"]
    assert body.index("contains hardcoded secret") < body.index("uses risky api")
    assert "api token in etc/x.conf [clm_2]" in body and "| imports_symbol | 3 |" in body


def test_summary_caps_per_predicate():
    claims = [_c(i, "suspicious_string") for i in range(9)]
    _, body, cited = summary.summarize(claims, "x")
    assert len(cited) == summary.PER_PREDICATE and "and 4 more" in body


def test_structured_statements_and_confidence_render_readably():
    c = {"id": "clm_x", "predicate": "uses_risky_api", "statement": {"api": "system", "category": "command_exec"},
         "confidence": {"combined": 0.99, "max": 0.9}}
    _, body, _ = summary.summarize([c], "x")
    assert "- api: system, category: command_exec [clm_x] (confidence 0.99)" in body
