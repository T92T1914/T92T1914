<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-obscur.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/header-clair.svg">
  <img src="assets/header-clair.svg" alt="Illustrative motifs for forecasting, search, probability, concurrent work and historical archives. These shapes do not represent measured results." width="1200">
</picture>

# Trinidy Farris

I build things because I want to understand how they work and how far I can take them.

I am an Air Force veteran studying computer science with an AI/ML concentration.
I expect to finish classes in January or February 2027 and graduate in April 2027.
My projects connect my logistics background with the systems, mathematics and
creative work that keep me curious.

These are passion projects. I spend weeks at a time on them, sometimes months.
I like getting something working, finding the detail I missed and figuring out
why it matters. I am looking for early career software and systems engineering
opportunities, especially work involving C++, Python and research tools.

## Start with the work

| If you want to explore... | Start here |
| --- | --- |
| Native interfaces, ownership and performance | [Heterogeneous Batch Runtime](#heterogeneous-batch-runtime) |
| Search, evaluation and controlled execution | [MCTS Combat Engine](#mcts-combat-engine) |
| Numerical models and expensive state spaces | [Exact Blackjack Solver](#exact-blackjack-solver) |
| Historical data and interactive visualization | [Tornado Atlas](#tornado-atlas) |

### Heterogeneous Batch Runtime

My main systems project is a C++20 runtime with scalar, optimized CPU and optional
CUDA paths. Installed consumers can discover compiled backends without confusing
them with a working device. A separate image classifier connects ONNX Runtime
through C++. Each request owns its input and output, and an obsolete result
cannot replace the current one while its underlying work finishes.

The retained inference comparisons check complete output tensors, session reuse
and memory. Reusing the C++ session reduced repeated call cost, but the direct
Python CPU baseline was faster at every tested batch size in both collections.
The CUDA followup records GPU operator placement. These results do not measure
recognition accuracy or establish general GPU superiority. GPU sanitizer and
hardware counter acceptance remain open. HIP and SYCL are not implemented.

[Explore the project](https://t92t1914.github.io/heterogeneous-batch-runtime/) ·
[Read the CPU comparison](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e9346dac005e8dc4558b029cd813e260dce0236a/docs/inference-results.md) ·
[Read the CUDA followup](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e9346dac005e8dc4558b029cd813e260dce0236a/docs/inference-cuda-results.md) ·
[Inspect the backend contract](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e9346dac005e8dc4558b029cd813e260dce0236a/docs/backend-discovery.md)

### MCTS Combat Engine

Monte Carlo tree search samples possible futures to choose an action in a compact
turn based model. The Python engine stays separate from the companion that
records decisions and encounters, replays matching records without search and
inspects saved evidence.

An optional root allocation treatment reduced mean first action reference loss
by about 53.2 percent on sixteen controlled modeled states at a one round horizon.
Two cases had fewer exact best action hits, and five state uncertainty intervals
included zero. This measures the gap between the selected action and the best
action under the declared reference objective, not full encounter playing strength
or search speed.

The later prespecified encounter comparison was inconclusive about which policy
wins more often. Equal allowances per decision produced different total work.
The standard search policy remains the default.

The companion also provides Windows managed capture and passive recovery for a
small declared workload. It owns worker lifetimes, bounds retained output and
records incomplete or contradictory evidence. Recovery reads retained files
without retrying or replacing trials. These operational controls do not establish
better play, authenticate receipt origin or provide a hostile code sandbox.

[Explore the decisions](https://t92t1914.github.io/mcts-combat-engine/) ·
[Read the encounter finding](https://github.com/T92T1914/mcts-combat-engine/blob/2a8d2ac354415d765542d61b195dd01baf9c475c/docs/encounter-outcomes.md) ·
[Use the managed consumer](https://github.com/T92T1914/mcts-combat-engine/blob/2a8d2ac354415d765542d61b195dd01baf9c475c/docs/managed-encounters.md)

<details>
<summary>See all sixteen states in the frozen root allocation study</summary>

<p>The figure retains both cases with fewer exact best action hits and all five
state intervals that include zero. It shows the accepted horizon one study,
with ordinary UCT still the default.</p>

<a href="https://github.com/T92T1914/mcts-combat-engine/blob/0d516b9f8e779708f9139d67116198a87f9ced7f/docs/root-allocation.md">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/root-allocation-study-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/root-allocation-study-clair.png">
    <img src="assets/root-allocation-study-clair.png" alt="Frozen sixteen state horizon one study at 32 simulations and transitions per search. Mean first action reference loss changed from 0.010989648244 to 0.005141135643, an observed reduction of 53.2184 percent. Two cases had fewer exact best hits and five state intervals include zero. UCT remains the default. This is not a search time or full encounter claim." width="640">
  </picture>
</a>

<p><a href="https://github.com/T92T1914/mcts-combat-engine/blob/0d516b9f8e779708f9139d67116198a87f9ced7f/docs/root-allocation/results.json">Read the full deciding results</a>
and <a href="assets/project-figures.json">figure source record</a>.
The figure reuses saved evidence. It does not add a new experiment.</p>

</details>

<a href="https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-clair.png" alt="One recorded decision after 10,000 simulations. Spark has mean shaped reward 0.532, Pass 0.506 and Weakness Mark 0.495. Exact visits are 5,724, 2,445 and 1,831 respectively. Reward is not a win probability." width="900">
  </picture>
</a>

### Exact Blackjack Solver

The same hand total does not always mean the same decision when different cards
remain. This solver follows that distinction through explicit finite shoe models
and hidden dealer information. The original split path is approximate. Separate
bounded common shoe models preserve shared depletion and combined settlement,
with their own information and wager conventions.

One H17 ace request, where the dealer hits soft 17, returns all four original
action values at 82,780 states under the unchanged 100,000 state cap. This is one
specific completion result, not a general speedup or a full shoe guarantee.
Installed calculation and replay commands preserve reusable records. The browser
inspector reads saved results without calculation or upload. Same engine replay
and independent mathematical checks remain different kinds of evidence.

[Explore the models](https://t92t1914.github.io/exact-blackjack-solver/#model-route) ·
[Calculate and replay the H17 request](https://github.com/T92T1914/exact-blackjack-solver#a-complete-h17-ace-calculation) ·
[Read the completion evidence](https://github.com/T92T1914/exact-blackjack-solver/blob/259aa8aedf84510887d8dbf3e5bf928c1447458a/docs/ace-terminal-reuse.md)

<a href="https://github.com/T92T1914/exact-blackjack-solver/blob/c5fa104375fca65404cfdf2ddda015d9eb6a54a2/docs/ace-terminal-reuse.md">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/ace-terminal-reuse-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/ace-terminal-reuse-clair.png">
    <img src="assets/ace-terminal-reuse-clair.png" alt="One qualified cold H17 ace request completed all four original action values in 82,780 entered states under the unchanged 100,000 state cap. Original binary64 values were preserved. This is completion of one request, with no general latency or larger shoe guarantee." width="900">
  </picture>
</a>

<a href="https://github.com/T92T1914/exact-blackjack-solver/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/main/docs/blackjack-composition-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/main/docs/blackjack-composition-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/main/docs/blackjack-composition-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/main/docs/blackjack-composition-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/main/docs/blackjack-composition-clair.png" alt="Two recorded hard 16 hands against a dealer ten. Ten and six prefers hit, while eight, five and three prefers stand. Both expected returns are negative. The exact hit and stand examples are separate from approximate split valuation." width="900">
  </picture>
</a>

### Tornado Atlas

I have always been interested in tornadoes. I wanted a way to study where they
went, what was documented and what we can actually say about how they looked.
Atlas combines a searchable NOAA record collection with four historical exhibits:
El Reno, Joplin, Blackwell and Tuscaloosa. Maps, photographs and evidence dossiers
connect observations to their sources.

Reported times, camera observations and illustrative models remain separate.
The local research desk exports reviewed publication candidates without private
notes. The museum is usable now. Registered changing appearance and calibrated
historical damage remain unfinished research goals.

[Visit the museum](https://t92t1914.github.io/tornado-atlas/) ·
[Explore the record collection](https://t92t1914.github.io/tornado-atlas/atlas.html) ·
[Inspect the evidence dossiers](https://t92t1914.github.io/tornado-atlas/dossier.html)

## Supporting projects

### Freight Forecast

My logistics background is the starting point for
[Freight Forecast](https://github.com/T92T1914/freight-forecast). It connects
chronological evaluation to a FastAPI service, containers and monitoring.
Synthetic shipments and the separate Bureau of Transportation Statistics freight
activity index stay distinct.
On that index, carrying forward the last observation beat the learned model.
The forecast ledger separates issuance, source revisions and corrections. It
currently contains no real issued forecast.

<a href="https://github.com/T92T1914/freight-forecast/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-clair.png" alt="Recorded synthetic shipments over 24 test months. Model mean absolute error is 226 moves per month versus 327 for the seasonal baseline. Each prediction uses prior observations." width="900">
  </picture>
</a>

### Adaptive Timing Engine

[Adaptive Timing Engine](https://github.com/T92T1914/adaptive-timing-engine)
examines scheduling when work becomes obsolete. Cancellation requests, physical
completion and adoption of a result are separate events. The trace explorer
makes generated workloads and rejected work inspectable. Those studies do not
establish real time guarantees or a validated model of human behavior.

<a href="https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-clair.png" alt="Recorded worker example: 101 requests, two calculations, 99 replacements and one stale completion. The final result is payload 100 at revision 101." width="900">
  </picture>
</a>

### Clair and Obscur

[Clair and Obscur](https://t92t1914.github.io/clair-obscur-themes/) is a shared
visual theme family with downloadable packages and previews, installation guidance
and recovery instructions. Package and browser preview checks remain separate from complete
native compatibility, restart persistence, signing and store approval.

## How I approach the work

I keep examples, tests, measurements and design notes close to the code because
I want to understand the decisions and be able to explain them. Sometimes the
useful result is an improvement. Sometimes the simpler approach wins or the
evidence does not settle the question.

These projects matter to me outside a job search. They are not claims of
deployment in a live logistics or emergency operation.

[My LinkedIn profile](https://www.linkedin.com/in/t92t1914/) has my experience and education.
