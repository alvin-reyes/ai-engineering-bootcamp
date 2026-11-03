"""Step 4: measure retrieval (recall@k) and answers (accuracy) over an eval-set file."""
import json
from dataclasses import dataclass
from pathlib import Path

from .answer import answer_question
from .retrieve import Retriever


@dataclass(frozen=True)
class EvalCase:
    id: str
    question: str
    answerable: bool
    source: str | None        # document that holds the answer (None if unanswerable)
    must_contain: str | None  # phrase a correct answer must contain (None if unanswerable)


def load_eval_set(path) -> list[EvalCase]:
    """Read a JSONL file: one JSON object per line with id, question, answerable, source, must_contain.
    Skip blank lines. `source` and `must_contain` may be missing or null for unanswerable cases."""
    # TODO
    raise NotImplementedError


def recall_at_k(cases, retriever: Retriever, k: int) -> float:
    """Share of ANSWERABLE cases where a chunk from the expected source document is in the top k hits.
    Unanswerable cases are ignored. Return 0.0 if there are no answerable cases."""
    # TODO
    raise NotImplementedError


def is_correct(case: EvalCase, ans) -> bool:
    """Unanswerable case: correct only if the system did NOT answer.
    Answerable case: correct only if it answered, the answer contains `must_contain` (ignore case),
    and at least one citation points into the expected source document."""
    # TODO
    raise NotImplementedError


def run_eval(cases, retriever: Retriever, client, k: int = 5) -> dict:
    """Run every case. Return {"n": number of cases, "recall_at_k": ..., "accuracy": share correct,
    "failures": [ids of the wrong cases, in order]}. Answer each case with answer_question(..., k=min(k, 3))."""
    # TODO
    raise NotImplementedError
