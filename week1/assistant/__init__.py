"""Week 1 build: a streaming CLI assistant with history and a structured summary."""
from .core import (  # noqa: F401
    MODEL, SUMMARY_SCHEMA, Assistant, AssistantError, Reply,
    describe_error, get_api_key, text_of, validate_summary,
)
