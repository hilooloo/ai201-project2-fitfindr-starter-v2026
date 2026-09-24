"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()

    def size_matches(item_size: str, target_size: str) -> bool:
        item_size_lower = item_size.lower()
        target_lower = target_size.lower()
        if item_size_lower == target_lower:
            return True
        tokens = re.split(r"[/ ()]+", item_size_lower)
        return target_lower in [t for t in tokens if t]

    candidates = []
    for item in listings:
        if max_price is not None:
            try:
                if float(item["price"]) > float(max_price):
                    continue
            except (TypeError, ValueError):
                continue
        if size is not None:
            if not size_matches(item.get("size", ""), size):
                continue
        candidates.append(item)

    desc_tokens = [t for t in re.split(r"\W+", description.lower()) if t]

    scored = []
    for item in candidates:
        text_parts = [
            item.get("title", ""),
            item.get("description", ""),
            item.get("category", ""),
            " ".join(item.get("style_tags", []) or []),
            " ".join(item.get("colors", []) or []),
            item.get("brand") or "",
        ]
        item_text = " ".join(text_parts).lower()
        score = sum(1 for token in desc_tokens if token in item_text)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    return [item for _, item in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    def describe_item(item: dict) -> str:
        parts = [
            item.get("title") or item.get("name", ""),
            f"({item.get('category', '')})",
        ]
        colors = item.get("colors") or []
        if colors:
            parts.append("colors: " + ", ".join(colors))
        tags = item.get("style_tags") or []
        if tags:
            parts.append("style: " + ", ".join(tags))
        return " — ".join(p for p in parts if p)

    new_item_desc = describe_item(new_item)

    items = wardrobe.get("items") or []

    if not items:
        prompt = (
            "A user is considering thrifting this item:\n"
            f"{new_item_desc}\n\n"
            "They don't have any wardrobe items on file yet. Give general "
            "styling advice for this piece — what kinds of items, colors, "
            "and styles it would pair well with, and one or two outfit ideas "
            "using pieces someone might typically own."
        )
    else:
        wardrobe_lines = "\n".join(f"- {describe_item(i)}" for i in items)
        prompt = (
            "A user is considering thrifting this item:\n"
            f"{new_item_desc}\n\n"
            "Here is their current wardrobe:\n"
            f"{wardrobe_lines}\n\n"
            "Suggest 1-2 cohesive outfits that pair the new item with "
            "specific pieces from their wardrobe. Name the wardrobe items "
            "explicitly by their description."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "No outfit suggestion provided to generate a fit card."

    title = new_item.get("title", "this piece")
    price = new_item.get("price", "")
    platform = new_item.get("platform", "")

    prompt = (
        "Write a short social media caption (2-4 sentences) for a thrift "
        "flip post. It should read like a real, enthusiastic post from "
        "someone excited about their find — not a product description.\n\n"
        f"Item: {title}\n"
        f"Price: ${price}\n"
        f"Found on: {platform}\n"
        f"Outfit idea: {outfit}\n\n"
        "Naturally mention the item name, the price (with a '$'), and the "
        "platform once each. Capture the overall styling vibe, and end with "
        "at least two relevant hashtags (like #thrifted or #streetwear)."
    )

    return generate(prompt)
