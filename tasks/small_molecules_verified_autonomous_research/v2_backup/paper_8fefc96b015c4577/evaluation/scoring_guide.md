# case_02 Private scoring guide

**Do not provide to ARCHE.** Paper: Unified Photoredox Strategy for Selective Access to Hydroisoquinoline and Benzosultam via Tether Modulation of Allylamine; DOI 10.1021/acs.orglett.5c04344.

Source location: Main text p4 Scheme 3c; SI p34–40. The main text and SI are located in 03_论文原文_仅供评测者/case_02/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|benzyl_barrier|35|Barrier for closure onto the benzyl-tethered aryl ring|
|sulfonyl_barrier|35|Barrier for closure onto the arenesulfonyl aryl ring|
|cyclization_conclusion|30|Final conclusion: cyclization on the benzyl side is more favorable|

Whole-case success requires all required scientific items to pass; the scientific score out of 100 only helps display partial completion. No process points are awarded.

## Item-by-item criteria

### r_benzyl_barrier

Identify the benzyl-tethered aryl closure by connectivity and forming-bond/negative-mode evidence, corresponding to source TS2. Compute G(TS)-G(uncyclized radical minimum), 298.15 K/1 atm, implicit DMSO, charge0 doublet. Validate the minimum and relevant first-order saddle; source -0.05 is on a different plot zero and is not this barrier.

Numerical target: 13.08 ± 1.5 kcal/mol.

### r_sulfonyl_barrier

Identify the arenesulfonyl aryl closure by connectivity and forming-bond/negative-mode evidence, corresponding to source TS2-prime. Use the same radical-reference definition and valid saddle evidence. Arbitrary candidate numbers or closest energies do not determine identity.

Numerical target: 19.25 ± 1.5 kcal/mol.

### r_cyclization_conclusion

The final answer selects the benzyl-tethered aryl closure as lower-barrier than the arenesulfonyl alternative using the two mapped, comparable calculated channels and their difference. A reversed ranking, undecided selection or mere listing of both does not recover the conclusion. No downstream oxidation/aromatization or catalyst cycle is required.

## Package changes and reference boundaries

The old starting XYZ is excluded from this package; the new initial guess was generated independently from SMILES using ETKDG and a general-purpose force field, without using the authors' TS/minimum coordinates.

Historical records may contain remote /inspire paths, which serve only as background indexes. Scoring for this package does not depend on accessing them; historical acceptance statuses must not be treated as results of the current ARCHE test.
