"""Request-scoped context via contextvars."""

from __future__ import annotations

from contextvars import ContextVar, Token
from typing import Any, Optional

_context: ContextVar[dict[str, Any]] = ContextVar("arqia_obs_context", default={})


def get_context() -> dict[str, Any]:
    return dict(_context.get())


def bind(**fields: Any) -> Token:
    current = get_context()
    merged = {**current, **{k: v for k, v in fields.items() if v is not None}}
    return _context.set(merged)


def reset(token: Token) -> None:
    _context.reset(token)


def clear() -> Token:
    return _context.set({})


def get_field(name: str) -> Optional[Any]:
    return get_context().get(name)
