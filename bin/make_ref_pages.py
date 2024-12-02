"""Generate API reference pages from JSON metadata extracted from JavaScript source."""

import argparse
import json
from pathlib import Path
import sys


# Suffix for generated files.
SUFFIX = "md"

# Attributes to document.
ATTRIBUTES = [
    "annotations",
    "coloraxis",
    "geo",
    "images",
    "map",
    "mapbox",
    "polar",
    "scene",
    "selections",
    "shapes",
    "sliders",
    "smith",
    "ternary",
    "updatemenus",
    "xaxis",
    "yaxis",
]

# Template for documentation of attributes.
ATTRIBUTE_TEMPLATE = """---
template: attribute.jinja
permalink: /javascript/reference/{full_attribute_path}/
name: {attribute}
full_name: {full_attribute}
description: Figure attribute reference for Plotly's JavaScript open-source graphing library.
parentlink: layout
block: layout
parentpath: layout
---
"""

# Documenting top-level layout.
GLOBAL_PAGE = """---
template: global.jinja
permalink: /javascript/reference/layout/
name: layout
description: Figure attribute reference for Plotly's JavaScript open-source graphing library.
parentlink: layout
block: layout
parentpath: layout
mustmatch: global
---
"""

# Template for documentation of trace.
TRACE_TEMPLATE = """---
template: trace.jinja
permalink: /javascript/reference/{trace}/
trace: {trace}
description: Figure attribute reference for Plotly's JavaScript open-source graphing library.
---
"""


def main():
    """Main driver."""
    try:
        opt = parse_args()
        schema = json.loads(Path(opt.schema).read_text())
        make_global(opt)
        for attribute in ATTRIBUTES:
            make_attribute(opt, attribute)
        for trace in schema["traces"]:
            make_trace(opt, trace)
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def make_attribute(opt, attribute):
    """Write reference pages for attributes."""
    full_attribute = f"layout.{attribute}"
    content = ATTRIBUTE_TEMPLATE.format(
        full_attribute=full_attribute,
        full_attribute_path=full_attribute.replace(".", "/"),
        attribute=attribute,
    )
    write_page(opt, "attribute", f"{attribute}.{SUFFIX}", content)


def make_global(opt):
    """Make top-level 'global' page."""
    write_page(opt, "global", f"global.{SUFFIX}", GLOBAL_PAGE)
    


def make_trace(opt, trace):
    """Write reference page for trace."""
    content = TRACE_TEMPLATE.format(trace=trace,)
    write_page(opt, "trace", f"{trace}.{SUFFIX}", content)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", required=True, help="where to write generated page stubs")
    parser.add_argument("--schema", required=True, help="path to plot schema file")
    parser.add_argument("--verbose", action="store_true", help="report progress")
    return parser.parse_args()


def write_page(opt, kind, page_name, content):
    """Save a page."""
    output_path = Path(f"{opt.pages}/{page_name}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    if opt.verbose:
        print(f"{kind}: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
