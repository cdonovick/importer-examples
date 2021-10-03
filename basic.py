from printing_importers import *
import sys

sys.meta_path.insert(0, PrintingImporter)
#sys.path_importer_cache.clear()
#sys.meta_path.insert(0, PrintingPathFinder)
#sys.path_hooks.insert(0, print_hook)

import os
import package.sub1.file
print('---')
import package
del package
import package
print('---')
sys.modules.clear()
import package
