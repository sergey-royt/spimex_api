from contextlib import nullcontext as does_not_raise

from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY


TEST_LAST_TRADING_DATES_PARAMS = [
    # default
    (
        "/last_trading_dates/",
        {},
        HTTP_200_OK,
        [
            "2024-11-01",
            "2024-10-28",
            "2024-10-25",
            "2024-10-24",
            "2024-10-23",
            "2024-10-22",
            "2024-10-21",
            "2024-10-18",
            "2024-10-17",
            "2024-10-16",
        ],
        does_not_raise(),
    ),
    # count = 5
    (
        "/last_trading_dates/",
        {"count": 5},
        HTTP_200_OK,
        [
            "2024-11-01",
            "2024-10-28",
            "2024-10-25",
            "2024-10-24",
            "2024-10-23",
        ],
        does_not_raise(),
    ),
    # error count less than 1
    (
        "/last_trading_dates/",
        {"count": 0},
        HTTP_422_UNPROCESSABLE_ENTITY,
        {},
        does_not_raise(),
    ),
]
