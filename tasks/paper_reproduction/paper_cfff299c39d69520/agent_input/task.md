# Scientific objective

Determine, by independent computation, the free-energy span for the stated Zn/proline-catalyzed coupling of R1 and R2 and test the authors' qualitative proposal of a redox-neutral Zn(II) catalytic route involving catalyst activation, nucleophilic alkyne activation, alkynyl-halide activation, product release, and catalyst regeneration. Report Gibbs energies or consistent relative free energies, the span definition, stationary-point identities, and the mechanistic/temperature interpretation.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`; IDs, connectivity, charge and multiplicity are explicit. The measured objects are optimized minima, transition states, frequencies, IRC/connectivity evidence, and Gibbs free energies at a declared temperature and standard-state convention. You may choose software, functional, basis, solvent treatment and conformer protocol, but disclose them. Do not use the paper, SI or general web.

# Required scientific validation/investigation

Independently generate a finite, deduplicated set of plausible catalyst/intermediate/TS states consistent with the disclosed qualitative route; retain an identity and provenance for every candidate. Optimize and characterize advanced states, using zero imaginary frequencies for minima and one for a TS or a clearly justified alternative. Validate the selected TS by IRC or another outcome-based connectivity test. Compute the cycle span from a stated reference and include sensitivity/limitations. Completion has two truthful outcomes: (i) a connected validated route with a span and conclusion, or (ii) a bounded-failure report identifying what could not be established, attempted candidates and missing validation. Submit the corresponding schema branch; do not invent energies, a route or a conclusion when validation fails. Stop when additional searches no longer produce distinct validated states under the declared generation protocol, and report coverage.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include methods, candidate records, validation evidence, energies, span, conclusion, coverage, and limitations.
