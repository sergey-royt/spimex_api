from typing import Sequence

from httpx import Response


def prepare_payload(
    response: Response, exclude: Sequence[str] | None = None
) -> dict:
    """Extracts the payload from the response."""
    payload = response.json().get("payload")
    if payload is None:
        return {}
    return payload
