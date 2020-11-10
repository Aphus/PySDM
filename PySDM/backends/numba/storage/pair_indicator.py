"""
Created at 09.11.2020
"""

from PySDM.backends.numba.impl._algorithmic_step_methods import AlgorithmicStepMethods
from PySDM.backends.numba.storage.storage import Storage


class PairIndicator:

    def __init__(self, length):
        self.indicator = Storage.empty(length, dtype=int)  # TODO bool
        self.length = length

    def update(self, cell_start, cell_id):
        AlgorithmicStepMethods.find_pairs_body(
            cell_start.data, self.indicator.data, cell_id.data, cell_id.idx.data, len(cell_id))
        self.length = len(cell_id)
