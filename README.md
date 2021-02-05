# deferred-import

Lazy import and install on demand Python packages.

1. Package will be loaded only when you use it in the first time. Deferring it makes module loading much faster.
1. If module is missed, the package will be automatically installed. It allows to make some project dependencies optional and install them on demand.

## Installation

```bash
python3 -m pip install --user deferred-import
```

## Usage

```python
from deferred_import import deferred_import

requests = deferred_import('requests')
attr = deferred_import('attr', package='attrs')

requests.get('http://httpbin.org/status/200')
# <Response [200]>
```
