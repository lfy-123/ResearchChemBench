# Scientific objective

Determine and compare H–H activation free-energy barriers for neutral singlet silylenes 1 and V′ reacting with neutral singlet H2, using separated reactants as the reference for each system.

# Public inputs and scientific boundaries

Use `data/inputs/silylene_1_singlet.xyz` (55 atoms), `data/inputs/silylene_Vprime_singlet.xyz` (36 atoms), and `data/inputs/h2.xyz`. These are given reactant identities, not H2-activation TSs. All are neutral singlets. The primary physical boundary is implicit benzene, 298 K and 1 atm; apply the same stated method and Gibbs convention to both systems and separated H2. Barrier = G(TS) − G(silylene) − G(H2), in kcal/mol. Conformers and TS approaches are to be constructed by the agent; no author TS is supplied. No paper, SI, evaluator, historical verification archive or general-web lookup is an agent input.

# Required scientific validation/investigation

Optimize and characterize the reactants as minima. Locate H–H activation TSs, verify exactly one relevant imaginary mode, and establish reactant/product connection by IRC, constrained relaxation or a justified endpoint test. Use one main row for `system_id` = `1` and one for `V-prime`, in any order; record extra attempts separately. Report candidate evidence and comparable barriers, then determine the ordering from your results. No fixed two-round stopping rule is imposed.

# Deliverables

Submit `report/results.json`. Set overall status to `complete` only when both rows are `validated_success`; each requires a validated reactant, TS/connection evidence and numerical barrier. Otherwise use `bounded_failure`, with each failed row's reason and available diagnostics. Missing frequency or barrier values may be omitted/null as permitted by the schema; do not fabricate them.
