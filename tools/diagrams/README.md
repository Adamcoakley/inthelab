# Diagram generator

Every lab diagram is drawn by code, from one shared library (`dg.py`).
Colours are CSS variables, so each SVG follows the site's light/dark theme
once the lab page inlines it. See `/style-guide` on the site for the rules.

## Icons

The AWS icons the diagrams use are already in `aws-icons/` (only the ones in
use, about 40 files). They come from the `aws-icons` npm package (v3.3.0),
which repackages AWS's official Architecture Icons with stable file names.

To use a new icon, grab it from that package and copy it into the same
sub-folder here:

    npm pack aws-icons@3.3.0          # downloads aws-icons-3.3.0.tgz
    tar -xzf aws-icons-3.3.0.tgz      # icons are in package/icons/
    # browse names at https://aws-icon.mkabumattar.com/icons/

Then reference it by path, e.g. `d.icon("resource/AmazonVPCNATGateway", x, y, 40)`.
You can also point `AWS_ICONS` at a full copy of `package/icons`.

## Regenerate

    python3 tools/diagrams/p0.py      # Phase 0
    python3 tools/diagrams/p1.py      # Phase 1
    python3 tools/diagrams/p234.py    # Phases 2 to 4
    python3 tools/diagrams/home.py    # home page
    python3 tools/diagrams/styleguide_assets.py   # add --css to print the theme tokens

Each script writes straight into `public/images/labs/` using the same file
names the labs already reference, so no Markdown changes are needed.

## Adding a diagram

Write a function in the right phase file using the helpers in `dg.py`
(icons, groups, arrows, status marks, cards, tables), add it to `ALL`,
run the script, and reference the SVG from the lab as usual.
