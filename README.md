# FairPair: Head-to-Head Judging That Cannot Be Won by Position

**Category:** Intelligent Contracts (standalone primitive)
**Files:** `fairpair.py` (contract), `test_flow.py` (call-sequence walkthrough)

## The problem

Small grants, local competitions, hackathons and "pick the better entry"
decisions end with someone choosing between two public submissions. Human
judges can be biased. A single AI judge has a quieter flaw: **position
bias**. Language models often lean toward whichever option is shown first
(or second), so the same two submissions can win or lose depending only on
the order they were pasted in.

## The primitive

A contest has a public rubric and up to 8 candidates, each one a public page.
Anyone can request a match between two candidates. Every validator fetches
both pages itself and judges the pair **twice, once in each order**, with
neutral labels (Option 1 / Option 2). A candidate wins only if it wins in
**both** orders. Anything else is a tie. Results roll up into a round-robin
standings table (`get_standings`).

## Consensus design: order-swap agreement

Validators agree on the position-proofed verdict (`a`, `b` or `tie`):

1. **Leader integrity.** The leader's verdict must follow from its own two
   picks. A leader cannot report a win its own judging did not support.
2. **Independent re-run.** Each validator re-fetches both pages
   (`gl.nondet.web.render`) and runs the full two-order judging itself.
3. **Exact agreement** on the verdict.

Near-equal entries often fail to resolve because judging flips between runs.
That is intended: an unstable comparison produces no ruling, not false
precision.

## Replay rules

- One match per pair. A decided match is final.
- A tied pair can be rematched **once**. A second tie is final.
- Entries close when the first match is filed.
- Max 8 candidates (28 matches).
- An unreachable page never decides a match: nothing is written, so knocking
  a rival's page offline cannot win it.

## State

| Map | Key | Value |
|---|---|---|
| `contests` | `contest_id` | creator, title, rubric, matches_filed, candidates |
| `matches` | `contest_id\|lo\|hi` | winner, rounds, history with both order picks |

`total_contests` and `total_matches` are `u256` counters. No page content is
stored.

## Known limitations

- Swapping neutralises position and label bias, **not** a page that praises
  itself by name. Pages are marked untrusted, but a determined author can
  still try to steer the reading.
- Only the first ~10,000 characters of each page's text are read.
- The rubric is not validated for fairness; the contract judges against the
  rubric, not reality.
- Entrants can edit their pages between matches.
- Image-heavy pages give the model little text.

## Extending

- Best-of-three with different prompt phrasings.
- Entry bond refunded on completing a match.
- Tie-break rule for level standings.
