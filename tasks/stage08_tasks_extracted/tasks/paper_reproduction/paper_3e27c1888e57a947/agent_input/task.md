# Scientific objective

Independently test the authors' qualitative hypothesis that SO2 capture by the neutral doublet allylic radical Int2-a can occur at two sites, corresponding to 1,4 and 1,2 addition. Locate and validate the competing transition states and compute each relative Gibbs free-energy barrier from the common Int2-a + SO2 reference at 298.15 K in DMSO. Do not assume the paper's software, model chemistry, geometry, ordering, or result values.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the neutral doublet allylic radical Int2-a captures SO₂ preferentially at the terminal site (the 1,4 channel), while the internal 1,2 capture is a competing possibility. The proposed selectivity is a kinetic preference between the two site-specific addition pathways.

**Candidate route or mechanism.**
Search for SO₂ addition transition states from the common Int2-a + SO₂ reactant reference at both the terminal/1,4 site and the internal/1,2 site, preserving the atom mapping defined below. Treat each as a proposed concerted or otherwise directly connected capture event leading to its corresponding adduct, and compare the two site-specific pathways on the same free-energy convention.

**Discriminating evidence.**
Discriminate the pathways using optimized stationary-point structures, frequency classification with one capture-consistent imaginary mode for each TS, and IRC or an equivalent connectivity test linking each TS to Int2-a + SO₂ and its site-specific adduct. Use the authors’ qualitative comparison framework of gas-phase stationary-point/thermal analysis combined with solution-phase electronic energies in DMSO at 298.15 K, while choosing and documenting your own computational implementation.

# Public inputs and scientific boundaries

Use `data/inputs/int2a.xyz` as the complete Cartesian identity of Int2-a, with charge 0 and multiplicity 2. For answer-neutral site identity, use the atom numbering in that XYZ: the conjugated carbon framework is identified by its covalent connectivity, with the CF2H-bearing carbon (XYZ atom 1) as the substituted end; the internal site is framework carbon XYZ atom 8 and the terminal site is framework carbon XYZ atom 12. Thus “1,2” means SO2 capture at atom 8 and “1,4” means capture at atom 12; preserve this mapping in candidate and connectivity records. Add neutral singlet SO2 (`system.json`: one S bonded to two O atoms) as the reacting fragment; its orientation and separation are to be chosen computationally. The scored objects are the lowest defensible validated TS candidates you identify for terminal/1,4 SO2 capture and internal/1,2 SO2 capture from the same Int2-a + SO2 reference. Report relative Gibbs barriers in kcal/mol, stationary-point classification, and connectivity. The boundary is the isolated molecular system and 298.15 K; state clearly how solvent and thermal terms were treated. The public qualitative experimental boundary is that the 1,4 channel is observed and the 1,2 byproduct was not detected; it is not a numerical target.

# Required scientific validation/investigation

Generate a finite, chemically distinct set of candidate complexes/TS guesses for each site, document the generation and deduplication rule, and optimize or otherwise refine candidates with a method you justify. Advance a candidate only when it has converged, has the expected reactant/product bond-change pattern, and has a frequency analysis. A TS candidate must have exactly one imaginary frequency whose displacement is consistent with SO2 capture; validate both sides with IRC or a scientifically justified equivalent that identifies Int2-a + SO2 and the corresponding 1,4 or 1,2 adduct. Compute both barriers against the same reference convention and report units and formulas. Completion requires either two validated site-specific TSs with barriers and a comparison, or a bounded-failure report naming which site could not be validated, the candidates attempted, validation evidence, and the limitation. In bounded failure, use null for every unavailable barrier or TS path and do not infer an ordering requiring the missing site. Stop when both site searches have converged and been validated, or when additional distinct guesses no longer produce a new validated stationary point under your stated search-generation rule; report coverage and stopping reason.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus supporting calculation files or logs referenced by the JSON. Include candidate identities, structures or file paths, frequencies, connectivity evidence, reference-energy convention, barriers, ordering, and a concise scientific conclusion. If bounded failure occurs, use the failure branch and do not fabricate missing barriers.
