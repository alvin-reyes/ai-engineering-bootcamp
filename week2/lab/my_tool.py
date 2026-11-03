"""Lab Part 3: design ONE tool from your capstone canvas. Fill in every TODO, then run `pytest tests/test_lab_tool.py`.

Test your description on a partner (or Claude): "given only this description, when would you call this tool, and
what would you pass?" If the answer is wrong, the description is the bug.
"""

TOOL = {
    "name": "TODO_tool_name",
    # TODO: three lines: when to use it, what it returns, what it is NOT for.
    "description": "TODO",
    "input_schema": {
        "type": "object",
        "properties": {},          # TODO: your fields, each with a type
        "required": [],            # TODO: the fields the model must always send
        "additionalProperties": False,
    },
}

WRITES = None       # TODO: True if the tool changes anything (sends, saves, refunds, deletes), else False
APPROVAL = ""       # TODO: if WRITES, who approves and when, in one sentence. Else leave empty.

EXAMPLE_GOOD = {}   # TODO: one valid input
EXAMPLE_BAD = {}    # TODO: one bad input (missing field, wrong type, or an extra field)


def validate(args):
    """Return None if args are fine, else the error message your tool should send back to the model.

    A good error says what was wrong and what to send instead.
    """
    # TODO
    raise NotImplementedError("TODO: validate")
