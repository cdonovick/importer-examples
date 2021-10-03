import importlib
import importlib.abc
import importlib.util
import importlib.machinery
import sys
import types
import os

def _call_with_frames_removed(f, *args, **kwargs):
    return f(*args, **kwargs)

def _bounded_repr(obj, n):
    s = repr(obj)
    if len(s) > n:
        return s[0:n-3] + '...'
    else:
        return s

class PrintingImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    @classmethod
    def find_spec(cls, fullname, path, target=None):
        if fullname[0] == '_':
            return None
        print(f'{cls.__name__}.find_spec({fullname}, {path}, {target})')
        if path is None:
            path = sys.path

        spec = None
        for entry in path:
            if not isinstance(entry, str):
                continue
            full_path = f'{entry}/{fullname.split(".")[-1]}'
            if os.path.isdir(full_path):
                full_path_ext = full_path + '/__init__.py'
                is_package = True
            else:
                full_path_ext = full_path + '.py'
                is_package = False

            if os.path.isfile(full_path_ext):
                spec = importlib.machinery.ModuleSpec(fullname, cls, origin=full_path_ext, is_package=is_package)
                spec.has_location = True
                if is_package:
                    spec.submodule_search_locations = [full_path]
                break


        return spec

    @classmethod
    def create_module(cls, spec):
        print(f'{cls.__name__}.create_module({_bounded_repr(spec, 20)})')
        module = types.ModuleType(spec.name)
        module.__spec__ = spec
        module.__name__ = spec.name
        module.__loader__ = spec.loader
        module.__file__ = spec.origin
        module.__path__ = spec.submodule_search_locations
        module.__cached__ = spec.cached
        module.__package__ = spec.parent
        return module

    @classmethod
    def exec_module(cls, module):
        print(f'{cls.__name__}.exec_module({_bounded_repr(module, 20)})\n')
        src_file = module.__file__
        with open(src_file, 'r') as src:
            src_code = src.read()

        _call_with_frames_removed(exec, src_code, module.__dict__)

class PrintingPathFinder(importlib.abc.MetaPathFinder):
    @classmethod
    def find_spec(cls, fullname, path, target=None):
        print(f'{cls.__name__}.find_spec({fullname}, {path}, {target})')
        if path is None:
            path = sys.path

        spec = None
        for entry in path:
            try:
                finder = sys.path_importer_cache[entry]
                print(f'found finder ({_bounded_repr(finder, 10)}) in cache for {entry}')
            except KeyError:
                for hook in sys.path_hooks:
                    try:
                        finder = hook(entry)
                    except ImportError:
                        finder = None
                    if finder is not None:
                        sys.path_importer_cache[entry] = finder
                        print(f'found finder ({_bounded_repr(finder, 10)}) for {entry} from hook ({_bounded_repr(hook, 10)})')
                        break
            if finder is not None:
                spec = finder.find_spec(fullname, target)
                if spec is not None:
                    print(f'found spec {_bounded_repr(spec, 20)}')
                    break
        print()
        return spec

def print_hook(path):
    print(f'print_hook({path})')
    return None
