"""Build plotly.js documentation using jinja template."""

import argparse
import frontmatter
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError
import json
import markdown
from pathlib import Path
import sys

import plugins


KEYS_TO_IGNORE = {
    "_isSubplotObj",
    "editType",
    "role",
}
SUBPLOT = "_isSubplotObj"


def main():
    """Main driver."""
    opt = parse_args()
    schema = json.loads(Path(opt.schema).read_text())
    env = Environment(loader=FileSystemLoader(opt.theme))
    env.filters["backtick"] = plugins.backtick
    env.filters["debug"] = plugins.debug
    all_pages = opt.page if opt.page else [p.name for p in Path(opt.stubs).glob("*.md")]
    err_count = 0
    for page in all_pages:
        if opt.crash:
            render_page(opt, schema, env, page)
        else:
            try:
                render_page(opt, schema, env, page)
            except Exception as exc:
                print(f"ERROR in {page}: {exc}", file=sys.stderr)
                err_count += 1
    print(f"ERRORS: {err_count} / {len(all_pages)}")


def get_details(schema, page):
    """Temporary hack to pull details out of schema and page header."""
    # Trace
    if "full_name" not in page:
        return page

    key = page["name"].split(".")[-1]
    entry = schema["layout"]["layoutAttributes"][key]

    # Subplot
    if SUBPLOT in entry:
        return entry

    # Figure
    return list(entry["items"].values())[0]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--crash", action="store_true", help="crash on first error")
    parser.add_argument("--out", help="name of output directory")
    parser.add_argument("--schema", required=True, help="path to schema JSON")
    parser.add_argument("--stubs", required=True, help="path to stubs directory")
    parser.add_argument("--theme", required=True, help="path to theme directory")
    parser.add_argument("page", nargs="...", help="name(s) of source file in stubs directory")
    return parser.parse_args()


def render_page(opt, schema, env, page_name):
    """Render a single page."""
    stem = Path(page_name).stem
    loaded = frontmatter.load(Path(opt.stubs, page_name))
    metadata = loaded.metadata
    assert "template" in metadata, f"page {page_name} does not specify 'template'"
    content = loaded.content
    details = get_details(schema, metadata)
    template = env.get_template(metadata["template"])
    html = template.render(
        page={"title": stem, "meta": metadata},
        config={"data": {"plot-schema": schema}},
        details=details,
        keys_to_ignore=KEYS_TO_IGNORE,
        content=content,
    )
    if opt.out:
        Path(opt.out, stem).mkdir(parents=True, exist_ok=True)
        Path(opt.out, stem, "index.html").write_text(html)
    else:
        print(html)


if __name__ == "__main__":
    main()
