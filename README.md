# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr is an intelligent thrifting agent that helps users discover second-hand fashion pieces and seamlessly style them. A user provides a natural language search query specifying an aesthetic or item, optional size preferences, and a budget constraint. The agent parses the request, filters matching listings across platforms, cross-references candidate pieces with the user's existing wardrobe to suggest cohesive outfit pairings, and crafts a ready-to-post aesthetic caption. If no matching listings are found within the criteria, it halts early and provides clear recommendations on how to broaden the search.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
Searches the secondhand listings dataset and filters items matching query description keywords, an optional clothing size, and an optional maximum price threshold.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
`description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:**
A list of listing dicts, each containing `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list[str]), `size` (str), `condition` (str), `price` (float), `colors` (list[str]), `brand` (str or None), and `platform` (str).
- **When it has nothing:**
An empty list `[]`.

### `suggest_outfit`

- **What it does:**
Recommends styling pairings combining a newly selected thrift listing with complementary pieces from the user's saved wardrobe.
- **Inputs:**
`new_item` (dict containing `id`, `title`, `category`, `style_tags`, `colors`, and `price`), `wardrobe` (list[dict], each containing `id`, `name`, `category`, `colors`, `style_tags`, and `notes`)
- **Returns:**
A string containing outfit recommendations and styling advice.
- **When it has nothing:**
A string containing general standalone styling and pairing advice when the wardrobe list is empty (`[]`).

### `create_fit_card`

- **What it does:**
Generates a short, engaging social media caption highlighting key item attributes, pairing notes, and style vibes.
- **Inputs:**
`outfit` (str), `new_item` (dict containing `title`, `price`, `brand`, and `platform`)
- **Returns:**
A string containing a ready-to-post caption with item highlights and relevant style hashtags.
- **When it has nothing:**
An empty string `""`.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If `search_listings` returns an empty list, put a message in the session explaining what to adjust and stop before calling `suggest_outfit`. Otherwise, take the first matched listing into `session["selected_item"]` and proceed to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
regex and keyword extraction

**What moves through the session:** <!-- which fields, in what order -->
`query` -> `search_results` -> `selected_item` -> `wardrobe` -> `outfit_suggestion` -> `fit_card`

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask "looking for a vintage graphic tee under $30"

Found:    Mesh Long-Sleeve Top — Black — $15.0 on depop

Outfit:   Here are two cohesive outfits using the new mesh long-sleeve top and pieces from your current wardrobe:

Outfit 1: 90s Grunge Streetwear
- Top: Mesh Long-Sleeve Top (layered over the White ribbed tank top for a textured, high-contrast look)
- Bottoms: Baggy straight-leg jeans, dark wash
- Shoes: Black combat boots
- Outerwear: Vintage black denim jacket
- Accessories: Black crossbody bag

Why it works: Layering the sheer black mesh top over the white ribbed tank creates a striking contrast that leans heavily into the 90s grunge and Y2K aesthetic. Pairing it with baggy dark-wash jeans and black combat boots keeps the silhouette balanced (fitted on top, relaxed on the bottom) while tying the dark color palette together. Throwing on the vintage black denim jacket and crossbody bag finishes off an effortless, edgy streetwear look.

Outfit 2: Contrast & Texture Play
- Top: Mesh Long-Sleeve Top (worn under the Oversized grey crewneck sweatshirt with the collar and cuffs peeking out)
- Bottoms: Wide-leg khaki trousers
- Shoes: Chunky white sneakers
- Accessories: Brown leather belt

Why it works: This outfit plays with style juxtaposition by blending the grunge/goth mesh top with the minimalist, earth-toned pieces in your closet. By peeking the mesh sleeves and neckline out from under the oversized grey crewneck, you add instant texture and dimension to a basic sweatshirt. Tucking it into the wide-leg khaki trousers (cinched with the brown leather belt) grounds the look with warm neutrals, and the chunky white sneakers add a modern, casual finish.

Fit card: Obsessed is an understatement! Snagged this black mesh long-sleeve top on Depop for just $15, and I’m already living in it. Whether I'm layering it over a white tank for that 90s grunge feel or peeking the cuffs out of a cozy crewneck, it adds the coolest texture to everything. #thrifted #streetwear

2 model calls this session, 814 prompt + 466 output tokens

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; ..."
from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two cohesive outfits you can create by adding the vintage Levi's 501 jeans to your current wardrobe:

```

```
$ python -c "from tools import create_fit_card; ..."
from utils.data_loader import load_listings; print(create_fit_card('vintage Levis with white tank and chunky sneakers', load_listings()[0]))"
Still not over scoring these vintage Levi's 501 jeans on Depop for just $38! The wash is literal perfection and they fit like a absolute dream. Throwing them on with a simple white tank and chunky sneakers for the ultimate effortless look. #thrifted #streetwear

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
I asked why `create_fit_card` generated word-for-word identical outputs across multiple test runs on the same item, and how to verify output variability.
- *What came back:*
The explanation identified that `config.py` had caching enabled (`CACHE_ENABLED`), meaning subsequent calls with identical prompts bypassed the model and reused stored responses.
- *What I changed:*
Instead of altering source configurations prematurely, I passed `AI201_CACHE="0"` via the environment variable during terminal runs to disable caching and verified that the model produced natural phrasing and formatting variations.

**Moment 2**

- *What I asked for:*
I asked for the implementation of the planning loop in `agent.py` to coordinate query parsing, tool execution, and session-based state propagation.
- *What came back:*
An implementation structuring the query regex parser and ensuring all intermediate states (`parsed`, `search_results`, `selected_item`, `outfit_suggestion`, `fit_card`) were routed strictly through the `session` dictionary rather than direct variable chaining.
- *What I changed:*
For the empty search branch, I refined `session["error"]` so that instead of a generic "No results" string, it specifically directed the user on what filters to relax (raising the price ceiling or removing size/keyword constraints) and ensured `fit_card` remained `None`.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
