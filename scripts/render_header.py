"""Render the profile's illustrative Clair and Obscur header with Python 3.

Run from any directory. Use --check to verify the committed renditions.
The original assets/signals.svg remains unchanged. These motifs are not data.
There is no visible text, font dependency, animation, or external resource.
"""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN_REVISION = "7a57fe750ff50205a17e1d342106a0d3f2777159"
TOKEN_SOURCE = (
    "https://github.com/T92T1914/clair-obscur-themes/blob/"
    f"{TOKEN_REVISION}/tokens.json"
)
# Only the reviewed family roles needed by this fixed illustration are copied.
PALETTES = {
    "clair": {
        "canvas": "#f8f7f3", "panel": "#fdfcf8", "divider": "#b8b6ae",
        "muted": "#595854", "accent": "#365f78", "control": "#ecebe6",
    },
    "obscur": {
        "canvas": "#090909", "panel": "#151515", "divider": "#494949",
        "muted": "#bcbcbc", "accent": "#b3c8d8", "control": "#252525",
    },
}
DESCRIPTION = (
    "Illustrative motifs for forecasting, search, probability, concurrent work "
    "and historical archives. These shapes do not represent measured results."
)


def render(appearance):
    c = PALETTES[appearance]
    panels = "\n".join(
        f'  <rect x="{24 + i * 232}" y="28" width="224" height="184" rx="12" '
        f'fill="{c["panel"]}" stroke="{c["divider"]}"/>'
        for i in range(5)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="240" viewBox="0 0 1200 240" fill="none">
  <title>Systems, models and archives</title>
  <desc>{DESCRIPTION}</desc>
  <metadata>Appearance: {appearance}. Palette: {TOKEN_SOURCE}. Renderer: scripts/render_header.py.</metadata>
  <rect width="1200" height="240" rx="16" fill="{c['canvas']}"/>
{panels}
  <g stroke="{c['divider']}" stroke-width="2">
    <!-- Axes belong to the signal and distribution, not every motif. -->
    <path d="M48 169H224M512 169H688"/>
  </g>
  <g stroke="{c['accent']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
    <!-- A signal with a visibly provisional continuation. -->
    <path d="M49 145C64 153 75 110 89 119S106 157 121 136S139 72 153 87S175 139 191 107"/>
    <path d="M191 107C202 88 210 77 223 84" stroke-dasharray="3 9"/>
    <circle cx="153" cy="87" r="6" fill="{c['accent']}" stroke="{c['panel']}" stroke-width="2"/>
    <!-- Distinct search branches, with one path emphasized. -->
    <path d="M285 119L337 81L391 66M337 81L391 103L445 83M285 119L337 147L391 130M337 147L391 158M391 103L445 133" stroke="{c['divider']}"/>
    <path d="M285 119L337 81L391 103L445 83"/>
    <g fill="{c['panel']}">
      <circle cx="285" cy="119" r="6"/><circle cx="337" cy="81" r="6"/>
      <circle cx="391" cy="103" r="6"/><circle cx="445" cy="83" r="6"/>
    </g>
    <!-- A distribution without a fabricated scale or numeric claim. -->
    <g fill="{c['accent']}" fill-opacity="0.18" stroke-width="3">
      <rect x="518" y="145" width="17" height="20" rx="3"/>
      <rect x="543" y="121" width="17" height="44" rx="3"/>
      <rect x="568" y="85" width="17" height="80" rx="3"/>
      <rect x="593" y="65" width="17" height="100" rx="3"/>
      <rect x="618" y="94" width="17" height="71" rx="3"/>
      <rect x="643" y="131" width="17" height="34" rx="3"/>
      <rect x="668" y="151" width="17" height="14" rx="3"/>
    </g>
    <!-- Staggered work intervals share a time marker. -->
    <path d="M748 85H916M748 121H916M748 157H916" stroke="{c['divider']}" stroke-width="2"/>
    <path d="M832 66V174" stroke="{c['muted']}" stroke-width="3"/>
    <g fill="{c['control']}">
      <rect x="748" y="78" width="58" height="14" rx="7"/>
      <rect x="790" y="114" width="66" height="14" rx="7"/>
      <rect x="866" y="150" width="50" height="14" rx="7"/>
    </g>
    <!-- Source cards connect to an archive record. -->
    <path d="M1015 89H1045V121H1078M1015 153H1045V121" stroke="{c['muted']}"/>
    <g fill="{c['control']}">
      <rect x="980" y="66" width="35" height="44" rx="4"/>
      <rect x="980" y="132" width="35" height="44" rx="4"/>
      <rect x="1078" y="87" width="67" height="70" rx="5"/>
    </g>
    <path d="M1092 105H1129M1092 121H1129M1092 137H1115" stroke-width="3"/>
  </g>
</svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for appearance in PALETTES:
        target = ROOT / "assets" / f"header-{appearance}.svg"
        content = render(appearance)
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Out of date: {target.relative_to(ROOT)}")
        else:
            target.write_text(content, encoding="utf-8", newline="\n")
    print("Header renditions match the renderer." if args.check else "Rendered Clair and Obscur headers.")


if __name__ == "__main__":
    main()
