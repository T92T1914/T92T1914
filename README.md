CS student (AI/ML concentration) with six years in Air Force logistics behind it —
household goods movement at a JPPSO, freight rates, storage, search-and-rescue
support. Forecasting demand cycles was the job before it was the coursework.

I build things that check their own work. The through-line across the projects
below is that a number is not trusted until something independent reproduces it.

### Projects

**[freight-forecast](https://github.com/T92T1914/freight-forecast)** — monthly
shipment volume forecasting served as a containerized API: scikit-learn, FastAPI,
Docker, Kubernetes, Prometheus, Grafana.
Beats its seasonal-naive baseline by 31% (226 vs 327 MAE on 24 held-out months),
and the training script exits non-zero if it ever stops beating it, so a
regression fails CI instead of shipping quietly.

**[mcts-combat-engine](https://github.com/T92T1914/mcts-combat-engine)** —
open-loop Monte Carlo Tree Search for stochastic, imperfect-information
turn-based combat. Pure Python, zero dependencies, with an original example game
so every claim in the README is runnable.
Extracted and generalized from a larger private project where the same search
core evaluated 400,000+ simulations per decision inside a one-second budget.

**[exact-blackjack-solver](https://github.com/T92T1914/exact-blackjack-solver)** —
exact, composition-dependent blackjack solver: the true expected value of hit,
stand, double and split by enumerating every continuation against the actual
remaining shoe. No tables, no training, no simulation in the answer.
The enumeration is cross-checked by an independent Monte Carlo harness, and the
test suite pins the direction every rule change moves the EV, not magic constants.

### How I work

Two habits that show up in everything here:

- **Independent reproduction over code review.** On one project every material bug
  was caught by two implementations disagreeing, and none by reading the code —
  including a bug that appeared identically in an exact solver and its Monte Carlo
  cross-check, which only surfaced because the two answers differed. That solver is
  the one above.
- **Negative results stay in the repo.** Reverted changes are documented where they
  were made, with the measurement that killed them, so nobody spends a day
  rediscovering why an idea does not work.

### Currently

- Extending the forecasting service — model monitoring beyond request metrics
- A real-time input-scheduling problem with a sub-millisecond latency budget
- Coursework toward the CS degree (AI/ML)
