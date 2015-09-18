import warnings

try: ImportWarning
except NameError:
    class ImportWarning(Warning):
        pass

from generateSampleData import generateSampleData

