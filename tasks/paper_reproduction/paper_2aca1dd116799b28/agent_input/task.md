# Scientific objective

Determine whether the Bergman cycloaromatization electronic activation barriers of the three supplied, uniquely labeled triazolyl enediyne–amino-acid reactants EDY 15, EDY 16 and EDY 17 can be computed reproducibly, and whether the resulting relative barriers test the qualitative author hypothesis that donor/acceptor electronics and steric distortion affect transition-state stabilization. Compute electronic ΔE‡ = E(TS) − E(reactant) for each molecule in kcal/mol. The author hypothesis is qualitative only: independently test a catalyst-free, through-bond electronic-stabilization explanation against geometric distortion.

# Public inputs and scientific boundaries

Public files `data/inputs/edy_15.xyz`, `edy_16.xyz`, and `edy_17.xyz` are the SI-labeled optimized reactant geometries, with atom identities and Cartesian coordinates in Å. Each molecule is neutral, singlet, gas phase. EDY 15 is the D–D member, EDY 16 the D–A1 member, and EDY 17 the A1–A1 member; D means para-methoxyphenyl and A1 means para-cyanophenyl. The target reaction is intramolecular Bergman cycloaromatization, forming the new bond between the two terminal reactive carbons of the enediyne. Do not use paper/SI text or internet literature. TS, product, reference energies and expected ordering are not public. No universal software or model chemistry is prescribed.

# Required scientific validation/investigation

For each named molecule, generate and deduplicate a finite set of reactant conformers and TS guesses, document the selection rule, optimize the reactant and candidate TS, and retain a candidate only when the reactant has zero imaginary frequencies and the TS has exactly one imaginary frequency whose mode involves enediyne cyclization. Establish TS-to-product/reactant connectivity by IRC, constrained displacement, or another explicitly justified structural validation. Stop when each molecule has one validated lowest barrier among the explored candidates, or report bounded failure with all attempted candidates and the reason. Report search coverage and limitations; do not claim global uniqueness from an incomplete search.

# Deliverables

Submit `report/results.json` following the schema. Include status, per-molecule energies, validation evidence, method details, candidate coverage, barrier ordering if all three succeed, and a conclusion about the qualitative electronic/geometric explanation. A bounded-failure branch is valid only with attempted candidates, failure reasons and limitations. Completion means all three validated barriers or an honest bounded-failure report for any unresolved molecule.
