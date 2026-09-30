# Private paper route

## 1. Scientific objective and author claim

The paper uses first-principles work functions of anatase TiO2(101) and rutile TiO2(110) to test whether the two TiO2 phases can support a built-in field and a Z-scheme hetero-phase homojunction in TiO2 nanotube-array photoanodes. The authors claim electron transfer from anatase toward rutile because the phase work functions differ.

## 2. System and model boundary

The calculated objects are clean periodic TiO2 slabs exposing anatase (101) or rutile (110). The SI identifies TiO2 stoichiometry, the two facets, fully relaxed lattice structures, and a vacuum-slab work-function calculation. The experimental catalyst is an anatase/rutile TiO2 nanotube array; the DFT calculation is a facet-level model rather than an atomically explicit nanotube junction.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define phase surfaces | Anatase (101) and rutile (110) TiO2 crystal faces | VASP periodic DFT | Fully relaxed lattice structure | Surface slab models | ev_doc_31bc16078a2e_000005_1b945275651f |
| 2 | Relax ionic geometry | Each surface model | VASP geometry optimization | PBE GGA; plane-wave cutoff 400 eV; EDIFFG = -0.03 eV/Å | Relaxed slabs | ev_doc_31bc16078a2e_000005_1b945275651f |
| 3 | Obtain surface vacuum level and Fermi level | Relaxed anatase and rutile slabs | VASP static first-principles calculation | Work-function calculation; remaining settings are not reported in the supplied SI | Work functions for both facets | ev_doc_31bc16078a2e_000005_1b945275651f |
| 4 | Interpret phase charge transfer | Two computed work functions plus experimental context | Comparison in the paper | Lower-work-function phase donates toward higher-work-function phase | Built-in-field/Z-scheme interpretation | ev_doc_04cc9a003baa_000146_45f1fa8e68fe |

## 4. Validation and analysis protocol

The authors report the two facet work functions in the discussion of Fig. 5 and use their difference to infer electron transfer and a built-in electric field. The interpretation is combined with XPS evidence of no significant Ti 2p/O 1s shift and the paper's band-structure discussion. The paper also reports that holes dominate pollutant oxidation and that superoxide formation is especially associated with the mixed-phase sample, but those experiments are contextual rather than part of the slab calculation.

## 5. Private reference results

The paper reports 6.871 eV for anatase (101) and 7.009 eV for rutile (110), implying anatase-to-rutile electron transfer and a 0.138 eV work-function difference. These values are hidden from agents and are used only for evaluation.

## 6. Limitations and interpretation boundaries

The supplied SI does not specify slab layer count, termination, vacuum width, dipole correction, k-point mesh, smearing, pseudopotential variant, or other VASP tags. The released task therefore fixes a target-independent slab recipe and permits scientifically justified equivalent settings, while requiring complete reporting and convergence evidence. Agreement with the paper values is a benchmark comparison, not proof that a real nanotube interface has the same microscopic charge distribution.
