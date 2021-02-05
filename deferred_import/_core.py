# built-in
import subprocess
import sys
from importlib import import_module
from logging import getLogger
from pathlib import Path
from types import ModuleType
from typing import List


logger = getLogger(__package__)


def _is_global() -> bool:
    venv_root = Path(sys.executable).parent.parent
    return not (venv_root / 'pyvenv.cfg').exists()


def _install(name: str) -> None:
    logger.warning(f'cannot find {name}, trying to install')
    args = [sys.executable, '-m', 'pip', 'install']
    if _is_global():
        args.append('--user')
    args.append(name)
    code = subprocess.call(args, stdout=subprocess.DEVNULL)
    if code != 0:
        raise RuntimeError(f'cannot install package {name}')


class LazyModule:
    __slots__ = (
        '_name',
        '_package',
        '_install',
    )

    def __init__(
        self,
        name: str,
        package: str = None,
        install: bool = True,
        eager: bool = False,
    ):
        self._name = name
        self._package = package or name.split('.', maxsplit=1)[0]
        self._install = install
        if eager:
            self._module

    def _import(self) -> ModuleType:
        try:
            return import_module(name=self._name)
        except ImportError:
            if not self._install:
                raise
            _install(name=self._package)
        return import_module(name=self._name)

    @property
    def _module(self) -> ModuleType:
        return sys.modules.get(self._name) or self._import()

    def __getattr__(self, name: str):
        return getattr(self._module, name)

    def __dir__(self) -> List[str]:
        return dir(self._module)

    def __repr__(self) -> str:
        return '{t}({n})'.format(
            t=type(self).__name__,
            n=self._name,
        )
