# case_14 Private scoring guide

**Do not provide to ARCHE.** Paper: Synthesis and characterization of N-propargyl-3-nitropyrrole derivatives: in silico molecular docking studies, and cytotoxic activities in lung cancer; DOI 10.1016/j.molstruc.2025.144925.

Source location: Main text p2 Fig.1; SI DOCX Theoretical study/Table 1. The original paper and SI are located in 03_论文原文_仅供评测者/case_14/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|base_hydrogen_transfer|15|Base-induced N–H transfer and H2 formation|
|activated_n_intermediate|15|The deprotonated nitrogen-containing intermediate connects to the subsequent reaction|
|n_c_bond_formation|20|Substitution event involving N–C formation and C–Br cleavage|
|net_exergonicity|10|Balanced net product formation has an exergonic trend|
|connected_route_answer|20|Final: a two-step molecular explanation of the complete N-propargylation|
|energetic_answer|20|Final: distinguish local substitution difficulty from overall exergonicity|

Whole-case success requires all mandatory scientific items to pass; the 100-point scientific score only helps display partial completion. No process points are awarded.

## Item-by-item criteria

### r_base_hydrogen_transfer

Actual structures and reaction-connectivity evidence support base-induced removal of the N–H hydrogen of 3-nitropyrrole and formation of H2, preserving the β-nitropyrrole identity and balancing atoms/charges. The authors' hydride-contact model TS1 is a reference; chemically equivalent representations are allowed, and source coordinates or a fixed search method are not mandatory. Merely writing a deprotonation label or providing an unvalidated TS earns no credit.

### r_activated_n_intermediate

Valid calculations support the deprotonated nitrogen-containing pyrrole state and its corresponding stabilization, maintaining a mapping of the same anionic skeleton to the precursor for subsequent propargylation. The authors' S2/H2 contact state at approximately −25.5 kcal/mol relative to the initial state is context; the same contact partner/conformation is not mandatory. An actual intermediate state and connectivity relationships must be obtained; two mutually unbalanced models cannot be spliced together.

### r_n_c_bond_formation

Actual reaction structures, vibrational modes and appropriate connectivity evidence support bond formation between pyrrole N and the propargylic carbon and C–Br cleavage, retaining the terminal alkyne and β-nitro position. The SN2 channel of the authors' TS2 is a reference. Author labels or a full IRC are not mandatory, but merely calculating a nonreactive imaginary frequency or a product with incorrect substitution positions earns no credit.

### r_net_exergonicity

Compatible energy definitions and complete material/charge accounting yield a calculated substantially exergonic trend for net formation of the N-propargyl product. The authors' G of approximately −45.5 kcal/mol is reference context, with no hidden exact window. Do not omit H2/reagents/Br or derive ΔG directly from the yield.

### r_connected_route_answer

Finally, use a computationally supported connected explanation to link the roles of the substrate, base and alkylating reagent through to the correct N-propargyl product. The authors' deprotonation followed by substitution is a reference; equivalent routes supported by actual evidence are acceptable. Merely showing isolated TSs/products or proposing an untested reaction type is insufficient.

### r_energetic_answer

Using the connected pathway and comparable energies, explicitly establish that subsequent N–C substitution has a more pronounced local activation requirement than the preceding near-reactant deprotonation, while the net conversion is exergonic. Correctly distinguish relative profile heights, local barriers from the respective precursors and the reaction ΔG; the authors' 16.2 is only an energy difference under their reference definition. Do not describe a negative relative TS G as an experimentally strictly barrierless reaction, or infer a quantitative rate from 89%/24h.

## Package changes and reference boundaries

The simplified source TS does not contain Na; effects of the full solid NaH/ion-pair system have not been established. A negative plotted relative TS height does not imply a zero local barrier.

Historical records may contain remote /inspire paths, which serve only as background indexes. Scoring in this package does not depend on accessing them; historical acceptance statuses must not be treated as results of this ARCHE evaluation.
