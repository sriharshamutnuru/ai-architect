# -*- coding: utf-8 -*-
"""
Week 2 Weekend Project — APIClient with bfsi_tools package
Combines: classes (Day 1), dataclasses (Day 2),
error handling + logging (Day 3), modules (Day 4), pip/venv (Day 5)

This is the skeleton your Week 5 Anthropic client inherits from.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

from bfsi_tools import (
    parse_circular,
    parse_bank,
    Circular,
    Bank,
    CircularParseError,
    MissingFieldError,
)

# ── Load environment config ───────────────────────────────
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APP_ENV   = os.getenv("APP_ENV", "development")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Config dataclass ──────────────────────────────────────
@dataclass(frozen=True)
class ClientConfig:
    base_url:    str
    api_key:     str
    max_retries: int   = 3
    timeout:     float = 30.0
    environment: str   = "development"

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("api_key cannot be empty")
        if self.max_retries < 1:
            raise ValueError("max_retries must be at least 1")


# ── Response dataclass ────────────────────────────────────
@dataclass
class APIResponse:
    success:  bool
    data:     Optional[object]   = None
    error:    Optional[str]      = None
    call_num: int                = 0

    def __repr__(self) -> str:
        if self.success:
            return f"APIResponse(ok, call={self.call_num}, data={self.data})"
        return f"APIResponse(failed, call={self.call_num}, error={self.error})"


# ── APIClient class ───────────────────────────────────────
class APIClient:
    """
    A typed API client that wraps bfsi_tools parsing.
    This exact structure is what your Week 5 Anthropic
    and OpenAI clients will be based on.
    """

    def __init__(self, config: ClientConfig):
        self.config     = config
        self.call_count = 0
        self._errors:   list[str] = []
        logger.info(
            f"APIClient initialised — env={config.environment} "
            f"retries={config.max_retries}"
        )

    def _make_call(self, payload: str) -> APIResponse:
        """Internal — simulate one API call with error tracking."""
        self.call_count += 1
        logger.debug(f"Call #{self.call_count}: {payload[:40]}...")
        return APIResponse(success=True, call_num=self.call_count)

    def get_circular(self, payload: str) -> APIResponse:
        """Parse a circular payload. Returns APIResponse with Circular or error."""
        response = self._make_call(payload)
        try:
            circular = parse_circular(payload)
            if circular is None:
                error_msg = "Parser returned None"
                self._errors.append(error_msg)
                return APIResponse(
                    success=False,
                    error=error_msg,
                    call_num=self.call_count,
                )
            logger.info(f"Circular parsed: {circular.circular_id}")
            response.data = circular
            return response
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self._errors.append(str(e))
            return APIResponse(
                success=False,
                error=str(e),
                call_num=self.call_count,
            )

    def get_bank(self, payload: str) -> APIResponse:
        """Parse a bank payload. Returns APIResponse with Bank or error."""
        response = self._make_call(payload)
        try:
            bank = parse_bank(payload)
            if bank is None:
                error_msg = "Parser returned None"
                self._errors.append(error_msg)
                return APIResponse(
                    success=False,
                    error=error_msg,
                    call_num=self.call_count,
                )
            logger.info(f"Bank parsed: {bank.name}")
            response.data = bank
            return response
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                call_num=self.call_count,
            )

    def stats(self) -> dict:
        """Return client usage statistics."""
        return {
            "total_calls":   self.call_count,
            "total_errors":  len(self._errors),
            "success_rate":  (
                f"{(self.call_count - len(self._errors)) / max(self.call_count, 1):.0%}"
            ),
            "environment":   self.config.environment,
        }

    def __repr__(self) -> str:
        return (
            f"APIClient(url='{self.config.base_url}', "
            f"calls={self.call_count}, "
            f"errors={len(self._errors)})"
        )


# ── Main ──────────────────────────────────────────────────
def main() -> None:
    # Build config from environment
    config = ClientConfig(
        base_url    = "https://api.rbi.gov.in",
        api_key     = os.getenv("ANTHROPIC_API_KEY", "demo-key"),
        max_retries = 3,
        environment = APP_ENV,
    )

    client = APIClient(config)

    # ── Circular calls ────────────────────────────────────
    circular_payloads = [
        '{"id": "RBI/101", "tier": "high",   "pages": 36, "tags": ["kyc"]}',
        '{"id": "RBI/102", "tier": "medium", "pages": 8}',
        '{"id": "RBI/103",                   "pages": 24}',
        'not valid json',
        '{"tier": "high", "pages": 12}',
    ]

    print("\n── Circular results ──")
    for p in circular_payloads:
        resp = client.get_circular(p)
        if resp.success and resp.data:
            c = resp.data
            print(f"  ✓ {c.summary()} → {c.classify()}")
        else:
            print(f"  ✗ call #{resp.call_num}: {resp.error}")

    # ── Bank calls ────────────────────────────────────────
    bank_payloads = [
        '{"name": "HDFC",     "npa": 1.2, "branches": 6800}',
        '{"name": "Yes Bank", "npa": 5.1, "branches": 1100}',
        '{"npa": 3.5}',
    ]

    print("\n── Bank results ──")
    for p in bank_payloads:
        resp = client.get_bank(p)
        if resp.success and resp.data:
            b = resp.data
            print(f"  ✓ {b.summary()}")
        else:
            print(f"  ✗ call #{resp.call_num}: {resp.error}")

    # ── Stats ─────────────────────────────────────────────
    print("\n── Client stats ──")
    for key, val in client.stats().items():
        print(f"  {key:<16} {val}")

    print(f"\n{client}")


if __name__ == "__main__":
    main()