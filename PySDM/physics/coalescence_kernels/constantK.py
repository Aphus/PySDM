"""
Created at 14.05.2021
"""

import numpy as np
from scipy import special


class ConstantK:

    def __init__(self, a):
        self.a = a
        self.core = None

    def __call__(self, output, is_first_in_pair):
        output = self.a

    def register(self, builder):
        self.core = builder.core
