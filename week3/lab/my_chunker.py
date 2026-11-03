"""Lab step 4: your own chunking strategy. Standalone, so you can test it before pasting it into chunking.py."""
import re


def by_sentences(text: str, n: int = 2) -> dict[str, str]:
    """Chunks of `n` sentences each. Return {chunk_id: chunk_text}.

    Example: by_sentences("A. B. C.", 2) -> {"s0": "A. B.", "s1": "C."}
    """
    # TODO: split `text` into sentences (hint: re.split(r"(?<=[.!?])\s+", text)), group them n at a time.
    raise NotImplementedError


if __name__ == "__main__":
    print(by_sentences("One. Two. Three.", 2))
