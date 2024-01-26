import re
from pathlib import Path

import mistletoe
from mistletoe.block_token import BlockToken
from mistletoe.markdown_renderer import MarkdownRenderer
from mistletoe.span_token import SpanToken

wordsAndDefinitions = []
with open(Path.cwd() / "Notes" / "2024-01-08 Course Intro.md", "r") as file:
    text = file.readlines()

    for line in text:
        match = re.search(r"([A-z ]+): (.+)", line, re.RegexFlag.M)
        if match:
            word, definition = match.group(1).lstrip(), match.group(2)
            wordsAndDefinitions.append((word, definition))
