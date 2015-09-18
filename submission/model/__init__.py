import warnings

try: ImportWarning
except NameError:
    class ImportWarning(Warning):
        pass

from randomForest import randomForest
from extraTrees import extraTrees
from adaBoost import adaBoost

