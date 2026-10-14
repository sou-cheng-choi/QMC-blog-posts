# Run from the QMC-blog-posts repository root:
#   python PortfolioSimplex/code/simplex_bias.py
# Or from PortfolioSimplex:
#   python code/simplex_bias.py
# The figure is written to PortfolioSimplex/images/simplex_bias.png.

from pathlib import Path

import numpy as np
import qmcpy as qp
n, D = 512, 3
cube_points = qp.Sobol(dimension=D, seed=7).gen_samples(n)
normalized = cube_points / cube_points.sum(axis=1, keepdims=True)
w = qp.SimplexUniform.transform_points(cube_points[..., :D - 1], transform_method="root")
p = np.concatenate([w, 1 - w.sum(axis=-1, keepdims=True)], axis=-1)

# --- plotting ---
import matplotlib.pyplot as plt

simplex_boundary = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0]])
fig = plt.figure(figsize=(9, 4.2))
for col, (title, points, color) in enumerate([
    ("Sum-Normalized (Biased)", normalized, "crimson"),
    ("SimplexUniform Root (Uniform)", p, "seagreen"),
    ]):
    ax = fig.add_subplot(1, 2, col + 1, projection="3d")
    ax.scatter(*points.T, s=8, alpha=0.7, color=color, depthshade=False)
    ax.plot(*simplex_boundary.T, color="0.25", linewidth=1.2)
    ax.set(xlim=(0, 1), ylim=(0, 1), zlim=(0, 1))
    ax.set_title(title, fontweight="bold")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=24, azim=38)
    ax.set_xlabel("$p_1$"); ax.set_ylabel("$p_2$"); ax.set_zlabel("")
    ax.text2D(-0.08, 0.5, "$p_3$", transform=ax.transAxes, rotation=90, va="center", ha="center")
fig.tight_layout()
image_path = Path(__file__).resolve().parent.parent / "images" / "simplex_bias.png"
fig.savefig(image_path, dpi=170, bbox_inches="tight")
