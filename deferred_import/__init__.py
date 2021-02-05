"""Lazy import and install on demand Python packages.
"""

# app
from ._core import LazyModule as deferred_import


__version__ = '0.1.0'
__all__ = ['deferred_import']
