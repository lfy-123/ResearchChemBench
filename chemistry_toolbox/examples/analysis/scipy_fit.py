from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

from researchchem_job import JobContext


def linear(x, slope, intercept):
    return slope * x + intercept


ctx = JobContext.load()
data = np.loadtxt(ctx.input("data"), delimiter=",", skiprows=1)
parameters, covariance = curve_fit(linear, data[:, 0], data[:, 1])
ctx.write_json(
    "fit",
    {
        "slope": float(parameters[0]),
        "intercept": float(parameters[1]),
        "standard_errors": np.sqrt(np.diag(covariance)).tolist(),
    },
)
