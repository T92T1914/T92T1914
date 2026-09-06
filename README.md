<img src="assets/signals.svg" alt="" width="1200">

# Trinidy Farris

**I build software around things I care about.**

Six years in Air Force logistics. Now studying computer science with an AI/ML
concentration. My projects connect that operational background with the systems,
mathematics, and visual work that keep me curious.

I spend weeks at a time on these projects: building a version, finding what
breaks, understanding why, and coming back with a better question. I learn by
doing, and I like showing the work along the way.

[Forecasting](#freight-forecast) · [Stochastic search](#mcts-combat-engine) ·
[Probability](#exact-blackjack-solver) · [Adaptive timing](#adaptive-timing-engine) ·
[Current focus](#systems-engineering)

## Systems engineering

My long-term project explores **human-like input performance**: how timing,
workload, recovery, and technique interact as a system's state changes. It brings
together behavioral modeling, input scheduling, concurrent planning, and measured
feedback. It is where I spend most of my project time, working through the small
details that shape the behavior of the whole system.

The application-specific implementation and original calibration data stay
private. **adaptive-timing-engine** is a focused public companion: a generalized
concurrency design plus a new timing simulation, generated workloads, and its
own tests. It represents one part of the engineering, with the scope made
explicit. The four projects below are public and runnable.

## Four projects to explore

### freight-forecast

**From a logistics problem to a service you can inspect.**

Seasonal demand is familiar territory from my time in logistics. I built a
forecasting service around a simple test: can the model improve on using the
same month last year, and can I show how the surrounding service behaves?

The project covers chronological evaluation, a FastAPI service, Docker,
Kubernetes, and Prometheus/Grafana monitoring. On **seeded synthetic data**, the
model's mean absolute error is **226 moves versus 327** for the seasonal-naive
baseline across 24 held-out months. That is a reproducible experiment, not a
claim about operational shipment data.

[Run a forecast](https://github.com/T92T1914/freight-forecast#quickstart) ·
[See the deployment evidence](https://github.com/T92T1914/freight-forecast/blob/main/VERIFICATION.md) ·
[Inspect a measured serving improvement](https://github.com/T92T1914/freight-forecast/blob/main/docs/serving-performance.md)

### mcts-combat-engine

**Making decisions when the same move can lead somewhere different.**

A turn-based combat simulator gave me a place to explore stochastic search:
sample possible futures, compare decisions, and see where a shallow search
gets things wrong. The engine uses open-loop Monte Carlo Tree Search and
optional parallel worker processes, in pure Python with no runtime dependencies.

One detail worth reading: removing a card shifts list indexes, but a search
tree's action must still mean the same card. The implementation preserves that
identity across simulations and tests changing move availability. Seeded
benchmarks include the cases that improved and the one that got worse.

[Read one decision](https://github.com/T92T1914/mcts-combat-engine#reading-one-decision) ·
[Explore the design decisions](https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/design-decisions.md) ·
[Compare the results](https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/benchmark-results.md)

### exact-blackjack-solver

**Following a decision all the way down to the remaining cards.**

Two hands can have the same total and still call for different decisions.
This project calculates action values from the cards left in the shoe,
using dynamic programming and memoization, then checks the calculations with
an independent simulation harness.

Hit, stand, and double are exactly enumerated within the supported model.
**Split valuation is approximate**, with independent split hands and a shared
resplit-budget approximation. The CLI shows the values and the margin between
actions, so a close decision stays visibly close.

[Walk through a hand](https://github.com/T92T1914/exact-blackjack-solver#a-worked-decision) ·
[Explore the solver](https://github.com/T92T1914/exact-blackjack-solver#how-it-works) ·
[Read the model limits](https://github.com/T92T1914/exact-blackjack-solver#what-this-does-not-prove)

### adaptive-timing-engine

**Making humanized timing experiments inspectable.**

Humanized timing is more than adding random delay: variation interacts with
workload, recovery, and execution constraints. This standalone simulation makes
those interactions visible. A latest-request worker also addresses a systems
failure: an older calculation finishing after its input has become obsolete.

The offline trace explorer compares **48 paired cases**, switching one policy
mechanism at a time. Generated workloads expose constraints, rejected work,
and deadline expiration. Under saturation at seed 42, the full policy admits
**96 of 240** tasks; disabling variation admits **108**. That tradeoff stays
visible. The parameters are synthetic, not a validated model of human behavior.

[Run the trace explorer](https://github.com/T92T1914/adaptive-timing-engine#run-it) ·
[Inspect the concurrency decisions](https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/design-decisions.md) ·
[See the paired results](https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/evidence/results.md)

## What connects the work

I like problems where an answer has to survive contact with the details:
changing state, uncertain outcomes, timing, or a baseline that is harder to
beat than expected. I keep examples, tests, measurements, and design notes
close to the code so the interesting decisions are open to inspection.

I am building toward software and MLOps work in logistics, defense, and
operational technology. I am also going to keep making things because I want
to see how far an idea can go.
