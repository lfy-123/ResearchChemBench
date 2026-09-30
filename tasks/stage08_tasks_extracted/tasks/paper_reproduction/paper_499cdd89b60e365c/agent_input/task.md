# Scientific objective

Determine, from first-principles thermodynamics, whether Ga incorporation into Cu is favored at a Cu(111) surface under methanol-synthesis conditions, and contrast that result with bulk Cu–Ga alloying. Establish the stable Ga coverage at 230 °C and H2O/H2 = 0.003 without relying on a published route or presumed answer.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that reduction of gallium oxide can make Ga incorporation into the near-surface region of Cu thermodynamically relevant under methanol-synthesis conditions, while bulk Cu–Ga alloying is less favored at that reaction point and is associated with more reducing, higher-temperature conditions.

**Candidate route or mechanism.**
Examine reduction of β-Ga2O3 by H2 coupled to replacement of top-layer Cu atoms by Ga in Cu(111), and compare the resulting surface-alloy family with composition-dependent bulk Cu–Ga alloy families. Treat the extent of surface substitution as the variable to resolve rather than assuming a particular winning arrangement.

**Discriminating evidence.**
Use relaxed first-principles energies for the references and candidate alloys in an oxide/H2/H2O-referenced chemical-potential balance, then compare the resulting surface and bulk free-energy stability across temperature and H2O/H2 ratio, including the supplied reaction point. Structural relaxation and convergence checks should support the energetic comparison.

# Public inputs and scientific boundaries

Use `data/inputs/cu111_base.cif` as a 2×2 Cu(111) four-layer slab, `cu_bulk.cif` as the Cu reference, `h2.xyz` and `h2o.xyz` as neutral singlet molecules, and `system_spec.json` for the reaction point, allowed top-layer substitutions, and β-Ga2O3 Materials Project record mp-1008844. Preserve atom identity and charge/multiplicity; only replace top-layer Cu by Ga. The physical boundary is Cu/Cu(111), Ga2O3, H2 and H2O. Measure thermodynamic stability/free-energy differences and stable coverage; do not infer catalytic rates or kinetics. Select and justify the computational method and candidate coverage space independently.

# Required scientific validation/investigation

Propose plausible surface and bulk alloy hypotheses, generate a finite candidate set with explicit identities, deduplicate equivalent structures, and retain per-candidate coordinates, composition, and validation status. Optimize references and candidates, audit force/energy convergence and atom counts, and construct an oxide/H2/H2O-referenced chemical-potential balance. Compare surface and bulk families at 503.15 K and H2O/H2=0.003. Completion requires a converged stable-coverage assignment plus bulk/surface comparison, or a bounded-failure report with the best-supported interval and missing evidence. In bounded failure, do not invent energies or stable coverage for unevaluated or non-converged candidates. Stop after the declared candidate space is covered or a documented numerical/resource limit; report coverage, alternate hypotheses considered, and limitations.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include independent method choices, candidate records, energies/free-energy differences with units, reaction-point stable coverage or interval, bulk comparison, validation evidence, conclusion, and limitations. Include enough coordinates or file references to reproduce every advanced candidate.
