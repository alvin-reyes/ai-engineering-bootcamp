"""The terminal loop. `handle` runs one line and is what the tests call; `main` wires it to a real client.

    python -m assistant          chat; the whole history is sent every turn
    /summary                     the conversation as JSON that matches SUMMARY_SCHEMA
    /short <text>                ask with a tiny max_tokens to see the cut-off notice
    /quit                        leave
"""
import json

import anthropic

from .core import Assistant, AssistantError, get_api_key


def handle(assistant: Assistant, line: str, out=print) -> bool:
    """Run one line of input. Return False to stop the loop, True to keep going.

    - ""            nothing to do
    - "/quit"       return False
    - "/summary"    print `json.dumps(assistant.summary(), indent=2)` with `out`
    - "/short ..."  `assistant.ask(rest_of_line, max_tokens=25)`
    - anything else `assistant.ask(line)` (the reply is streamed by the assistant, so do not print it again)
    Catch AssistantError, print `[error: <message>]` with `out`, and return True: the app must not crash.
    """
    # TODO: implement the commands above
    raise NotImplementedError("handle")


def main():
    try:
        key = get_api_key()
    except AssistantError as exc:
        raise SystemExit(f"[error: {exc}]")
    assistant = Assistant(anthropic.Anthropic(api_key=key), write=lambda chunk: print(chunk, end="", flush=True))
    while True:
        try:
            line = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not handle(assistant, line):
            break
