import typing as t
from time import sleep
from urllib.parse import urlencode

import httpx

SEA_DATA_URL_FMT = "https://data.seattle.gov/resource/{dataset_id}.json"


# A collection of well-known datasets that we've given friendly names to.
SEA_DATASETS: dict[str, str] = {
    # Building permits
    # https://data.seattle.gov/Built-Environment/Building-Permits/76t5-zqzr/about_data
    "building_permits": "76t5-zqzr",
    # Issued building permits -- not sure I understand the difference
    # https://data.seattle.gov/Built-Environment/Issued-Building-Permits/8tqq-u7ib/about_data
    "issued_building_permits": "8tqq-u7ib",
    # Land use applications submitted to the City of Seattle
    # https://data.seattle.gov/Built-Environment/Land-Use-Permits/ht3q-kdvx/about_data
    "land_use_permits": "ht3q-kdvx",
    # Trade permits issued by the SDCI
    # https://data.seattle.gov/Built-Environment/Trade-Permits/c87v-5hwh/about_data
    "trade_permits": "c87v-5hwh",
    # Electrical permits issued by the SDCI
    # https://data.seattle.gov/Built-Environment/Electrical-Permits/c4tj-daue/about_data
    "electrical_permits": "c4tj-daue",
    # Plan reviews conducted by the SDCI
    # https://data.seattle.gov/Built-Environment/Plan-Review/tqk8-y2z5/about_data
    "plan_reviews": "tqk8-y2z5",
    # Plan comments submitted to the SDCI
    # https://data.seattle.gov/Built-Environment/Plan-Comments/e285-aq8h/about_data
    "plan_comments": "e285-aq8h",
}


def get_sea_data_url(dataset_id: str, *, offset: int = 0, limit: int = 1_000) -> str:
    base_url = SEA_DATA_URL_FMT.format(dataset_id=dataset_id)
    query = urlencode({"$offset": offset, "$limit": limit})
    return f"{base_url}?{query}"


def _get_sea_data_page(
    dataset_id: str, *, offset: int = 0, limit: int = 1_000, retries: int = 3
) -> list[dict]:
    """
    Fetch a single page of data from a Seattle Open Data dataset.

    If the request fails, it will be retried up to `retries` times after
    a short delay.
    """
    url = get_sea_data_url(dataset_id, offset=offset, limit=limit)
    attempt = 0
    while attempt < retries + 1:
        try:
            response = httpx.get(url)
            response.raise_for_status()
            maybe = response.json()
            # Sanity checks; if this fails we have a bug or the API has changed.
            if not isinstance(maybe, list):
                raise ValueError(f"Expected a list, got {type(maybe)}: {maybe}")
            if maybe and not isinstance(maybe[0], dict):
                raise ValueError(
                    f"Expected a list of dicts, got {type(maybe[0])}: {maybe}"
                )
            return maybe
        except httpx.HTTPError, httpx.ConnectError:
            if attempt == retries:
                raise
            sleep(0.5 * 2 ** (attempt + 1))
        attempt += 1
    raise RuntimeError("Unreachable")


def get_sea_data(
    dataset_id: str,
    *,
    offset: int = 0,
    limit: int = 1_000,
    single: bool = False,
    retries: int = 3,
) -> t.Iterable[dict]:
    """
    Fetch data from a Seattle Open Data dataset.

    If `single` is True, return only a single page of results as an iterable
    of dicts. If False, return a generator that yields all results by
    fetching multiple pages as needed.
    """
    current_offset = offset
    while True:
        page = list(
            _get_sea_data_page(
                dataset_id, offset=current_offset, limit=limit, retries=retries
            )
        )
        if not page:
            break
        yield from page
        if single:
            break
        current_offset += limit
