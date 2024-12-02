"""Jinja plugins."""

import re
import sys


BACKTICK_RE = re.compile(r'`(.+?)`')
def backtick(text):
    """Regex replacement reordered."""
    return BACKTICK_RE.sub(r"<code>\1</code>", text)


def debug(msg):
    """Print debugging message during template expansion."""
    print(msg, file=sys.stderr)


# If being loaded by MkDocs, register the filters.
if "define_env" in globals():
    def define_env(env):
        env.filters["backtick"] = backtick
        env.filters["debug"] = debug
