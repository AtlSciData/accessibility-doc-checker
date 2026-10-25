from app.scoring import score, penalty


def test_no_violations_scores_100():
    assert score([]) == 100


def test_one_serious_node():
    assert score([{"impact": "serious", "nodes": 1}]) == 93


def test_cap_limits_a_repeated_rule():
    # 5 critical nodes count as 3 (cap): 3 * 10 = 30
    assert score([{"impact": "critical", "nodes": 5}]) == 70


def test_penalties_add_up_across_rules():
    v = [{"impact": "critical", "nodes": 1},   # 10
         {"impact": "moderate", "nodes": 2}]   # 6
    assert score(v) == 84


def test_score_never_below_zero():
    v = [{"impact": "critical", "nodes": 3}] * 10  # 300 penalty
    assert score(v) == 0


def test_missing_or_unknown_impact_counts_as_minor():
    assert penalty(None, 2) == 2
    assert penalty("weird", 1) == 1


def test_same_input_same_score():
    v = [{"impact": "serious", "nodes": 2}, {"impact": "minor", "nodes": 9}]
    assert score(v) == score(list(v))


def test_best_practice_only_rules_are_not_scored():
    from app.scoring import score
    v = [
        {"impact": "moderate", "nodes": 1, "tags": ["cat.keyboard", "best-practice"]},
        {"impact": "serious", "nodes": 1, "tags": ["wcag2a", "wcag311"]},
    ]
    assert score(v) == 93
