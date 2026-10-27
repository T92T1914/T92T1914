<picture>
  <img src="assets/header-obscur.svg" alt="Illustrative motifs for forecasting, search, probability, concurrent work and historical archives. These shapes do not represent measured results." width="1200">
</picture>

# Trinidy Farris

I build things because I want to understand how they work and how far I can take them.

I am an Air Force veteran studying computer science with an AI/ML concentration.
I expect to finish classes in December 2026 and graduate in February 2027.
My projects connect my logistics background with the systems, mathematics and
creative work that keep me curious.

These are passion projects. I spend weeks at a time on them, sometimes months.
I like getting something working, finding the detail I missed and figuring out
why it matters. I am looking for early career software and systems engineering
opportunities, especially work involving C++, Python, research tools and software assurance.

## Start with the work

| If you want to explore... | Start here |
| --- | --- |
| Native interfaces, ownership and performance | [Heterogeneous Batch Runtime](https://github.com/T92T1914/heterogeneous-batch-runtime) |
| PyTorch integration and native training operations | [Ragged Pooling for PyTorch](https://github.com/T92T1914/ragged-pool) |
| Search, evaluation and controlled execution | [MCTS Combat Engine](https://github.com/T92T1914/mcts-combat-engine) |
| Numerical models and expensive state spaces | [Exact Blackjack Solver](https://github.com/T92T1914/exact-blackjack-solver) |
| Historical data and interactive visualization | [Tornado Atlas](https://github.com/T92T1914/tornado-atlas) |
| Application state, access and retry behavior | [Shipment Exception Workspace](https://github.com/T92T1914/shipment-exception-workspace) |

### Heterogeneous Batch Runtime

My main systems project is a C++20 runtime with scalar, optimized CPU and optional
CUDA paths. Installed consumers can discover compiled backends without confusing
them with a working device. A separate image classifier connects ONNX Runtime
through C++. Each request owns its input and output, and an obsolete result
cannot replace the current one while its underlying work finishes. Optional
[model batching](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/5d51afd321fc56e1e316ec3ce202d03cd6279146/docs/model-batching.md)
processes a nonempty batch of up to eight images in one invocation while serial
remains the default.

The retained inference comparisons check complete output tensors, session reuse
and memory. Reusing the C++ session reduced repeated call cost, but the direct
Python CPU baseline was faster at every tested batch size in both collections.
The CUDA followup records GPU operator placement. These results do not measure
recognition accuracy or establish general GPU superiority. A later
[batching study](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/5d51afd321fc56e1e316ec3ce202d03cd6279146/docs/batching-results.md)
reduced complete request cost for two and eight images within each provider,
with CPU still faster in every tested batch. GPU sanitizer and
hardware counter acceptance remain open. HIP and SYCL are not implemented.

[Explore the project](https://t92t1914.github.io/heterogeneous-batch-runtime/) ·
[Read the CPU comparison](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e9346dac005e8dc4558b029cd813e260dce0236a/docs/inference-results.md) ·
[Read the CUDA followup](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e9346dac005e8dc4558b029cd813e260dce0236a/docs/inference-cuda-results.md) ·
[Inspect the backend contract](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e9346dac005e8dc4558b029cd813e260dce0236a/docs/backend-discovery.md)

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/runtime-obscur-narrow.png">
  <img src="assets/explainers/runtime-obscur-wide.png" alt="Conceptual masked sum: values and a mask enter an owned request, and the uncancelled computation returns 7.0. Cancellation intent alone does not establish physical completion." width="900">
</picture>

For values `[2, -3, 5]` and mask `[1, 0, 1]`, the ordinary uncancelled sum is
`7.0`. Running storage stays owned until physical return. This conceptual
illustration adds no timing or CPU/GPU result.
[Explore the project](https://t92t1914.github.io/heterogeneous-batch-runtime/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/runtime-obscur-wide.png)

### Ragged Pooling for PyTorch

Groups of data do not always have the same length. This small PyTorch component
combines each group into one vector using softmax weights. C++ handles the CPU
forward and backward operations, and Python connects them to training. The package
includes readable references, installed training examples and trusted model
exports for packed and padded inputs. The eager packed and padded CPU routes
also support second order gradients, including small training examples with
penalties on input gradients. Compiled training remains first order.

An optional CUDA companion supports eager packed training in float32 and float64.
The tested Windows RTX 4090 route passed installed gradient and model update
checks and six native diagnostic runs on the eager consumer. A separate fixed
shape `torch.compile` route uses `aot_eager` to capture forward and backward
graphs and check matched training updates. Those graphs run with eager PyTorch,
without optimized code generation or a speed claim. The compiled consumer has no
new sanitizer result.

Separate bounded CUDA routes now cover padded inputs, dynamic training, trusted
inference export and selected second derivatives. Later native derivative
binaries have no new sanitizer qualification. CUDA graph capture and broader
device portability remain outside the qualified scope.

The Linux CPU examples use two responsive ranks for unequal batches, accumulated
updates, continuation, clipping and shared numerical admission. These fixed
synthetic consumers do not establish GPU distributed training or general crash
recovery.

The studies use synthetic data and declared CPU environments. They do not establish
a general performance advantage or real world model accuracy. Third derivatives
remain outside the accepted routes.

[Inspect the component](https://github.com/T92T1914/ragged-pool) and
[read the supported contract](https://github.com/T92T1914/ragged-pool/blob/f2031fe8297df24c407413ac76856fc5feabe53b/docs/contract.md),
[packed second order boundary](https://github.com/T92T1914/ragged-pool/blob/f2031fe8297df24c407413ac76856fc5feabe53b/docs/second-order.md),
[padded second order boundary](https://github.com/T92T1914/ragged-pool/blob/f2031fe8297df24c407413ac76856fc5feabe53b/docs/padded-second-order.md)
and [trained padded export](https://github.com/T92T1914/ragged-pool/blob/f2031fe8297df24c407413ac76856fc5feabe53b/docs/padded-export.md).
The [CUDA contract](https://github.com/T92T1914/ragged-pool/blob/1cfc678d33bb34c036d8f0336ecfd986a6e97ea2/cuda/README.md),
[eager validation record](https://github.com/T92T1914/ragged-pool/blob/98a2748e8eca8fd03442c86e8504d9a03bd5c3bc/cuda/evidence/windows-sm89-20261021.json)
and [compiled validation record](https://github.com/T92T1914/ragged-pool/blob/fcbdb698cab1fc0549e9b27c7ec69b8e2cce69a4/cuda/evidence/compiled-windows-sm89-20261021.json)
describe these separate GPU checks.

The [Linux CPU training examples](https://github.com/T92T1914/ragged-pool/blob/1cfc678d33bb34c036d8f0336ecfd986a6e97ea2/docs/distributed-cpu.md) and [shared update admission](https://github.com/T92T1914/ragged-pool/blob/1cfc678d33bb34c036d8f0336ecfd986a6e97ea2/docs/distributed-admission.md) keep their separate contracts and controls.

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/ragged-obscur-narrow.png">
  <img src="assets/explainers/ragged-obscur-wide.png" alt="Conceptual pooling route: unequal groups receive softmax weights and produce one vector per group. Empty groups return zero vectors. This is a first-order training illustration, separate from broader qualified routes." width="900">
</picture>

In this conceptual example, weights `[0.25, 0.75]` combine `[2, 0]` and `[0, 4]`
into `[0.5, 3]`. Empty groups return zeros. The illustration explains the first-order
training mechanism, while the supported derivative boundaries remain above.
[Explore the project](https://t92t1914.github.io/ragged-pool/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/ragged-obscur-wide.png) ·
[Detailed Obscur diagram](https://raw.githubusercontent.com/T92T1914/ragged-pool/91470d74a0559a5f6f0168deb27f27f87152d66a/docs/ragged-pool-obscur.png) ·
[Clair alternate](https://raw.githubusercontent.com/T92T1914/ragged-pool/91470d74a0559a5f6f0168deb27f27f87152d66a/docs/ragged-pool-clair.png)

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
A separate [installed Linux consumer](https://github.com/T92T1914/mcts-combat-engine/blob/d075b7ea94d32de178d8e6e766ab7c66bf8b101e/docs/linux-managed-episode.md)
records and replays through an existing local Docker daemon, with resource
accounting limited to its owned container and descendants.

[Explore the decisions](https://t92t1914.github.io/mcts-combat-engine/) ·
[Read the encounter finding](https://github.com/T92T1914/mcts-combat-engine/blob/2a8d2ac354415d765542d61b195dd01baf9c475c/docs/encounter-outcomes.md) ·
[Use the managed consumer](https://github.com/T92T1914/mcts-combat-engine/blob/2a8d2ac354415d765542d61b195dd01baf9c475c/docs/managed-encounters.md)

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/mcts-obscur-narrow.png">
  <img src="assets/explainers/mcts-obscur-wide.png" alt="Conceptual search route using a retained decision: a saved modeled state receives 10,000 simulations and selects Spark at mean shaped reward 0.532. The reward is not a win probability." width="900">
</picture>

The retained decision ranks Spark at mean shaped reward `0.532` after `10,000`
simulations. This compact explanation reuses that one modeled decision. It adds no
search run and does not describe an encounter win rate.
[Explore the project](https://t92t1914.github.io/mcts-combat-engine/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/mcts-obscur-wide.png)

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

<details>
<summary>Open the detailed saved decision figure and its appearance alternatives</summary>

<a href="https://github.com/T92T1914/mcts-combat-engine/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/mcts-combat-engine/main/docs/mcts-decision-clair.png" alt="One recorded decision after 10,000 simulations. Spark has mean shaped reward 0.532, Pass 0.506 and Weakness Mark 0.495. Exact visits are 5,724, 2,445 and 1,831 respectively. Reward is not a win probability." width="900">
  </picture>
</a>

</details>

### Exact Blackjack Solver

The same hand total does not always mean the same decision when different cards
remain. This solver follows that distinction through explicit finite shoe models
and hidden dealer information. The original split path is approximate. Separate
bounded common shoe models preserve shared depletion and combined settlement,
with their own information and wager conventions.

One H17 ace request, where the dealer hits soft 17, returns all four original
action values at 82,780 states under the unchanged 100,000 state cap. This is one
specific completion result, not a general speedup or a full shoe guarantee.
[Completed settlement reuse](https://github.com/T92T1914/exact-blackjack-solver/blob/689a6ee94b8be3948ab384c869f3476a0e396773/docs/bounded-resplit-calculation.md#reuse-completed-settlement-states)
also lets two declared sixteen card non ace requests finish after earlier refusal,
without establishing lower latency or universal completion.
Installed calculation and replay commands preserve reusable records. The browser
inspector reads saved results without calculation or upload. Same engine replay
and independent mathematical checks remain different kinds of evidence.

[Explore the models](https://t92t1914.github.io/exact-blackjack-solver/#model-route) ·
[Calculate and replay the H17 request](https://github.com/T92T1914/exact-blackjack-solver#a-complete-h17-ace-calculation) ·
[Read the completion evidence](https://github.com/T92T1914/exact-blackjack-solver/blob/259aa8aedf84510887d8dbf3e5bf928c1447458a/docs/ace-terminal-reuse.md)

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/solver-obscur-narrow.png">
  <img src="assets/explainers/solver-obscur-wide.png" alt="Conceptual composition route: hard 16 against a dealer ten is evaluated with the cards remaining. The retained examples hit ten and six, but stand on eight, five and three. Exact hit and stand are separate from the original approximate split path." width="900">
</picture>

The retained six-deck examples hit `10 + 6` and stand on `8 + 5 + 3` against a
dealer ten. Both expected returns remain negative. These exact hit/stand examples
are separate from the original approximate split route.
[Explore the project](https://t92t1914.github.io/exact-blackjack-solver/#model-route) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/solver-obscur-wide.png)

<details>
<summary>Open the retained completion and composition figures</summary>

<a href="https://github.com/T92T1914/exact-blackjack-solver/blob/c5fa104375fca65404cfdf2ddda015d9eb6a54a2/docs/ace-terminal-reuse.md">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/ace-terminal-reuse-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/ace-terminal-reuse-clair.png">
    <img src="assets/ace-terminal-reuse-clair.png" alt="One qualified cold H17 ace request completed all four original action values in 82,780 entered states under the unchanged 100,000 state cap. Original binary64 values were preserved. This is completion of one request, with no general latency or larger shoe guarantee." width="900">
  </picture>
</a>

<a href="https://github.com/T92T1914/exact-blackjack-solver/blob/4f2128eb9692bade742e6684ddc27919b2c63633/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/4f2128eb9692bade742e6684ddc27919b2c63633/docs/blackjack-composition-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/4f2128eb9692bade742e6684ddc27919b2c63633/docs/blackjack-composition-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/4f2128eb9692bade742e6684ddc27919b2c63633/docs/blackjack-composition-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/4f2128eb9692bade742e6684ddc27919b2c63633/docs/blackjack-composition-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/exact-blackjack-solver/4f2128eb9692bade742e6684ddc27919b2c63633/docs/blackjack-composition-clair.png" alt="Two recorded hard 16 hands against a dealer ten. Ten and six prefers hit, while eight, five and three prefers stand. Both expected returns are negative. The exact hit and stand examples are separate from the original approximate split path." width="900">
  </picture>
</a>

</details>

### Tornado Atlas

I have always been interested in tornadoes. I wanted a way to study where they
went, what was documented and what we can actually say about how they looked.
Atlas combines a searchable NOAA record collection with six historical exhibits:
El Reno, Joplin, Blackwell, Tuscaloosa and Birmingham, Newcastle and Moore, and
Udall. Maps, photographs and evidence dossiers connect observations to their sources.

Reported times, camera observations and illustrative models remain separate.
The local research desk exports reviewed publication candidates without private
notes. The museum is usable now. Registered changing appearance and calibrated
historical damage remain unfinished research goals.

[Visit the museum](https://t92t1914.github.io/tornado-atlas/) ·
[Explore the record collection](https://t92t1914.github.io/tornado-atlas/atlas.html) ·
[Inspect the evidence dossiers](https://t92t1914.github.io/tornado-atlas/dossier.html)

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/atlas-obscur-narrow.png">
  <img src="assets/explainers/atlas-obscur-wide.png" alt="Conceptual evidence route: a credited observation carries time and viewpoint limits into evidence and replay. Unknowns stay explicit, and observation stays separate from illustration." width="900">
</picture>

A source's clock and viewpoint inform what can be said about a historical event.
A clock claim alone does not register changing appearance. Unknowns remain
explicit, and an illustrative model is labeled separately.
[Explore the project](https://t92t1914.github.io/tornado-atlas/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/atlas-obscur-wide.png)

## Supporting projects

### Shipment Exception Workspace

[Shipment Exception Workspace](https://github.com/T92T1914/shipment-exception-workspace)
is a local shipment review demo built with React and TypeScript, FastAPI and
PostgreSQL. Operators in the seeded organizations can create exceptions, search
and filter the queue, then assign or resolve a selected record. Reviewers can
inspect records and their history without changing them. Each change and its
history are recorded in the same transaction. Stale edits are refused, and a
retry that is still authorized can recover a committed result after a response
is lost.

Participating tabs recheck the shared session, clear old account state after
observed changes and discard delayed results from the previous context.
Recovery does not automatically repeat uncertain writes.

The [v0.9.0 release](https://github.com/T92T1914/shipment-exception-workspace/releases/tag/v0.9.0)
provides the installable application with its built frontend. The
[operator walkthrough](https://github.com/T92T1914/shipment-exception-workspace/blob/618aa4f18394064004318ea3619ae2412d609c8c/docs/operator-walkthrough.md)
shows creation, a competing edit, stale-version refusal and recovery after a
deliberately interrupted committed response. The
[installation guide](https://github.com/T92T1914/shipment-exception-workspace/blob/618aa4f18394064004318ea3619ae2412d609c8c/docs/install.md)
describes the supported local PostgreSQL route.

A separate public reviewer mode refuses business writes and receipt replay on
the server. Local HTTPS staging passed. A public hosted URL and provider restart
acceptance remain unfinished, so the installed walkthrough is the available demo.

A [local restore guide](https://github.com/T92T1914/shipment-exception-workspace/blob/b2ff568e49ef037a7a585f0ee39be79a11d81f6f/docs/backup-and-restore.md) records a trusted synthetic
workspace restored through direct loopback into a separate empty database on
the same cluster. Data and database structure matched before application
startup, without initializing, migrating or seeding the target. That Windows x64
result uses PostgreSQL 18.1, CPython 3.13.3 and the v0.8.0 wheel and tools. It does
not establish production backups or disaster recovery.

The [accepted workflow and limits](https://github.com/T92T1914/shipment-exception-workspace/blob/618aa4f18394064004318ea3619ae2412d609c8c/README.md)
use synthetic records. There is no carrier integration or production deployment.

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/shipment-obscur-narrow.png">
  <img src="assets/explainers/shipment-obscur-wide.png" alt="Conceptual retry route from the installed synthetic walkthrough. Casey assignment expects version 2 and commits version 3 with history and a receipt. Its response is lost, a still-authorized same-intent retry adds no event, and later resolution reaches version 4." width="900">
</picture>

Casey assignment commits version 3, its history event and saved response together.
When that reply is lost, a still-authorized retry with the original key and body
recovers the saved response without another event. Later resolution reaches
version 4. This conceptual explanation follows the installed walkthrough.
[Explore the static project page](https://t92t1914.github.io/shipment-exception-workspace/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/shipment-obscur-wide.png)

### Freight Forecast

My logistics background is the starting point for
[Freight Forecast](https://github.com/T92T1914/freight-forecast). It connects
chronological evaluation to a FastAPI service, containers and monitoring.
Synthetic shipments and the separate Bureau of Transportation Statistics freight
activity index stay distinct.
On that index, carrying forward the last observation beat the learned model.
The forecast ledger separates issuance, source revisions and corrections. Its
public example contains no real issued forecast.

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/freight-obscur-narrow.png">
  <img src="assets/explainers/freight-obscur-wide.png" alt="Conceptual forecasting route: earlier months supply features, later months test the predictions and the model returns a monthly forecast. On the separate BTS index, carrying forward the last observation beat the learned model." width="900">
</picture>

Earlier observations supply the features and later months test the predictions.
This conceptual route keeps the synthetic series separate from the BTS index,
where the simpler last-observation baseline won.
[Explore the project](https://t92t1914.github.io/freight-forecast/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/freight-obscur-wide.png)

<details>
<summary>Open the retained synthetic forecast figure and appearance alternatives</summary>

<a href="https://github.com/T92T1914/freight-forecast/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/freight-forecast/main/docs/freight-forecast-clair.png" alt="Recorded synthetic shipments over 24 test months. Model mean absolute error is 226 moves per month versus 327 for the seasonal baseline. Each prediction uses prior observations." width="900">
  </picture>
</a>

</details>

### Adaptive Timing Engine

[Adaptive Timing Engine](https://github.com/T92T1914/adaptive-timing-engine)
examines scheduling when work becomes obsolete. An
[installed consumer](https://github.com/T92T1914/adaptive-timing-engine/blob/9cadd27c8c72f07c371c54525671c0254a160f20/docs/revision-file.md)
runs finite local revisions through CPU analysis, keeping physical completion
separate from adoption of the current answer. Saved receipts can be checked
without executing the work. The trace explorer retains its generated workloads.
These studies do not establish real time guarantees or a validated model of
human behavior.

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/adaptive-obscur-narrow.png">
  <img src="assets/explainers/adaptive-obscur-wide.png" alt="Conceptual scheduling route: a newer revision arrives, older physical work may finish and only the current answer is adopted. Physical completion and current-answer adoption remain separate." width="900">
</picture>

A newer request can replace waiting work without claiming that an older running
calculation has stopped. The retained worker example computes payloads `0` and
`100`, rejects the obsolete result and retains payload `100` at revision `101`.
[Explore the project](https://t92t1914.github.io/adaptive-timing-engine/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/adaptive-obscur-wide.png)

<details>
<summary>Open the retained worker figure and appearance alternatives</summary>

<a href="https://github.com/T92T1914/adaptive-timing-engine/blob/main/docs/visual-example.md">
  <picture>
    <source media="(min-width: 1024px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-obscur-wide.png">
    <source media="(min-width: 1024px) and (prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-clair-wide.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-obscur.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-clair.png">
    <img src="https://raw.githubusercontent.com/T92T1914/adaptive-timing-engine/main/docs/adaptive-timing-clair.png" alt="Recorded worker example: 101 requests, two calculations, 99 replacements and one stale completion. The final result is payload 100 at revision 101." width="900">
  </picture>
</a>

</details>

### Clair and Obscur

[Clair and Obscur](https://t92t1914.github.io/clair-obscur-themes/) is a shared
visual theme family with downloadable packages and previews, installation guidance
and recovery instructions. Package and browser preview checks remain separate from complete
native compatibility, restart persistence, signing and store approval. The shared
palette also supplies a [Garmin watch face candidate](https://github.com/T92T1914/clair-obscur-themes/blob/4574e0350dbb6fc626e4e07b606c177188166861/docs/garmin-watchface.md)
and [phone icons](https://github.com/T92T1914/clair-obscur-themes/blob/4574e0350dbb6fc626e4e07b606c177188166861/docs/samsung-icons.md).
An earlier watch version has simulator acceptance. The current watch source has
its own unexecuted simulator and device checks. A scoped earlier phone theme was
applied, while full icon assignment, launcher behavior and restoration remain
separate checks.

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/themes-obscur-narrow.png">
  <img src="assets/explainers/themes-obscur-wide.png" alt="Conceptual theme route: named surface, text and focus roles map into platform packages and previews. Preview checks and native installation acceptance remain separate." width="900">
</picture>

Named surface, text and focus roles map to each platform's package. A working
preview does not establish native installation, restart persistence or complete
host compatibility.
[Explore the project](https://t92t1914.github.io/clair-obscur-themes/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/themes-obscur-wide.png)

### Calendar Tracker AI

[Calendar Tracker AI](https://github.com/T92T1914/calendar-tracker-ai) is a small
Python text-menu application for a CSCI498 version control lab. It adds, lists,
edits, deletes and searches local events, saves JSON and exports a new CSV.
It is a single-writer coursework application without online calendar integration,
time-zone handling or an AI service.

<picture>
  <source media="(max-width: 680px)" srcset="assets/explainers/calendar-obscur-narrow.png">
  <img src="assets/explainers/calendar-obscur-wide.png" alt="Conceptual local calendar route: a title and local date/time are validated and saved to schema-1 JSON, then inspected or exported to a new CSV. This is a local single-writer program, not an online calendar or AI service." width="900">
</picture>

A validated event goes into schema-1 JSON, and export writes a separate new CSV.
The browser page explains this local program rather than running a calendar service.
[Explore the project](https://t92t1914.github.io/calendar-tracker-ai/) ·
[Source and limits](PROFILE_EXPLAINERS.md) ·
[Full-size infographic](assets/explainers/calendar-obscur-wide.png)

## How I approach the work

I keep examples, tests, measurements and design notes close to the code because
I want to understand the decisions and be able to explain them. Sometimes the
useful result is an improvement. Sometimes the simpler approach wins or the
evidence does not settle the question.

These projects matter to me outside a job search. They are not claims of
deployment in a live logistics or emergency operation.

[My LinkedIn profile](https://www.linkedin.com/in/t92t1914/) has my experience and education.

[Read in another language](TRANSLATION.md): browser translation help, with code and evidence kept exact.
