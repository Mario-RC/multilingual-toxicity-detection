"""Runtime helpers that keep optional ML dependencies lazy."""

from __future__ import annotations


def resolve_device(device: str | None = None) -> str:
    """Return a torch device string without importing torch at package import."""

    if device:
        return device

    import torch

    return "cuda:0" if torch.cuda.is_available() else "cpu"

