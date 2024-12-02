"""Prettify HTML."""

from bs4 import BeautifulSoup
import sys

sys.stdout.write(BeautifulSoup(sys.stdin.read(), "html.parser").prettify())
