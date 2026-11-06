# case_01 Private scoring guide

**Do not provide to ARCHE.** Paper: [3,3] and [5,5] Sigmatropic Shifts of Polycyclic Dibutadienylcyclopropanes: Computational Explorations of Concerted and Stepwise Mechanisms and “Negative Activation Energies”; DOI 10.1021/jacs.5c19476.

Source location: Main text p4 Fig.5, p14; SI p6. The main text and SI are located in 03_论文原文_仅供评测者/case_01/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|barrier_33|25|Activation free energy of the [3,3] channel|
|barrier_55|25|Activation free energy of the [5,5] channel|
|channel_structures|20|Correct molecular structures for the [3,3] and [5,5] channels|
|rearrangement_conclusion|30|Final conclusion: [3,3] has a lower barrier than [5,5]|

Whole-case success requires all required scientific items to pass; the scientific score out of 100 only helps display partial completion. No process points are awarded.

## Item-by-item criteria

### r_barrier_33

Recover the chemically assigned [3,3] channel Gibbs barrier relative to validated 3a at 298.15 K in the isolated-molecule boundary. Require a stationary saddle with exactly one relevant imaginary mode and displacement/connectivity validation; no source-coordinate copying or arbitrary candidate label.

Numerical target: 23.5 ± 3.0 kcal/mol.

### r_barrier_55

Recover the chemically assigned [5,5] channel Gibbs barrier relative to the same 3a reference at 298.15 K, with a valid first-order saddle and channel-specific displacement/connectivity evidence. Do not substitute barriers for other polycyclic substrates in this paper.

Numerical target: 26.2 ± 3.0 kcal/mol.

### r_channel_structures

Correctly construct distinct molecular structural models for both the [3,3] and [5,5] rearrangement channels of the supplied 3a. Require recoverable geometries and an unambiguous atom mapping that establish the channel-specific bond-breaking/forming pattern and connectivity, with the correct atom inventory and electronic state. Both channel assignments must be supported by actual computed structural evidence; names, file labels or two submitted jobs alone do not establish them. This item assesses structural identity separately from numerical barrier agreement: a correct channel model can pass even when its barrier misses tolerance. It does not replace the stationary-saddle and relevant-mode requirements of the two barrier items, and does not impose mandatory full IRC calculations.

### r_rearrangement_conclusion

The final comparison supported by the submitted two-channel computations identifies [3,3] as lower-barrier than [5,5] for 3a. Both numbers falling inside their independent ±3 windows does not by itself establish the correct ordering. Explain the comparison within the tested molecular mechanism; no negative-barrier result for another substrate is required.

## Package changes and reference boundaries

The input changes from specified, named [3,3]/[5,5] channels to unranked P1/P2 endpoints; the private reference structures map P1 to 3c of [5,5] and P2 to 3b of [3,3]. Targets and original tolerances are unchanged.

The old starting XYZ is excluded from this package; the new initial guess was generated independently from SMILES using ETKDG and a general-purpose force field, without using the authors' TS/minimum coordinates.

Historical records may contain remote /inspire paths, which serve only as background indexes. Scoring for this package does not depend on accessing them; historical acceptance statuses must not be treated as results of the current ARCHE test.
