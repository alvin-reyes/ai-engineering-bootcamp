"""Step 3: answer from the retrieved chunks, with citations, or say "I don't know"."""
import os
from dataclasses import dataclass, field

from .retrieve import Retriever

MODEL = os.environ.get("MODEL", "claude-opus-5-5")  # VERIFY the model id you have access to
NO_ANSWER = "I don't know. The documents do not answer this question."
SYSTEM = ("Answer only from the chunks. Cite the chunk id in square brackets after each claim, like "
          "[returns.md#refunds]. If the chunks do not answer the question, say you don't know.")


@dataclass
class Answer:
    text: str
    citations: list[str] = field(default_factory=list)  # chunk ids actually retrieved and cited
    answered: bool = False                             # False means "I don't know"


def get_client():
    """The real client. Needs ANTHROPIC_API_KEY. (Given.) Tests pass a fake client instead."""
    import anthropic
    return anthropic.Anthropic()


def build_prompt(question: str, hits) -> str:
    """One <chunk id="..."> ... </chunk> block per hit (blank line between), then a blank line and
    'Question: <question>'. The id is the chunk id: the model cites it."""
    # TODO
    raise NotImplementedError


def extract_citations(text: str, allowed_ids) -> list[str]:
    """Chunk ids written in [square brackets] in `text`, in order of first appearance, no repeats.
    Only ids in `allowed_ids` count: a made-up citation is ignored."""
    # TODO
    raise NotImplementedError


def answer_question(question: str, retriever: Retriever, client, k: int = 3) -> Answer:
    """Retrieve, ask the model, check the result.

    - No retrieval hits: return Answer(NO_ANSWER) WITHOUT calling the model.
    - Otherwise call client.messages.create(model=MODEL, max_tokens=..., system=SYSTEM, messages=[...]) and read
      the first text block of response.content.
    - If the reply has no valid citation, or says it doesn't know: return Answer(NO_ANSWER). An uncited answer
      is not accepted.
    - Otherwise Answer(text, citations, answered=True).
    """
    # TODO
    raise NotImplementedError
