import importlib
import importlib.abc
import importlib.util
import importlib.machinery
import sys
import types
import os
import tokenize
import token
import io

def _call_with_frames_removed(f, *args, **kwargs):
    return f(*args, **kwargs)

class MacroImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, ext='.px'):
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
        with open(src_file, 'rb') as src:
            tokens = list(tokenize.tokenize(src.readline))

        skip = False
        token_strm = []
        for t1, t2 in zip(tokens, tokens[1:]):

            if skip:
                skip = False
            elif t1.type == token.NAME and t1.string == 'e' and t2.type == token.STRING:
                new_tokens = tokenize.tokenize(io.BytesIO(f'exec(f{t2.string})'.encode()).readline)
                next(new_tokens)
                token_strm.extend((t.type, t.string) for t in new_tokens)
                skip = True
            else:
                token_strm.append((t1.type, t1.string))
        if not skip:
            token_strm.append((t2.type, t2.string))

        src_code = tokenize.untokenize(token_strm)
        _call_with_frames_removed(exec, src_code, module.__dict__)

