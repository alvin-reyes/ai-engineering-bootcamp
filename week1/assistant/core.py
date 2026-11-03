"""The assistant itself: history, streaming, a structured summary and clean error handling.

Nothing here talks to the network by itself. `Assistant` is given a `client` (the real `anthropic.Anthropic()`
in the app, a fake in the tests), so you can test every function without an API key.

Your job: replace each `# TODO:` with working code. Do not change the names or signatures: the tests call them.
"""
import json
import os
from dataclasses import dataclass

import anthropic

MODEL = os.environ.get("ASSISTANT_MODEL", "claude-opus-5-5")  # same model as the demos; change it in one place
SYSTEM = "You are a concise assistant for an AI engineering bootcamp. Answer in at most five sentences."

SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["topic", "key_points", "open_questions"],
    "additionalProperties": False,
}


class AssistantError(Exception):
    """A problem the user should see as one plain sentence, never as a traceback."""


@dataclass
class Reply:
    text: str            # the full reply text
    stop_reason: str     # "end_turn", "max_tokens", ...
    truncated: bool      # True when stop_reason == "max_tokens"
    input_tokens: int = 0
    output_tokens: int = 0


def text_of(content) -> str:
    """Join the text of a reply's content. `content` is a string or a list of blocks (objects with .type/.text).

    Given. Use it wherever you need the words of a reply.
    """
    if isinstance(content, str):
        return content
    return "".join(getattr(b, "text", "") for b in content if getattr(b, "type", None) == "text")


def get_api_key(environ=None) -> str:
    """Return ANTHROPIC_API_KEY from `environ` (default: os.environ).

    The key comes from the environment only: never from a file in the repo, never hard-coded.
    Raise AssistantError with a plain message that names the variable if it is missing or empty.
    """
    # TODO: read the variable, raise AssistantError if it is not set
    raise NotImplementedError("get_api_key")


def describe_error(exc: Exception) -> str:
    """Turn an anthropic error into one plain sentence for the user.

    - anthropic.RateLimitError: say you were rate limited and to wait and retry
    - other anthropic.APIStatusError: include the status code and say to fix the request, not just retry
    - anthropic.APIConnectionError: say the API could not be reached (check the network)
    - anything else: a generic sentence
    Check RateLimitError first (it is a kind of APIStatusError).
    """
    # TODO: return the right sentence for each case
    raise NotImplementedError("describe_error")


def validate_summary(data, schema=SUMMARY_SCHEMA) -> list:
    """Check `data` against `schema`. Return a list of problems; an empty list means valid.

    You only need the parts SUMMARY_SCHEMA uses: type object / array / string, "required", "properties",
    "additionalProperties": False and "items". Each problem is a short string, for example
    "missing key: topic" or "key_points: expected array".
    """
    # TODO: check the type, the required keys, extra keys, and the items of each array
    raise NotImplementedError("validate_summary")


class Assistant:
    def __init__(self, client, model=MODEL, system=SYSTEM, max_tokens=2048, write=print):
        self.client = client
        self.model = model
        self.system = system
        self.max_tokens = max_tokens
        self.write = write          # called with each streamed chunk; tests pass a list's .append
        self.history = []           # [{"role": "user" | "assistant", "content": ...}, ...]

    def ask(self, user_text: str, max_tokens: int = None) -> Reply:
        """Send one user turn, stream the reply, remember both sides, return a Reply.

        Steps:
        1. Add the user message to `self.history`.
        2. Stream with `self.client.messages.stream(model=..., max_tokens=..., system=..., messages=self.history)`.
           Call `self.write(chunk)` for every chunk of `stream.text_stream`, then `stream.get_final_message()`.
        3. Add the assistant reply to the history (use `final.content`).
        4. If `final.stop_reason == "max_tokens"`: call `self.write(...)` with a notice that contains the words
           "cut off", and set `truncated=True` on the Reply.
        5. On any `anthropic.APIError`: remove the user message you added (so the history stays clean) and raise
           `AssistantError(describe_error(exc))`.
        """
        # TODO: implement the five steps above
        raise NotImplementedError("Assistant.ask")

    def summary(self, max_tokens: int = None) -> dict:
        """Summarize the conversation as a dict that matches SUMMARY_SCHEMA.

        Steps:
        1. Nothing said yet? Raise AssistantError("nothing to summarize yet").
        2. Call `self.client.messages.create(...)` with `messages=self.history + [one extra user message asking
           for a summary]` and `output_config={"format": {"type": "json_schema", "schema": SUMMARY_SCHEMA}}`.
           Do NOT add the summary request or its answer to `self.history`.
        3. If `stop_reason == "max_tokens"` the JSON is cut off: raise AssistantError with a message that contains
           "cut off". Never try to parse half a JSON object.
        4. Parse the reply text as JSON (bad JSON -> AssistantError), check it with `validate_summary`
           (problems -> AssistantError), and return the dict.
        5. Wrap anthropic.APIError the same way as in `ask`.
        """
        # TODO: implement the five steps above
        raise NotImplementedError("Assistant.summary")
