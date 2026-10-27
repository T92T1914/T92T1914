# Compact project explanations

The ten visible profile figures explain input, mechanism and result. They are
conceptual renditions of the linked public project sources, not new experiments,
application captures or a claim that every project has the same architecture.
Each project section supplies its essential meaning as ordinary text.

[The input model](assets/profile-explainers-input.json) records the exact public
source revision and paths for each explanation. The
[rendering record](assets/profile-explainers.json) records the model, pinned
palette adapter, actual font identities, measured layout and output hashes.

| Project | Read the mechanism or retained evidence |
| --- | --- |
| Runtime | [Owned requests and physical return](https://github.com/T92T1914/heterogeneous-batch-runtime/blob/e84f4acdca294309f3e36c586a3872e85558f8de/docs/contracts.md) |
| Ragged | [Pooling and gradient contract](https://github.com/T92T1914/ragged-pool/blob/ddf8002cfd351723ff7a9e6c7471a966b8fe33db/docs/contract.md) |
| MCTS | [One saved decision and shaped reward](https://github.com/T92T1914/mcts-combat-engine/blob/bb9a56fcdd9ce95d55bf9fbed8bfc11f17bcd8e3/docs/visual-example.md) |
| Solver | [Exact composition examples and original split limit](https://github.com/T92T1914/exact-blackjack-solver/blob/4f2128eb9692bade742e6684ddc27919b2c63633/docs/visual-example.md) |
| Atlas | [Source dossiers and their limits](https://github.com/T92T1914/tornado-atlas/blob/24baed6b9160932c654c4f99af1c39081494acf9/docs/archive-dossiers.md) |
| Shipment | [The installed versioned operator walkthrough](https://github.com/T92T1914/shipment-exception-workspace/blob/67d10a531371b1f37b8dfbb7d4ed4fa5bdd3093c/docs/operator-walkthrough.md) |
| Freight | [Synthetic forecast and separate BTS finding](https://github.com/T92T1914/freight-forecast/blob/146ecc8efafe172deb41fb067b51329c1c4e8b8d/README.md) |
| Adaptive | [Owned work and retained worker example](https://github.com/T92T1914/adaptive-timing-engine/blob/0e63441b6ce772244c507054bf9d10539ba4475a/docs/visual-example.md) |
| Themes | [Preview and native acceptance](https://github.com/T92T1914/clair-obscur-themes/blob/bfe50ba72860da600cd3923a9a454c79c158ba37/docs/acceptance.md) |
| Calendar | [Local event storage and export](https://github.com/T92T1914/calendar-tracker-ai/blob/8a42a32aa73dcdc9582773c960da5b43297dd3ea/README.md) |

## Rebuild the profile figures

Use an isolated Python environment and the optional authoring dependencies in
`requirements-figures.txt`. Supply genuine static Inter Regular, SemiBold and Bold
4.1 TTF faces from the official release in a local directory:

```console
python -m pip install -r requirements-figures.txt
python scripts/render_project_explainers.py --font-dir /path/to/Inter/extras/ttf
python scripts/render_project_explainers.py --check
```

The renderer also accepts `PROFILE_FIGURE_FONT_DIR`. It verifies the exact font
hashes, names, weights, upright flags and Latin coverage. Font files and local
paths are not distributed. PNG labels use those actual glyphs, and SVG labels
are outlined from the same files. The committed input and output check does not
import plotting libraries, load fonts or execute any of the projects.

The fixed wide edition is 1800 by 600 pixels and the narrow edition is 960 by
1000 pixels. Cards use measured wrapping and text bounds. The narrow main labels
are configured at 40 pixels rather than shrinking a desktop poster. Obscur stays
opaque under either GitHub appearance. GitHub controls the surrounding page.
The profile's [Clair header alternate](assets/header-clair.svg) and retained
project figures remain available. The original MCTS study stays collapsed, with
its source and uncertainty limits intact. The detailed decision, composition,
worker and synthetic forecast figures are accessible in their project disclosures.

The MCTS reward is retained shaped reward, not a win probability. Solver's exact
hit/stand example is separate from its original approximate split route. Freight's
BTS baseline win remains separate from its synthetic comparison. Shipment's
conceptual lost reply follows Casey's version-3 assignment, while later resolution
reaches version 4. The Shipment static explanation does not host the application.
Atlas distinguishes source observations from illustration and unresolved historical
registration. Calendar remains a local coursework application without an online
calendar or AI service.
