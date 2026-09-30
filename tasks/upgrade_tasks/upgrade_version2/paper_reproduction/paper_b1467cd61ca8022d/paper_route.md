# Version 2 route record (private metadata)

The source compares PM, BM, TFPM and TFBM in LiFSI electrolytes and proposes a molecular solvation rationale. The task selects their local molecular interactions, not full electrolyte transport, interphase formation or battery performance.

The authors propose dual RESPO/dipole descriptors and synergistic O/F lithium coordination, favoring a six-membered TFPM chelate. Source calculations use Gaussian16 B3LYP/6-311+G(d,p), geometry/frequency checks, and Eb=Ecomplex−ELi+−Esolvent; Multiwfn3.8 is named for RESP. The source RESPO axis is labeled eV, whereas RESP atomic charges are in e; reproduce the actual defined quantity or explicitly flag this ambiguity instead of treating them as interchangeable. Their separate GROMACS2018 OPLS-AA bulk simulations use30 LiFSI with145 PM/125 BM/129 TFPM/110 TFBM,8 ns NVT and40 ns NPT with final30 ns analysis. The molecular task does not require that MD protocol or the builder’s former1:1:1 FSI cluster grid. Reproduce the relevant disclosed molecular baseline or justify substitutions; any new local model is an additional investigation. Published computed chelation and populations are author interpretations/results, not required answers.

No route in this record is an undisclosed AR scoring requirement. PR guidance is in its own public task.
