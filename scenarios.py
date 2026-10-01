"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

One scenario per criterion below (criteria.md has five). Each scenario lists
five *different* queries in "queries" — one per try — rather than repeating a
single query five times. For criteria 2, 3, and 5 the checked behavior is
deterministic Python logic (a branch, a dict reference, a price comparison),
so five identical tries would just prove the same thing five times; five
different items/queries is a stronger test of the same rule. Criterion 1 and 4
involve the model, so variety also guards against accidentally re-testing one
easy case.
"""

SCENARIOS = [
    {
        # Criterion 1 — a matching query completes all three tools.
        "name": "matching query completes",
        "criterion": 1,
        "wardrobe": "example",
        "queries": [
            "vintage graphic tee under $30",
            "black leather jacket",
            "denim jacket under $50",
            "cargo pants",
            "oversized hoodie",
        ],
    },
    {
        # Criterion 2 — an impossible query stops before suggest_outfit.
        "name": "impossible query stops early",
        "criterion": 2,
        "wardrobe": "example",
        "queries": [
            "neon pink astronaut spacesuit helmet with laser horns under $5",
            "designer ballgown size XXS under $5",
            "cyberpunk hoverboard boots under $1",
            "victorian steampunk submarine goggles under $2",
            "medieval titanium knight armor under $3",
        ],
    },
    {
        # Criterion 3 — the item search_listings selected is the same dict
        # suggest_outfit receives (session["selected_item"]'s id/title match).
        "name": "selected item state matches what reaches suggest_outfit",
        "criterion": 3,
        "wardrobe": "example",
        "queries": [
            "vintage graphic tee under $30",
            "black leather jacket",
            "denim jacket under $50",
            "cargo pants",
            "oversized hoodie",
        ],
    },
    {
        # Criterion 4 — the fit card names the price and at least one hashtag.
        "name": "fit card mentions price and a hashtag",
        "criterion": 4,
        "wardrobe": "example",
        "queries": [
            "vintage graphic tee under $30",
            "black leather jacket",
            "denim jacket under $50",
            "cargo pants",
            "oversized hoodie",
        ],
    },
    {
        # Criterion 5 — every returned listing respects the price ceiling.
        "name": "price ceiling respected",
        "criterion": 5,
        "wardrobe": "example",
        "queries": [
            "graphic tee under $20",
            "leather jacket under $30",
            "denim jacket under $25",
            "oversized hoodie under $40",
            "cargo pants under $35",
        ],
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "criterion": None,
        "wardrobe": "empty",
        "queries": ["denim jacket under $50"],
    },
]

WARDROBES = ("example", "empty")


def _queries(scenario: dict) -> list[str]:
    """A scenario's queries, whether it uses "queries" (a list) or "query" (one)."""
    queries = scenario.get("queries")
    if queries:
        return list(queries)
    query = scenario.get("query", "")
    return [query] if query else []


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        queries = _queries(scenario)
        if not queries or any(not q.strip() for q in queries):
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
