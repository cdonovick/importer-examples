import sys
from .macro_importer import MacroImporter
sys.meta_path.append(MacroImporter('px'))

