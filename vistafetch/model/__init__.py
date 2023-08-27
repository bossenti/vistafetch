"""Collection of model classes.

All model classes are defined using Pydantic.
"""
from vistafetch.model.asset import Fund, Stock
from vistafetch.model.search_result import SearchResult

__all__ = [
    "Fund",
    "Stock",
    "SearchResult",
]
