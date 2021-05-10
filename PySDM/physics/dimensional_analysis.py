"""
Crated at 2019
"""

from importlib import reload
from PySDM.physics import constants
from PySDM.physics import formulae
from PySDM.physics.impl import flag


class DimensionalAnalysis:

    def __enter__(*_):
        flag.DIMENSIONAL_ANALYSIS = True
        reload(constants)
        reload(formulae)

    def __exit__(*_):
        flag.DIMENSIONAL_ANALYSIS = False
        reload(constants)
        reload(formulae)
