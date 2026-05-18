from clerk_fetchers.fetchers.alamedausd_ca import AlamedaUSDFetcher
from clerk_fetchers.fetchers.example_city import ExampleCityFetcher
from clerk_fetchers.fetchers.berkeley_ca import BerkeleyCAFetcher
from clerk_fetchers.fetchers.houston_tx import HoustonTXFetcher
from clerk_fetchers.fetchers.senado_pr import SenadoPRFetcher


FETCHER_REGISTRY = {
    "example_city": ExampleCityFetcher,
    "alamedausd.ca": AlamedaUSDFetcher,
    "berkeley.ca": BerkeleyCAFetcher,
    "houston.tx": HoustonTXFetcher,
    "senado.pr": SenadoPRFetcher,
}

EXTRA_REGISTRY = {
    "example_city": {"base_url": "https://example-city.gov/meetings"},
}
