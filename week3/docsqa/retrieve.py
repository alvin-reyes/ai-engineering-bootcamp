"""Step 2: find the chunks most likely to answer a question."""
import math
import re
from collections import Counter
from dataclasses import dataclass

from .ingest import Chunk

STOP = set("a an the is are to of for in on at and or how what when do i my must be by with within does it "
           "you your we our can".split())


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


def tokenize(text: str) -> list[str]:
    """Lowercase, keep runs of letters, digits and hyphens, drop words in STOP.

    tokenize("The Return-Policy: 30 days!") == ["return-policy", "30", "days"]
    """
    # TODO
    raise NotImplementedError


def cosine(a, b) -> float:
    """Cosine similarity of two equal-length vectors; 0.0 if either has zero length. (Given.)"""
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def sentence_transformers_embed_fn(model_name: str = "all-MiniLM-L6-v2"):
    """Optional local embeddings (pip install sentence-transformers). Returns embed_fn(texts) -> list of vectors.

    Pass it to Retriever(chunks, embed_fn=...). Nothing leaves your machine. VERIFY it runs on yours.
    """
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return lambda texts: model.encode(list(texts), normalize_embeddings=True).tolist()


class Retriever:
    """Search over chunks. TF-IDF in pure Python by default; vectors if you pass `embed_fn`.

    embed_fn(list_of_texts) -> list of vectors. It is called once with all chunk texts when the Retriever is built,
    and once with [query] for each search.
    """

    def __init__(self, chunks: list[Chunk], embed_fn=None):
        self.chunks = list(chunks)
        self.embed_fn = embed_fn
        # TODO: with embed_fn: embed all chunk texts once.
        #       without: count the words in each chunk (tokenize) and compute idf = log(N / df) + 1 per word.
        raise NotImplementedError

    def search(self, query: str, k: int = 5) -> list[Hit]:
        """Top k chunks by score, best first. Only chunks with score > 0 (no overlap = no hit).
        Ties keep the original chunk order, so results are deterministic.

        TF-IDF score for a chunk: sum over the query words of (count in chunk * idf), divided by
        sqrt(1 + number of words in the chunk) so long chunks do not win just by being long.
        """
        # TODO
        raise NotImplementedError
