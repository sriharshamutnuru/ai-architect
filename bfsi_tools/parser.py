# -*- coding: utf-8 -*-
# bfsi_tools/parser.py — parsing raw JSON into domain objects

import json
import logging

from .models import Circular, Bank
from .exceptions import CircularParseError, MissingFieldError

logger = logging.getLogger(__name__)


def parse_circular(raw: str) -> Circular | None:
    """Parse a JSON string into a Circular. Returns None on failure."""
    try:
        data = json.loads(raw)
        if "id" not in data:
            raise MissingFieldError("Required field 'id' is missing")
        return Circular(
            circular_id=data["id"],
            tier=data.get("tier", "low"),
            pages=data.get("pages", 0),
            tags=data.get("tags", []),
        )
    except json.JSONDecodeError as e:
        logger.error(f"Bad JSON: {e}")
    except MissingFieldError as e:
        logger.error(f"Missing field: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


def parse_bank(raw: str) -> Bank | None:
    """Parse a JSON string into a Bank. Returns None on failure."""
    try:
        data = json.loads(raw)
        if "name" not in data or "npa" not in data:
            raise MissingFieldError("Required fields: name, npa")
        return Bank(
            name=data["name"],
            npa=float(data["npa"]),
            branches=data.get("branches", 0),
        )
    except json.JSONDecodeError as e:
        logger.error(f"Bad JSON: {e}")
    except MissingFieldError as e:
        logger.error(f"Missing field: {e}")
    return None