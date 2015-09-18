import warnings

try: ImportWarning
except NameError:
    class ImportWarning(Warning):
        pass

from randomForest import randomForest

