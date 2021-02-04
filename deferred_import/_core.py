# built-in
import subprocess
import sys
from importlib import import_module
from logging import getLogger
from pathlib import Path


logger = getLogger(__package__)


def _is_global() -> bool:
    venv_root = Path(sys.executable).parent.parent
    return not (venv_root / 'pyvenv.cfg').exists()


def _install(name: str) -> None:
    logger.warning('cannot find {name}, trying to install')
    args = [sys.executable, '-m', 'pip', 'install']
    if _is_global():
        args.append('--user')
    args.append(name)
    code = subprocess.call(args)
    if code != 0:
        raise RuntimeError('cannot install package {}'.format(name))


class cached_property:
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    """

    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class LazyModule:
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

    @cached_property
    def _module(self):
        try:
            return import_module(name=self._name)
        except ImportError:
            if not self._install:
                raise
            _install(name=self._package)
        return import_module(name=self._name)

    def __getattr__(self, name: str):
        return getattr(self._module, name)

    def __dir__(self):
        return dir(self._module)

    def __repr__(self) -> str:
        return '{t}({n})'.format(
            t=type(self).__name__,
            n=self._name,
        )
