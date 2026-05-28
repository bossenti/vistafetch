"""Requests session to be commonly shared.

Attributes
----------
api_session: Session to communicate with the API

"""

import os
from requests import Session

__all__ = [
    "api_session",
]


api_session = Session()
api_session.headers.update({"User-Agent": os.environ.get("VISTAFETCH_USER_AGENT", "vistafetch/1.0")})