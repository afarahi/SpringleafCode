import warnings

try: ImportWarning
except NameError:
    class ImportWarning(Warning):
        pass

from readData import readData
