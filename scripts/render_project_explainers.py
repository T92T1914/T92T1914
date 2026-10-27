"""Render the ten compact Obscur profile explanations from public source records.

Supply genuine static Inter 4.1 faces with --font-dir or PROFILE_FIGURE_FONT_DIR.
--check validates committed inputs and outputs without plotting dependencies.
No project is imported, searched, trained or benchmarked by this renderer.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODEL = "assets/profile-explainers-input.json"
TOKENS = "assets/profile-figure-tokens.json"
RECORD = "assets/profile-explainers.json"
SOURCE = "scripts/render_project_explainers.py"
INPUTS = (MODEL, TOKENS, SOURCE, "scripts/profile_mechanisms.py", "requirements-figures.txt")
PROJECTS = ("runtime", "ragged", "mcts", "solver", "atlas", "shipment",
            "freight", "adaptive", "themes", "calendar")
FONT_HASHES = {
    "Regular": "40d692fce188e4471e2b3cba937be967878f631ad3ebbbdcd587687c7ebe0c82",
    "SemiBold": "78a843fade9d4612a5567302fb595b56976eb5fcebf4fea5a5912d638bafcde3",
    "Bold": "288316099b1e0a47a4716d159098005eef7c0066921f34e3200393dbdb01947f",
}
WEIGHTS = {"Regular": 400, "SemiBold": 600, "Bold": 700}


def digest(path, *, text=False):
    data = path.read_text(encoding="utf-8").encode() if text else path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def read_model():
    model = json.loads((ROOT / MODEL).read_text(encoding="utf-8"))
    if tuple(project["id"] for project in model["projects"]) != PROJECTS:
        raise ValueError("The ten public projects must retain their declared order")
    for project in model["projects"]:
        if not project["composition"] or not project["source_paths"]:
            raise ValueError("Each project needs its own composition and public sources")
        if not project["essential_text"] or not project["footer"]:
            raise ValueError("Keep the mechanism and its limit in ordinary text")
        repository = project["repository"]
        reader_route = project["page"].split("#", 1)[0]
        if reader_route not in (
            f"https://t92t1914.github.io/{repository}/",
            f"https://github.com/T92T1914/{repository}",
        ):
            raise ValueError("Use this project's public webpage or source route")
    return model


def output_names(model):
    return tuple(f"assets/explainers/{project['id']}-obscur-{layout}.{extension}"
                 for project in model["projects"] for layout in ("wide", "narrow")
                 for extension in ("png", "svg"))


def check():
    model = read_model()
    record = json.loads((ROOT / RECORD).read_text(encoding="utf-8"))
    if record["new_project_execution"] is not False or record["model"] != model:
        raise ValueError("The profile rendition is not a new project execution")
    for name in INPUTS:
        if record["inputs_sha256_lf"][name] != digest(ROOT / name, text=True):
            raise ValueError("Profile figure input changed: " + name)
    if set(record["outputs_sha256"]) != set(output_names(model)):
        raise ValueError("All ten wide/narrow PNG/SVG renditions are required")
    for project in model["projects"]:
        if project["renderer"] == "reuse":
            for layout in ("wide", "narrow"):
                for extension in ("png", "svg"):
                    name = f"assets/explainers/{project['id']}-obscur-{layout}.{extension}"
                    expected = project["reused_artifacts"][layout + "." + extension]["sha256"]
                    if digest(ROOT / name) != expected:
                        raise ValueError("Pinned reused figure changed: " + name)
    for name, expected in record["outputs_sha256"].items():
        if digest(ROOT / name) != expected:
            raise ValueError("Profile figure output changed: " + name)
    for face, expected in FONT_HASHES.items():
        if record["typography"][face]["sha256"] != expected:
            raise ValueError("Profile font identity changed: " + face)
    print("Ten project-specific explanations match their sources and forty exports")


def resolve_fonts(directory):
    from fontTools.ttLib import TTFont
    from matplotlib.font_manager import FontProperties

    faces, record = {}, {}
    for label, expected in FONT_HASHES.items():
        path = directory / f"Inter-{label}.ttf"
        if digest(path) != expected:
            raise ValueError("Supply the pinned official Inter 4.1 face: " + path.name)
        with TTFont(path) as font:
            names = {name.toUnicode() for name in font["name"].names if name.nameID == 6}
            if (f"Inter-{label}" not in names or font["OS/2"].usWeightClass != WEIGHTS[label]
                    or font["OS/2"].fsSelection & 1):
                raise ValueError("Expected a genuine upright Inter face: " + path.name)
            if not set(range(32, 127)).issubset(font.getBestCmap()):
                raise ValueError("Missing Latin diagram glyphs: " + path.name)
        faces[label] = lambda size, p=path: FontProperties(fname=str(p), size=size * .72)
        record[label] = {"postscript": f"Inter-{label}", "weight": WEIGHTS[label],
                         "italic": False, "sha256": expected}
    return faces, record


def draw(project, roles, fonts, *, narrow):
    from profile_mechanisms import draw_project
    return draw_project(ROOT, project, roles, fonts, narrow=narrow)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", type=Path, default=os.environ.get("PROFILE_FIGURE_FONT_DIR"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
        return
    if args.font_dir is None:
        parser.error("Supply --font-dir or PROFILE_FIGURE_FONT_DIR; fonts are not bundled")
    import matplotlib
    import fontTools
    matplotlib.use("Agg")
    matplotlib.rcParams.update({"svg.fonttype": "path", "svg.hashsalt": "profile-specific-mechanisms-v2"})
    fonts, typography = resolve_fonts(Path(args.font_dir))
    model = read_model()
    adapter = json.loads((ROOT / TOKENS).read_text(encoding="utf-8"))
    layouts = {}
    for project in model["projects"]:
        layouts[project["id"]] = {"wide": draw(project, adapter["roles"], fonts, narrow=False),
                                   "narrow": draw(project, adapter["roles"], fonts, narrow=True)}
    record = {"schema_version": 2, "new_project_execution": False, "model": model,
              "adapter": adapter, "layouts": layouts, "typography": typography,
              "font_binaries_distributed": False, "svg_labels": "New compositions: outlined Inter glyphs. Reused figures retain their exact source typography.",
              "renderer_versions": {"python": sys.version.split()[0],
                                    "matplotlib": matplotlib.__version__, "fonttools": fontTools.__version__},
              "inputs_sha256_lf": {name: digest(ROOT / name, text=True) for name in INPUTS},
              "outputs_sha256": {name: digest(ROOT / name) for name in output_names(model)}}
    (ROOT / RECORD).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Rendered six project-specific diagrams and verified four exact retained figure families")


if __name__ == "__main__":
    main()
