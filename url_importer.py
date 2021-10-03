import importlib
import importlib.abc
import importlib.util
import importlib.machinery
import urllib.request
import sys
import types
import re


_UC = r'[a-zA-Z0-9_-]+'
_url_re = re.compile(rf'(https?://)?({_UC}\.)+(\w+)(/{_UC})*/?')

class UrlLoader(importlib.abc.PathEntryFinder, importlib.abc.SourceLoader):
    def __init__(self, url):
        if url[-1] != '/':
            url += '/'
        self._url = url

    def find_spec(self, fullname, target=None):
        spec = importlib.machinery.ModuleSpec(fullname, self, origin=self.get_filename(fullname))
        spec.has_location = True
        return spec

    def get_data(self, path):
        try:
            return urllib.request.urlopen(path).read()
        except:
            pass

        raise ImportError()



    def get_filename(self, fullname):
        return self._url + fullname + '.py'

    @classmethod
    def hook(cls, path):
        if _url_re.fullmatch(path):
            return cls(path)
        else:
            return None


