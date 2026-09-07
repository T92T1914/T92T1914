<img src="assets/signals.svg" alt="" width="1200">

# Trinidy Farris

**I build things because I want to understand how they work and how far I can take them.**

I am an Air Force veteran studying computer science with an AI/ML concentration.
I expect to finish classes in January or February 2027 and graduate in April 2027.
My projects connect my logistics background with the systems, mathematics, and
creative work that keep me curious.

These are passion projects. I spend weeks at a time on them, sometimes months,
and I take pride in that. I like getting something working, finding the detail
I missed, and figuring out why it matters. I learn by building, and I want
people to be able to see the work behind the result.

I am looking for early career software engineering opportunities, with a growing
interest in MLOps and operational systems. My [LinkedIn profile](https://www.linkedin.com/in/t92t1914/)
has my experience and education.

[Forecasting](#freight-forecast) · [Stochastic search](#mcts-combat-engine) ·
[Probability](#exact-blackjack-solver) · [Adaptive timing](#adaptive-timing-engine) ·
[Current focus](#systems-engineering)

## Start with a question

You can inspect these examples in your browser before setting anything up.
The project sections below also link to the code and local reproduction steps.

| If you want to see how I approach... | Start here |
| --- | --- |
| Forecast evaluation and serving | [Freight Forecast: one forecast and its baseline](https://github.com/T92T1914/freight-forecast#quickstart) |
| Concurrency and timing tradeoffs | [Adaptive Timing Engine: paired experiment results](https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/evidence/results.md) |
| Decisions under uncertainty | [MCTS Combat Engine: one search decision](https://github.com/T92T1914/mcts-combat-engine#reading-one-decision) |
| Numerical models and their limits | [Exact Blackjack Solver: a worked decision](https://github.com/T92T1914/exact-blackjack-solver#a-worked-decision) |

## Systems engineering

The project I spend the most time on explores **humanized input performance**.
Timing is only one part of it. Workload, recovery, technique, and changing state
all affect how the system behaves. I have spent months working through those
interactions, using behavioral modeling, input scheduling, concurrent planning,
and measured feedback.

The application and original calibration data stay private. **Adaptive Timing
Engine** is a public companion that lets me share one part of the engineering:
a generalized concurrency design, a new timing simulation, generated workloads,
and their own tests. The four projects below are public and runnable.

## Four projects to explore

### Freight Forecast

**A problem I knew from logistics, built into a service you can inspect.**

Seasonal demand is familiar territory from my time in logistics. For this
project, I wanted to see whether a model could improve on using the same month
last year, then build the service around it and show how it behaves.

The project covers chronological evaluation, a FastAPI service, Docker,
Kubernetes, and Prometheus/Grafana monitoring. On **seeded synthetic data**, the
model's mean absolute error is **226 moves versus 327** for the seasonal baseline
across 24 months held out from training. Those numbers describe this
reproducible experiment. They are not a claim about operational shipment data.

[![A model forecast and seasonal baseline compared with 24 months of synthetic shipment volumes](https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-example.png)](https://github.com/T92T1914/freight-forecast/blob/main/docs/visual-example.md)

The [recorded Grafana dashboard](https://github.com/T92T1914/freight-forecast/blob/main/docs/grafana-dashboard.png)
shows the other side of this project: request rates, latency, rejected inputs,
and forecast distributions under local container traffic.

[Run a forecast](https://github.com/T92T1914/freight-forecast#quickstart) ·
[See the deployment evidence](https://github.com/T92T1914/freight-forecast/blob/main/VERIFICATION.md) ·
[Inspect a measured serving improvement](https://github.com/T92T1914/freight-forecast/blob/main/docs/serving-performance.md)

### MCTS Combat Engine

**What makes a good decision when the outcome can change?**

A turn based combat simulator gave me a place to explore that question. The
engine samples possible futures, compares decisions, and makes it possible to
see where a shallow search gets things wrong. It uses open loop Monte Carlo
Tree Search and optional parallel worker processes, in pure Python with no
runtime dependencies.

One detail I had to get right was what an action means as the state changes.
Removing a card shifts list indexes, but the action stored in the search tree
must still mean the same card. The implementation preserves that identity and
tests changing move availability. The benchmarks include the cases that
improved and the one that got worse.

[![A seeded search ranks Spark, Pass and Weakness Mark by mean shaped reward, with visits shown separately.](https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-example.png)](https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/visual-example.md)

[Read one decision](https://github.com/T92T1914/mcts-combat-engine#reading-one-decision) ·
[Explore the design decisions](https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/design-decisions.md) ·
[Compare the results](https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/benchmark-results.md)

### Exact Blackjack Solver

**The same total does not always mean the same decision.**

I wanted to follow that difference down to the cards left in the shoe. This
solver calculates action values using dynamic programming and memoization,
then checks the calculations with an independent simulation harness.

Hit, stand, and double are exactly enumerated within the supported model.
**Split valuation is approximate**, with independent split hands and an
approximation for the shared resplit budget. The CLI shows the values and the
margin between actions. If the difference is small, you can see that for yourself.

[![Two hard 16 hands against a dealer ten have different exact hit and stand values.](https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/main/docs/blackjack-composition-example.png)](https://github.com/T92T1914/exact-blackjack-solver/blob/main/docs/visual-example.md)

[Walk through a hand](https://github.com/T92T1914/exact-blackjack-solver#a-worked-decision) ·
[Explore the solver](https://github.com/T92T1914/exact-blackjack-solver#how-it-works) ·
[Read the model limits](https://github.com/T92T1914/exact-blackjack-solver#what-this-does-not-prove)

### Adaptive Timing Engine

**A way to see what humanized timing policies actually do.**

Timing variation interacts with workload, recovery, and the limits on what can
be executed. I built this standalone simulation to make those interactions
visible. The planning worker also handles a problem that matters whenever work
happens in the background: an old calculation finishing after a newer request
has made it obsolete.

The offline trace explorer compares **48 paired cases**, changing one policy
mechanism at a time. You can inspect the constraints, rejected work, and expired
deadlines. Under saturation at seed 42, the full policy admits **96 of 240**
tasks; disabling variation admits **108**. I kept that tradeoff visible. The
parameters are synthetic and do not establish a validated model of human behavior.

[![A controlled worker experiment reduces 101 requests to two calculations and rejects one obsolete result.](https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-example.png)](https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/visual-example.md)

[Run the trace explorer](https://github.com/T92T1914/adaptive-timing-engine#run-it) ·
[Inspect the concurrency decisions](https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/design-decisions.md) ·
[See the paired results](https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/evidence/results.md)

## What connects the work

I like problems that keep giving me a reason to look closer. Sometimes it is
a timing detail. Sometimes it is a result I thought would improve and did not.
I keep examples, tests, measurements, and design notes close to the code
because I want to understand the decisions and be able to explain them.

I am working toward software engineering and MLOps roles in logistics, defense,
and operational technology. These projects also matter to me outside a job
search. I enjoy making them, and I want this page to show the range of what
I care about.
