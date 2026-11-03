"""Lab Part 3: the tool you designed from your canvas (lab/my_tool.py). Checks the shape, not your idea."""
import pytest

my_tool = pytest.importorskip("lab.my_tool")


def test_schema_is_strict_and_described():
    t = my_tool.TOOL
    assert t["name"] and len(t["description"]) >= 40
    schema = t["input_schema"]
    assert schema["type"] == "object" and schema["additionalProperties"] is False
    assert schema["required"] and set(schema["required"]) <= set(schema["properties"])


def test_good_input_passes_and_bad_input_gets_a_useful_error():
    assert my_tool.validate(my_tool.EXAMPLE_GOOD) is None
    error = my_tool.validate(my_tool.EXAMPLE_BAD)
    assert isinstance(error, str) and len(error) > 15, "the error should say what was wrong and what to send instead"


def test_a_write_tool_names_its_approval_step():
    assert my_tool.WRITES in (True, False)
    if my_tool.WRITES:
        assert my_tool.APPROVAL.strip(), "a tool that writes must say who approves it, and when"
