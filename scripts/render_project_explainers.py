"""Render the ten compact Obscur profile explanations from public source records.

Supply genuine static Inter 4.1 faces with --font-dir or PROFILE_FIGURE_FONT_DIR.
--check validates committed inputs and outputs without plotting dependencies.
No project is imported, searched, trained or benchmarked by this renderer.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODEL = "assets/profile-explainers-input.json"
TOKENS = "assets/profile-figure-tokens.json"
RECORD = "assets/profile-explainers.json"
SOURCE = "scripts/render_project_explainers.py"
INPUTS = (MODEL, TOKENS, SOURCE, "requirements-figures.txt")
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
        if len(project["cards"]) != 3 or not project["source_paths"]:
            raise ValueError("Each mechanism needs three cards and public sources")
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
    for name, expected in record["outputs_sha256"].items():
        if digest(ROOT / name) != expected:
            raise ValueError("Profile figure output changed: " + name)
    for face, expected in FONT_HASHES.items():
        if record["typography"][face]["sha256"] != expected:
            raise ValueError("Profile font identity changed: " + face)
    print("Ten compact explanations match their sources and forty exports")


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
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    width, height = (960, 1000) if narrow else (1800, 600)
    figure = plt.figure(figsize=(width / 100, height / 100), dpi=100,
                         facecolor=roles["canvas"])
    axes = figure.add_axes((0, 0, 1, 1), xlim=(0, width), ylim=(height, 0))
    axes.axis("off")

    def text(x, y, value, size, face="Regular", role="text"):
        return axes.text(x, y, value, fontproperties=fonts[face](size), va="top",
                         color=roles[role], linespacing=1.1)

    def box_bounds(label):
        extent = label.get_window_extent(figure.canvas.get_renderer())
        left, bottom = axes.transData.inverted().transform((extent.x0, extent.y0))
        right, top = axes.transData.inverted().transform((extent.x1, extent.y1))
        return tuple(float(value) for value in (left, top, right, bottom))

    def wrap(label, max_width):
        lines = []
        renderer = figure.canvas.get_renderer()
        for paragraph in label.get_text().split("\n"):
            line = ""
            for word in paragraph.split():
                candidate = (line + " " + word).strip()
                label.set_text(candidate)
                if label.get_window_extent(renderer).width <= max_width:
                    line = candidate
                elif line:
                    lines.append(line)
                    line = word
                    label.set_text(word)
                    if label.get_window_extent(renderer).width > max_width:
                        raise ValueError("An unbreakable profile word exceeds its panel: " + word)
                else:
                    raise ValueError("An unbreakable profile word exceeds its panel: " + word)
            lines.append(line)
        label.set_text("\n".join(lines))

    main_size = 48 if narrow else 40
    title_size = 52 if narrow else 50
    footer_size = 36 if narrow else 28
    title = text(60, 24, project["title"], title_size, "Bold")
    eyebrow = text(60, 118 if narrow else 125, "CONCEPTUAL MECHANISM", 28,
                   "SemiBold", "accent")
    panels = []
    for index, body in enumerate(project["cards"]):
        heading = text(0, 0, f"{index + 1}  " + ("INPUT", "MECHANISM", "RESULT")[index],
                       main_size, "SemiBold", "accent")
        label = text(0, 0, body, main_size)
        panels.append({"heading": heading, "body": label})
    footer = text(60, 0, project["footer"], footer_size, role="muted")
    figure.canvas.draw()
    first_panel = 190 if narrow else 200
    if narrow:
        wrap(title, width - 120)
        eyebrow.set_position((60, box_bounds(title)[3] + 16))
        first_panel = max(first_panel, math.ceil(box_bounds(eyebrow)[3] + 24))
    for panel in panels:
        wrap(panel["body"], 784 if narrow else 464)
    wrap(footer, width - 120)
    figure.canvas.draw()
    panel_height = max(200 if narrow else 230, math.ceil(max(
        box_bounds(panel["heading"])[3] - box_bounds(panel["heading"])[1] +
        box_bounds(panel["body"])[3] - box_bounds(panel["body"])[1] + 56
        for panel in panels)))
    for index, panel in enumerate(panels):
        x = 60 if narrow else 60 + index * 580
        y = first_panel + index * (panel_height + 24) if narrow else first_panel
        w = 840 if narrow else 520
        axes.add_patch(FancyBboxPatch((x, y), w, panel_height,
                                      boxstyle="round,pad=0,rounding_size=14",
                                      linewidth=2, edgecolor=roles["border"],
                                      facecolor=roles["panel"], zorder=1))
        panel["heading"].set_position((x + 28, y + 20))
        panel["heading"].set_zorder(2)
        heading_height = box_bounds(panel["heading"])[3] - box_bounds(panel["heading"])[1]
        panel["body"].set_position((x + 28, y + 20 + heading_height + 16))
        panel["body"].set_zorder(2)
        panel["inner"] = (x + 28, y + 20, x + w - 28, y + panel_height - 20)
        if index < 2:
            if narrow:
                a, b = (480, y + panel_height + 3), (480, y + panel_height + 21)
            else:
                a, b = (x + w + 8, y + panel_height / 2), (x + w + 52, y + panel_height / 2)
            axes.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=22,
                                           linewidth=2, color=roles["muted"]))
    bottom = (first_panel + 3 * panel_height + 48) if narrow else (first_panel + panel_height)
    footer.set_position((60, bottom + 32))
    figure.canvas.draw()
    if narrow:
        height = max(height, math.ceil(box_bounds(footer)[3] + 32))
        figure.set_size_inches(width / 100, height / 100, forward=False)
        axes.set_ylim(height, 0)
        figure.canvas.draw()
    geometry = []
    for panel in panels:
        measured = {}
        for kind in ("heading", "body"):
            bounds = box_bounds(panel[kind])
            inner = panel["inner"]
            if (bounds[0] < inner[0] - .01 or bounds[1] < inner[1] - .01 or
                    bounds[2] > inner[2] + .01 or bounds[3] > inner[3] + .01):
                raise ValueError(project["id"] + ": panel overflow " +
                                 panel[kind].get_text() + " actual=" + str(bounds) +
                                 " permitted=" + str(inner))
            measured[kind] = [round(value, 3) for value in bounds]
        if measured["body"][1] < measured["heading"][3] + 16 - .01:
            raise ValueError(project["id"] + ": heading/body overlap")
        geometry.append({"padded_panel": panel["inner"], "labels": measured})
    for label in axes.texts:
        bounds = box_bounds(label)
        if bounds[0] < 0 or bounds[1] < 0 or bounds[2] > width or bounds[3] > height:
            raise ValueError(project["id"] + ": canvas overflow " + label.get_text() + str(bounds))
    if box_bounds(title)[3] + 12 > box_bounds(eyebrow)[1]:
        raise ValueError(project["id"] + ": title/eyebrow overlap")
    if box_bounds(eyebrow)[3] + 12 > first_panel:
        raise ValueError(project["id"] + ": eyebrow/panel overlap")
    footer_bounds = box_bounds(footer)
    metadata = {"project": project, "kind": "conceptual profile rendition",
                "new_project_execution": False}
    path = ROOT / "assets" / "explainers" / f"{project['id']}-obscur-{'narrow' if narrow else 'wide'}"
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path.with_suffix(".png"), facecolor=roles["canvas"],
                   metadata={"Description": json.dumps(metadata, sort_keys=True)})
    svg_path = path.with_suffix(".svg")
    with svg_path.open("wb") as stream:
        figure.savefig(stream, format="svg", facecolor=roles["canvas"],
                       metadata={"Description": json.dumps(metadata, sort_keys=True), "Date": None})
    svg_path.write_bytes(svg_path.read_bytes().replace(b"\r\n", b"\n"))
    plt.close(figure)
    return {"width": width, "height": height, "panel_height": panel_height,
            "panel_geometry": geometry, "footer_bounds": footer_bounds,
            "main_label_pixels": main_size, "title_pixels": title_size,
            "footer_pixels": footer_size,
            "height_rule": ("Starts at 1000px and expands from measured footer bounds with 32px padding"
                            if narrow else "Fixed 600px canvas with verified bounds")}


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
    matplotlib.rcParams.update({"svg.fonttype": "path", "svg.hashsalt": "profile-explainers-v1"})
    fonts, typography = resolve_fonts(Path(args.font_dir))
    model = read_model()
    adapter = json.loads((ROOT / TOKENS).read_text(encoding="utf-8"))
    layouts = {}
    for project in model["projects"]:
        layouts[project["id"]] = {"wide": draw(project, adapter["roles"], fonts, narrow=False),
                                   "narrow": draw(project, adapter["roles"], fonts, narrow=True)}
    record = {"schema_version": 1, "new_project_execution": False, "model": model,
              "adapter": adapter, "layouts": layouts, "typography": typography,
              "font_binaries_distributed": False, "svg_labels": "outlined Inter glyphs",
              "renderer_versions": {"python": sys.version.split()[0],
                                    "matplotlib": matplotlib.__version__, "fonttools": fontTools.__version__},
              "inputs_sha256_lf": {name: digest(ROOT / name, text=True) for name in INPUTS},
              "outputs_sha256": {name: digest(ROOT / name) for name in output_names(model)}}
    (ROOT / RECORD).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Rendered ten compact Obscur explanations without executing their projects")


if __name__ == "__main__":
    main()
