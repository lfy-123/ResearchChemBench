# Scientific objective

Independently plan and execute a computational test of the authors' qualitative conformer-population route for neutral singlet compound 1. For the three public structures named 1-1, 1-2 and 1-3, determine optimized-minimum status, gas-phase relative Gibbs free energy at 298.15 K, and Boltzmann population. The authors' qualitative route is conformer thermochemistry used to weight downstream ECD; do not assume their numerical outcome or software/model chemistry.

# Public inputs and scientific boundaries

The files `data/inputs/conformer_1-1.xyz`, `conformer_1-2.xyz`, and `conformer_1-3.xyz` are Cartesian coordinates in Å for the complete 54-atom neutral singlet structures of compound 1. Atom order is the order in each XYZ file; no atoms may be added, removed, remapped, protonated, or stereochemically inverted. The thermochemical boundary is isolated gas-phase compound 1 at T=298.15 K. The scored object is only this named three-conformer set; the other SI conformers are outside scope. You may generate computational models and reoptimize structures, but must state method, software, thermal treatment, and any frequency scaling or low-frequency treatment.

# Required scientific validation/investigation

For each named conformer, perform a defensible optimization/frequency workflow and establish whether the result is a true local minimum using the submitted frequency evidence or an explicitly justified alternative. Compute relative Gibbs energies using one common, stated thermochemical convention and derive populations with an explicit formula and temperature. Check population normalization over exactly the three public conformers and report omitted-ensemble implications. Completion requires all three named conformers attempted and each assigned success or scientifically justified bounded failure. Stop after this set is analyzed; do not search for additional conformers. Compare results to the independently obtained references only in your discussion, without assuming a target value during calculation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-conformer identity, optimization/minimum evidence, relative Gibbs energy in kcal/mol when available, population in percent when available, method provenance, normalization, the most-populated named conformer when all required values are available (otherwise `null`), and a conclusion about the bounded three-conformer result. Include honest failure records for any conformer that cannot be completed and limitations concerning the excluded SI conformers; failed records must not contain fabricated numeric values.
