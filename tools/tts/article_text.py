"""Hugo front matter and readable prose for local article narration."""

from dataclasses import dataclass
from datetime import date, datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import textwrap
import tomllib

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.footnote import footnote_plugin
import yaml

MARKDOWN = MarkdownIt("commonmark").enable("table").use(footnote_plugin).use(dollarmath_plugin)
SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.DOTALL)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCK_TAGS = {"p", "div", "li", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "br"}
SKIP_TAGS = {"pre", "table", "script", "style", "figure", "audio", "video", "iframe", "svg", "math"}


class ProseHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.parts = []

    @property
    def skipped(self):
        return bool(self.stack and self.stack[-1][1])

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "") or ""
        skip = self.skipped or tag in SKIP_TAGS or bool(
            {"math", "footnotes", "footnote-ref"} & set(classes.split()))
        if tag in BLOCK_TAGS and not skip:
            self.parts.append("\n\n")
        if tag not in VOID_TAGS:
            self.stack.append((tag, skip))

    def handle_endtag(self, tag):
        if tag in BLOCK_TAGS and not self.skipped:
            self.parts.append("\n\n")
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.skipped:
            self.parts.append(data)


def front_matter(source):
    source = source.lstrip("\ufeff")
    lines = source.splitlines(keepends=True)
    if lines and lines[0].strip() in {"---", "+++"}:
        delimiter = lines[0].strip()
        for index in range(1, len(lines)):
            if lines[index].strip() in ({"---", "..."} if delimiter == "---" else {"+++"}):
                header = "".join(lines[1:index])
                metadata = yaml.safe_load(header) if delimiter == "---" else tomllib.loads(header)
                if metadata is not None and not isinstance(metadata, dict):
                    raise ValueError("front matter must be a mapping")
                return metadata or {}, "".join(lines[index + 1:])
        raise ValueError("unterminated front matter")
    if source.startswith("{"):
        metadata, end = json.JSONDecoder().raw_decode(source)
        if not isinstance(metadata, dict):
            raise ValueError("front matter must be a mapping")
        return metadata, source[end:].lstrip("\r\n")
    return {}, source


def narration_text(title, body):
    # Remove shortcode delimiters while retaining paired shortcodes' prose.
    body = SHORTCODE.sub("", body)
    body = re.sub(r"\\\[.*?\\\]", "", body, flags=re.DOTALL)
    body = re.sub(r"\\\(.*?\\\)", "", body, flags=re.DOTALL)
    parser = ProseHTML()
    parser.feed(MARKDOWN.render(body))
    parser.close()
    paragraphs = [str(title).strip()] if title else []
    for paragraph in "".join(parser.parts).split("\n\n"):
        paragraph = re.sub(r"https?://\S+", "", paragraph)
        paragraph = " ".join(paragraph.split())
        if paragraph:
            paragraphs.append(paragraph)
    return "\n\n".join(
        paragraph if paragraph[-1] in ".!?:;。！？…" else paragraph + "."
        for paragraph in paragraphs
    )


def split_chunks(text, max_chars=300):
    if max_chars < 40:
        raise ValueError("chunk size must be at least 40 characters")
    chunks = []
    current = ""
    for paragraph in text.split("\n\n"):
        for sentence in re.split(r"(?<=[.!?。！？])\s+", paragraph.strip()):
            for piece in textwrap.wrap(sentence, width=max_chars, break_on_hyphens=False):
                if current and len(current) + len(piece) + 1 > max_chars:
                    chunks.append(current)
                    current = ""
                current = f"{current} {piece}".strip()
        # Paragraph boundaries also give the speaker a short pause.
        if current:
            chunks.append(current)
            current = ""
    return chunks


def as_datetime(value):
    if isinstance(value, datetime):
        result = value
    elif isinstance(value, date):
        result = datetime.combine(value, datetime.min.time())
    elif value:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    else:
        return None
    return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result


@dataclass(frozen=True)
class Article:
    path: Path
    key: str
    source_hash: str
    text: str
    audio_path: Path


def enabled(metadata, *, drafts=False, future=False, expired=False):
    if metadata.get("audio") is not True:
        return False
    if metadata.get("draft") and not drafts:
        return False
    now = datetime.now(timezone.utc)
    publish = as_datetime(metadata.get("publishDate", metadata.get("publishdate", metadata.get("date"))))
    expires = as_datetime(metadata.get("expiryDate", metadata.get("expirydate")))
    return not ((publish and publish > now and not future) or (expires and expires <= now and not expired))
