import sys
from url_importer import UrlLoader
sys.path_hooks.append(UrlLoader.hook)

sys.path.append(r'https://raw.githubusercontent.com/cdonovick/SMT-PNR/master/pnrdoctor/util/data_structures/')

import bidict
print(bidict)
print(dir(bidict))
