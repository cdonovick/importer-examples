import importlib
import importlib.abc
import importlib.util
import importlib.machinery

class DumbyImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    @staticmethod
    def find_spec(fullname, path, target=None):
        print(f'DumbyImporter.find_spec({fullname}, {path}, {target})')
        return None


    @staticmethod
    def hook(path):
        print(f'DumbyImporter.hook({path})')
        return None


