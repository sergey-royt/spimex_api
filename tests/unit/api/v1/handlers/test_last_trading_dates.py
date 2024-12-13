from typing import Any

import pytest
from httpx import AsyncClient

from tests.fixtures import test_cases
from tests.utils import prepare_payload


class TestLastTradingDates:
    @staticmethod
    @pytest.mark.asyncio(loop_scope="module")
    @pytest.mark.parametrize(
        (
            "url",
            "params",
            "expected_status_code",
            "expected_payload",
            "expectation",
        ),
        test_cases.TEST_LAST_TRADING_DATES_PARAMS,
    )
    async def test_last_trading_dates(
        url: str,
        params: dict[str, str],
        expected_status_code: int,
        expected_payload: dict,
        expectation: Any,
        test_client: AsyncClient,
    ) -> None:
        response = await test_client.get(url, params=params)
        assert response.status_code == expected_status_code
        assert prepare_payload(response) == expected_payload
