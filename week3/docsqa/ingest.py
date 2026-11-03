"""Step 1: load documents and cut them into chunks."""
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    name: str  # file name, for example "returns.md"
    text: str


@dataclass(frozen=True)
class Chunk:
    id: str      # unique, used as the citation, for example "returns.md#refunds"
    source: str  # the document file name
    heading: str
    text: str    # starts with the heading line, then the body


def slugify(heading: str) -> str:
    """'Beta Two!' -> 'beta-two'. (Given: use it to build chunk ids.)"""
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def load_documents(folder) -> list[Document]:
    """Read every .md and .txt file directly inside `folder`, sorted by file name. Ignore other file types."""
    # TODO: list the files, filter by suffix, sort, read each one as UTF-8, return Documents.
    raise NotImplementedError


def chunk_document(doc: Document, max_chars: int = 800) -> list[Chunk]:
    """Cut one document into chunks.

    Rules (the tests check these):
    - One chunk per '## Heading' section. Text before the first '## ' (the '# Title') is not a chunk.
    - chunk.text = the heading, a newline, then the section body.
    - chunk.id = f"{doc.name}#{slugify(heading)}".
    - A section longer than max_chars is split on blank lines (paragraphs), packed greedily up to max_chars.
      Every part keeps the heading at the top of its text. Parts after the first get the id suffix -2, -3, ...
      so ids stay unique. Never drop text.
    """
    # TODO: split into sections, then split long sections, then build Chunk objects.
    raise NotImplementedError


def ingest(folder, max_chars: int = 800) -> list[Chunk]:
    """Load every document in `folder` and return all their chunks, in order."""
    # TODO: combine load_documents and chunk_document.
    raise NotImplementedError
