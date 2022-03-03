# Telenotify

## install

`pip install telenotify`

## example usage

```python
from telenotify import Telenotify


class CustomNotify(Telenotify):
    def get_update(self):
        return "woof!!"


CustomNotify("token", 60)
```
