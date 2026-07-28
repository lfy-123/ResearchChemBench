from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from researchchem_job import JobContext


ctx = JobContext.load()
data = np.loadtxt(ctx.input("data"), delimiter=",", skiprows=1)
figure, axis = plt.subplots(figsize=(6, 4))
axis.plot(data[:, 0], data[:, 1], marker="o")
axis.set_xlabel("Coordinate")
axis.set_ylabel("Value")
figure.tight_layout()
figure.savefig(ctx.output("figure"), dpi=200)
plt.close(figure)
ctx.register_output("figure")
