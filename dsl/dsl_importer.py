import importlib
import importlib.abc
import importlib.util
import importlib.machinery
import sys
import types
import os

def _call_with_frames_removed(f, *args, **kwargs):
    return f(*args, **kwargs)

class DSLImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, dict_t=dict, ext='.px'):
        self.dict_t = dict_t
        self.ext = ext

    def find_spec(self, fullname, path, target=None):
        if path is None:
            path = sys.path

        for entry in path:
            if entry == '':
                entry = os.getcwd()

            full_path = f'{entry}/{fullname}.{self.ext}'
            if os.path.isfile(full_path):
                spec = importlib.machinery.ModuleSpec(fullname, self, origin=full_path)
                spec.has_location = True
                break
        else:
            spec = None

        return spec

    def create_module(self, spec):
        module = types.ModuleType(spec.name)
        module.__spec__ = spec
        module.__name__ = spec.name
        module.__loader__ = spec.loader
        module.__file__ = spec.origin
        module.__path__ = spec.submodule_search_locations
        module.__cached__ = spec.cached
        module.__package__ = spec.parent
        return module

    def exec_module(self, module):
        src_file = module.__file__
        with open(src_file, 'r') as src:
            src_code = src.read()

        namespace = self.dict_t()
        _call_with_frames_removed(exec, src_code, module.__dict__, namespace)
        module.__dict__.update(namespace)













def _comment():
        namespace['types'] = types.ModuleType
        namespace['types'] = types
