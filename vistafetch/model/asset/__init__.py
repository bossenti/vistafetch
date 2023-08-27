"""Model several financial assets."""

from vistafetch.model.asset.financial_data import PriceData
from vistafetch.model.asset.fund import Fund
from vistafetch.model.asset.stock import Stock

__all__ = [
    "Fund",
    "PriceData",
    "Stock",
]
