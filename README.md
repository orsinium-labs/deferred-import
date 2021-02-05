# deferred-import

Lazy import and install on demand Python packages

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
