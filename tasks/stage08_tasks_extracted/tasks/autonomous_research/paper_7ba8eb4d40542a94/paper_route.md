# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to test whether imidazole (ImA) and salicylic acid (SA) form stable hydrogen-bonded complexes and to identify the most strongly interacting configuration. The authors claim that three ImA–SA hydrogen-bond systems are stable and that one configuration has the most negative interaction energy (reported in the main paper as ΔE = −36.59 kJ/mol), supporting the proposed hydrogen-bond-system passivation concept.

## 2. System and model boundary

The molecular system is one neutral imidazole molecule and one neutral salicylic-acid molecule in the gas phase. The searched structures are intermolecular complexes involving the imidazole N–H donor and salicylic-acid oxygen acceptor sites (carboxyl and phenolic oxygen sites). The electronic-structure boundary is an isolated molecular complex and its isolated monomers; device-level perovskite, solvent, and solid-state effects are outside this calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and optimize candidate ImA–SA hydrogen-bond arrangements | ImA, SA, and trial intermolecular arrangements | Gaussian 16 | Full geometry optimization; B3LYP-D3BJ/6-31G(d) | Optimized complex geometries | ev_doc_a4de3f572d59_000196_f90288270a00; ev_doc_a4de3f572d59_000219_79bca4286920 |
| 2 | Confirm stationary-point character | Optimized complexes | Gaussian 16 | Harmonic vibrational frequencies at B3LYP-D3BJ/6-31G(d); no imaginary frequencies for minima | Validated local minima | ev_doc_a4de3f572d59_000196_f90288270a00 |
| 3 | Compare intermolecular interaction and electrostatic properties | Validated complexes and isolated monomers | Gaussian 16; VMD; Multiwfn | Binding/intermolecular energy; MESP and real-space analysis | ΔE values, MESP and derived descriptors | ev_doc_a4de3f572d59_000219_79bca4286920; ev_doc_a4de3f572d59_000227_98d399ba8fba |

## 4. Validation and analysis protocol

The authors considered a structure stable when optimization produced a stationary point with no imaginary vibrational frequencies. They compared the interaction energies of the stable configurations and used electrostatic-potential/interaction diagrams to interpret hydrogen bonding. The main text states that only three named configurations, ImA-SA-1, ImA-SA-2, and ImA-SA-3, were stable and identifies ImA-SA-3 as the most stable with ΔE = −36.59 kJ/mol. The paper also reports spectroscopic and thermal evidence consistent with ImA N–H/SA O hydrogen bonding, but those experiments are contextual rather than part of the quantum-chemical benchmark endpoint.

## 5. Private reference results

The source-backed reference set is: three stable ImA–SA hydrogen-bond configurations; the configuration called ImA-SA-3 is the most stable; its reported ΔE is −36.59 kJ/mol. The supplied SI text exposes the existence and title of Table S1 but not the complete numerical entries for ImA-SA-1 and ImA-SA-2, so those values are not used as hidden scoring targets.

## 6. Limitations and interpretation boundaries

The supplied evidence does not contain Cartesian coordinates for the named complexes, nor the full Table S1 numerical data. The author labels are therefore unsuitable as public structure identifiers. The calculation is a gas-phase model at one density-functional/basis-set level and does not establish solution, crystal, or perovskite-interface free energies. Geometry-search completeness is not demonstrated quantitatively in the paper; an autonomous benchmark must report its generated candidates, deduplication, validation, and coverage limitations.
