# Scientific objective

Test the authors' qualitative proposal that methanol coordinates through a hydrogen bond to a carbonyl oxygen of Q(CH3)4 and independently compute the redox-dependent single-methanol hydrogen-bond enthalpy. Report ΔH1, ΔH2, ΔH_HB = ΔH2 − ΔH1, NAC1, NAC2, d1 and d2, with units and atom mapping. The author hypothesis is only that methyl sterics may favor an out-of-plane contact; no target structure or result is supplied.

# Public inputs and scientific boundaries

Use `data/inputs/q_ch3_4_neutral.smi`, `methanol.smi`, and `system_definition.json`. The SMILES files define neutral connectivity but do not encode coordinates or a preferred contact. Assign a stable atom map when generating the charged fragments and retain it in every complex and isolated-fragment calculation. Compute one-methanol complexes and isolated fragments in the charge/multiplicity states explicitly listed in `system_definition.json`, using an acetonitrile continuum at 298.15 K and 1 atm. You choose and justify the electronic-structure method, conformer generation, population analysis, and thermochemical convention. Do not use paper/SI/general web information.

# Required scientific validation/investigation

Generate a finite, deduplicated set of chemically plausible pair geometries for each state, retain candidate identities and atom mappings, and report optimization and frequency evidence for every advanced candidate rather than only a global validation statement. For a successful result, validate at least one reported pair per state as a minimum by frequency evidence, perform the same level of calculation for both isolated fragments and complexes, use a consistent enthalpy convention, and obtain NAC from a named population-analysis procedure. Report the contacted methanol H and quinone O mappings, OH···O distance, and a structure file reference or an unambiguous structural description for each selected candidate. Assess whether the submitted geometries support the disclosed steric/out-of-plane hypothesis, without treating that hypothesis as established in advance. Completion requires either a validated result for both states and the derived ΔH_HB, or a truthful bounded-failure report with per-state attempted candidates, diagnostics, coverage, unresolved requirements, and next step. Stop after all generated candidates are deduplicated and either one validated state-specific minimum per state is obtained or the documented search budget/technical limit is reached; report why stopping is scientifically defensible.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Select the `success` branch only when both state results are validated; otherwise use the `bounded_failure` branch and do not fabricate numerical placeholders. Include enough provenance to reproduce every submitted scientific result.
