""" module shared_types """

from typing import TypedDict

class CountryData(TypedDict):
    """Custom type for CountryData"""
    name: str
    capital: str
    population: str
    area: float
