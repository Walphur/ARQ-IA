"""Id generator for request/correlation ids."""

from __future__ import annotations

import re
import uuid
from typing import Optional

_SAFE = re.compile(r"^[A-Za-z0-9._:-]+$")
_MAX_LEN = 128


class UuidIdGenerator:
    def new_request_id(self) -> str:
        return str(uuid.uuid4())

    def sanitize_request_id(self, raw: Optional[str]) -> str:
        if not raw:
            return self.new_request_id()
        value = raw.strip()
        if not value or len(value) > _MAX_LEN or not _SAFE.match(value):
            return self.new_request_id()
        return value
