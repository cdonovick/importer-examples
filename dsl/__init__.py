import sys
from .dsl_importer import DSLImporter
from .type_check import TypeCheckDict
sys.meta_path.append(DSLImporter(TypeCheckDict, 'px'))
