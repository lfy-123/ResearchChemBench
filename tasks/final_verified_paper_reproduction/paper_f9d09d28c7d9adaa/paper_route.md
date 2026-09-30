# Private paper route — S1-core revision, 2026-09-23

The paper *Synthesis and structure-activity relationship study of highly distorted phenanthrimidazole molecules* (10.1016/j.molstruc.2025.145041) studies MeAC, TfAC, MeACFy and TfACFy. Its computational argument links ground-state distortion and orbital localization to the S1 LE/CT mixture and paired substitution effects.

## Author route and reference

1. Gaussian 09W B3LYP/6-31G(d,p) ground-state optimization; main pp.2–3 Fig.2 reports α1/α2/α3, β1 where present, and numerical HOMO/LUMO energies. These figure numbers are present even though no machine-readable author geometry is supplied.
2. Vertical TDDFT at the same stated level. SI p.6 Table S1 gives S1=3.0446/2.9162/3.0716/2.9552 eV in the compound order above; the brightest state is not necessarily S1.
3. Multiwfn NTO and IFCT on the selected excited states (main pp.3–4 Fig.3, SI pp.2–5 Fig.S1). The three IFCT groups are the phenanthrimidazole core, the short-axis substituted aryl, and acridine with its connecting phenyl bridge; fluorene belongs to the donor-side group where present. SI p.7 Table S2 gives S1 CT/LE=46.60/53.40, 58.94/41.06, 45.95/54.05, 56.42/43.58 percent.
4. Compare Me/CF3 and AC/ACFy pairs. The source associates CF3 with larger CT and Fy with larger LE. The latter differences are small (0.65 and 2.52 percentage points), so arbitrary directional hard gates are inappropriate without validated uncertainty.

## Geometry and orbital conventions

Source α3 values are 89.17/87.11/87.11/88.70 degrees, β1=87.11/88.02 degrees for the Fy pair. The public graph defines a bonded four-atom α3 and two complete aryl least-squares planes for β1, with normalized normals and acos(abs(dot)). The paper does not give a unique atom-selector/fitting algorithm; this reproducible convention is a benchmark operational definition, not a quotation of the author's algorithm. A nonbonded four-anchor torsion is not interchangeable with the plane angle.

HOMO is mainly acridine. Core/bridge LUMO localization applies primarily to the Me members; the source explicitly discusses redistribution toward the CF3 short-axis aryl in Tf members. The old all-four core/bridge statement and coefficient-square population proxy are superseded by compound-resolved, overlap-aware analysis. No quantitative short-axis metric or additional α1/α2 scoring requirement is introduced.

## Verification and scope boundary

The approved revision adds primary same-S1 TD/NTO/IFCT evidence to the previous ground-state scope. Four preserved ground-state minima and four new TD calculations support computational feasibility. Their S1 energies differ from the source by at most 0.0111 eV, and their three-fragment Mulliken-like IFCT CT values are 36.990/51.745/36.492/49.955 percent. These recover the two paired trends but differ from source CT by 6.465–9.610 percentage points. The author's complete geometry, partition settings and numerical implementation are not available; the cause of the quantitative offset is not established. Do not relabel those local numbers as author answers, expand a tolerance to fit them, or claim exact IFCT reproduction.

The task evaluates computed, traceable observables and their quantitative interpretation under its public definitions. Absolute-source agreement and robust trend support must be distinguished. The source reference is retained; narrow CT numerical grading needs a separate validated calibration. New scientific endpoints use the existing general semantic evaluation mechanism, without custom weights or paper-ID production code. Missing excited-state results remain incomplete. Earlier frozen ground-state runs keep their original contract and scores.

Triplet-level near-degeneracy, excited-state rates, RISC and device efficiency are outside the required S1 scope. The author considers them in its broader argument; the present subset does not certify that full mechanism.
