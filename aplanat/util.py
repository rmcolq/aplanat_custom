"""Utility functions for aiding plotting."""

import numpy as np


class Limiter(object):
    """Helper class to determine limits of data."""

    def __init__(self, limits=None):
        """Initialize the limit gathering."""
        if limits is not None:
            self.min, self.max = limits
        else:
            self.min, self.max = +float('inf'), -float('inf')

    def accumulate(self, data):
        """Analyse data to update limits.

        :param data: new data to analyse.

        """
        self.min = min(self.min, min(data))
        self.max = max(self.max, max(data))
        return self

    def fix(self, lower=None, upper=None):
        """Fix limits to new values.

        :param lower: new lower limit.
        :param upper: new upper limit.

        """
        if lower is not None:
            self.min = lower
        if upper is not None:
            self.max = upper
        return self


def pad(data):
    """Attempt to find a sensible plot bounds for a vector."""
    uniq = sorted(np.unique(data))
    pad = 0.5 * min(np.ediff1d(uniq))
    return uniq[0] - pad, uniq[-1] + pad
