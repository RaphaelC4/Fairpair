# test_flow.py - call sequence for GenLayer Studio (type params WITHOUT quote
# marks). Use pages you have opened yourself; make one clearly stronger.

def run(contract):
    contract.create_contest(contest_id="demo", title="Best plan",
        rubric="Prefer clear, concrete, verifiable plans with named steps.").transact()
    contract.add_candidate(contest_id="demo", candidate_id="alpha", url="https://en.wikipedia.org/wiki/Solar_power").transact()
    contract.add_candidate(contest_id="demo", candidate_id="beta", url="https://en.wikipedia.org/wiki/Candle").transact()

    # Expect a clear winner, or "tie" if the judge is unstable.
    print(contract.file_match(contest_id="demo", candidate_x="alpha", candidate_y="beta").transact())
    print(contract.get_match(contest_id="demo", candidate_x="alpha", candidate_y="beta").call())
    # history shows pick_a_first / pick_b_first: a win needs both to agree.

    # Must be rejected: same pair again if decided; add_candidate after the
    # first match; candidate_id "tie"; duplicate URL; playing itself.
    print(contract.get_standings(contest_id="demo").call())

if __name__ == "__main__":
    print(__doc__)
