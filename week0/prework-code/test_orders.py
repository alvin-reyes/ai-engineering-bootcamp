import asyncio
import time

import pytest

from orders import fetch_all, parse_order


def test_parses_a_good_order():
    order = parse_order('{"order_id": "ORD-1", "status": "shipped", "total": 19.9}')
    assert order.order_id == "ORD-1" and order.total == 19.9


def test_rejects_an_order_with_missing_fields():
    with pytest.raises(ValueError, match="total"):
        parse_order('{"order_id": "ORD-1", "status": "shipped"}')


def test_fetches_concurrently():
    start = time.perf_counter()
    assert len(asyncio.run(fetch_all(["a", "b", "c"]))) == 3
    assert time.perf_counter() - start < 0.25  # three 0.1 s calls at once, not 0.3 s in a row
