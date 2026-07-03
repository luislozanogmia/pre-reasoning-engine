"""Public package API for Pre-Reasoning."""

from __future__ import annotations

from typing import Optional

from .engine_core import ReasoningEngineV25 as ReasoningEngineV25Legacy
from .engine import ReasoningEngineV252
from .inference import ReasoningEngineV3

ReasoningEngine = ReasoningEngineV252
ReasoningEngineV25 = ReasoningEngineV252

__all__ = [
    "ReasoningEngineV25",
    "ReasoningEngineV25Legacy",
    "ReasoningEngineV252",
    "ReasoningEngineV3",
    "ReasoningEngine",
    "analyze",
    "pulse",
    "get_engine",
]


_ENGINE_CACHE: dict = {}


def get_engine(
    *,
    checkpoint_path: Optional[str] = None,
    device: str = "auto",
) -> ReasoningEngineV25:
    """Return a reasoning engine (13.7M neural perception + graph analysis).

    Engines are cached per (checkpoint_path, device): the 13.7M checkpoint
    load (~250 ms) is paid once per process instead of on every analyze()
    call. Set PRE_REASONING_NO_ENGINE_CACHE=1 to restore the old
    build-per-call behavior.
    """
    import os
    if os.environ.get("PRE_REASONING_NO_ENGINE_CACHE") == "1":
        return ReasoningEngine(checkpoint_path=checkpoint_path, device=device)
    key = (checkpoint_path, device)
    engine = _ENGINE_CACHE.get(key)
    if engine is None:
        engine = ReasoningEngine(checkpoint_path=checkpoint_path, device=device)
        _ENGINE_CACHE[key] = engine
    return engine


def analyze(
    text: str,
    *,
    checkpoint_path: Optional[str] = None,
    device: str = "auto",
) -> dict:
    """Analyze problem text and return a structural trace result."""
    return get_engine(
        checkpoint_path=checkpoint_path,
        device=device,
    ).analyze(text)


def pulse(
    original_problem: str,
    response: str,
    *,
    checkpoint_path: Optional[str] = None,
    device: str = "auto",
) -> dict:
    """Check whether a draft response addresses detected root blockers."""
    return get_engine(
        checkpoint_path=checkpoint_path,
        device=device,
    ).pulse(original_problem, response)
