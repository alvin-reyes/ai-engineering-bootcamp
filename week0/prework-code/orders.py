"""Builder prework: typed functions, a dataclass, and an async fan-out."""
import asyncio
import json
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    status: str
    total: float


def parse_order(raw: str) -> Order:
    """Parse one order from JSON text, failing loudly on bad input."""
    data = json.loads(raw)
    missing = {"order_id", "status", "total"} - data.keys()
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    return Order(order_id=str(data["order_id"]), status=str(data["status"]), total=float(data["total"]))


async def fetch_status(order_id: str) -> str:
    await asyncio.sleep(0.1)  # stands in for a slow network call
    return f"{order_id}: delivered"


async def fetch_all(order_ids: list[str]) -> list[str]:
    # run the slow calls at the same time, not one after another
    return await asyncio.gather(*(fetch_status(o) for o in order_ids))


if __name__ == "__main__":
    print(parse_order('{"order_id": "ORD-1", "status": "shipped", "total": "19.90"}'))
    print(asyncio.run(fetch_all(["ORD-1", "ORD-2", "ORD-3"])))
