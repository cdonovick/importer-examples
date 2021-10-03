from collections.abc import MutableMapping

class _MISSING: pass

class TypeCheckDict(dict, MutableMapping):
    __slots__ = '_d'
    def __init__(self, d=_MISSING):
        if d is _MISSING:
            d = {}
        self._d = d

    def __getitem__(self, name):
        v = self._d[name][1]
        if v is _MISSING:
            raise ValueError()
        else:
            return v

    def __setitem__(self, name, value):
        if name not in self._d:
            if isinstance(value, type):
                self._d[name] = [value, _MISSING]
            else:
                self._d[name] = [type(value), value]
        elif isinstance(value, self._d[name][0]):
            self._d[name][1] = value
        else:
            raise TypeError(f'{value} is not a {self._d[name][0]}')


    def __delitem__(self, name):
        return self._d.__delitem__(name)

    def __iter__(self):
        return self._d.__iter__()

    def __len__(self):
        return self._d.__len__()
