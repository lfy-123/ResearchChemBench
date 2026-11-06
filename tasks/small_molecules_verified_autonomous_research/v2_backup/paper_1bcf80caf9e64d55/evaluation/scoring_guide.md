# case_10 Private scoring guide

**Do not provide to ARCHE.** Paper: Phosphine-Catalyzed Alkyne-Ester Stitching for the Construction of Functionalized Cyclopentenones; DOI 10.1021/acs.orglett.5c04843.

Source locations: Main text p4–5 Scheme 4/5; SI from p97 onward. The main text and SI are located in 03_论文原文_仅供评测者/case_10/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|phosphine_addition|8|PEt3 addition and the zwitterion|
|initiation_energy|8|Free-energy height of initial addition|
|cyclization|8|Intramolecular cyclization|
|alkoxide_proton_transfer|8|Alkoxide departure and nucleophile generation|
|nucleophile_incorporation|8|Nucleophile incorporation into the product skeleton|
|phosphine_regeneration|8|PEt3 regeneration|
|product_structure|8|Complete cyclopentenone product|
|reaction_free_energy|8|Total free energy of the balanced products|
|initial_step_order|6|The initial step is the highest saddle point on the investigated profile|
|migration_competition|6|Comparison of direct cyclization and migration branches|
|route_conclusion|12|Final: select the direct-cyclization catalytic route|
|accessibility_conclusion|12|Final: kinetic and thermodynamic accessibility|

Whole-case success requires all required scientific items to pass; the 100-point scientific score only helps display partial completion. There are no process points.

## Item-by-item criteria

### r_phosphine_addition

Genuine connected calculations support nucleophilic addition of PEt3 to the alkyne β-C, forming zwitterionic intermediate 2 with a P–C bond. Verify that PEt3 is C6H15P; C7H17P is not equivalent. This item assesses bond and charge rearrangement independently of a numerical match for TS1.

### r_initiation_energy

Using initial complex 1 in Fig.S1 as zero, the target relative G of TS1 is 18.9 kcal/mol with an absolute tolerance of 1.0 kcal/mol; include all spectator material and maintain 383.15 K. Do not directly compare results using separated-reactant zeroes, isomeric phosphines or different chemical compositions.

Numerical target: 18.9 ± 1.0 kcal/mol.

### r_cyclization

Genuine connectivity and reaction modes of intermediate 2 support intramolecular attack on the ester carbonyl to construct five-membered-ring intermediate 3; preserve the complete side chain and atom mapping. The source common-reference heights of 8.2 for TS2 and 1.9 kcal/mol for 3 provide background only; do not treat 8.2 as a local activation energy.

### r_alkoxide_proton_transfer

Genuine connected calculations support alkoxide departure after cyclization and proton transfer involving 4-fluorophenol, producing a nucleophile capable of subsequent addition while conserving the ethanol equivalent and all atoms/charges. Associations of different fragments must be explicit; disconnected scalar nodes cannot substitute for chemical connectivity.

### r_nucleophile_incorporation

Computed TS4 and its connected endpoints support formation of the product's required C–O connectivity by the 4-fluorophenoxide nucleophile, preserving the five-membered ring and E-cinnamyl side chain. Source values of 2.8 for TS4 and −8.3 for 7 are background common-reference heights; no additional numerical threshold is imposed.

### r_phosphine_regeneration

Actual subsequent connectivity supports C–P cleavage and release of the correct neutral PEt3 as a recyclable catalyst; simply writing PEt3 on both sides of the reaction equation is insufficient. Maintain balanced spectator material such as ethanol. The source common-reference height of −0.9 for TS5 provides background only.

### r_product_structure

The actual endpoint graph is the observed aryloxycyclopentenone and retains the E-cinnamyl side chain, with atom origins traceable to the substrate/4-fluorophenol and ethanol coproduct. Do not substitute a simplified product that deletes the side chain or changes the phosphine; merely repeating the supplied product graph does not pass.

### r_reaction_free_energy

Using Fig.S1 complex 1 and matched spectator material as the initial reference, the balanced endpoint of product 9, PEt3 and ethanol has a target relative G of −24.7 kcal/mol with an absolute tolerance of 2.0 kcal/mol. Maintain 383.15 K and compatible solvent and standard state; do not use separated-reactant values or authors' energies to fill gaps in local calculations.

Numerical target: -24.7 ± 2.0 kcal/mol.

### r_initial_step_order

With the same complete material inventory and complex 1 as zero, actual comparison of the relevant saddle points along route A supports that initial phosphine addition is the highest and subsequent key saddle points are lower. A single TS1 number cannot establish the ordering of the entire profile; do not claim that concentration-dependent microkinetics have been established.

### r_migration_competition

Comparison from the common zwitterionic branch point with a consistent material reference provides actual competing-pathway evidence that the bottleneck of B's alcohol-assisted sequential 1,3-migrations lies higher than the cyclization route after branch A. Enumerating every B node is unnecessary; uncomputed later B states must not be described as independently established.

### r_route_conclusion

In the final conclusion, explicitly select route A, comprising PEt3-initiated zwitterion formation followed by direct cyclization, nucleophile incorporation and phosphine regeneration. Integrate actual connectivity, the complete observed product and migration-competition evidence to explain why this route is preferred. Merely listing candidate A does not earn credit; the conclusion is restricted to the investigated models and does not establish a globally unique mechanism.

### r_accessibility_conclusion

In the final conclusion, explain reaction accessibility using an actual complete free-energy profile and balanced endpoint: initial addition incurs the main energetic cost, and subsequent steps lead to an overall downhill product. Relate this to the 110°C conditions without treating 12 h or yield as an elementary rate constant. Passing the exact product-G window is not required, and a negative composite local difference cannot establish a negative physical barrier.

## Package changes and reference boundaries

The existing product free-energy residual is approximately −7.087. The rules primarily assess scientific propositions; no additional exact numerical thresholds were introduced. Stoichiometric balance, geometries and thermal corrections must be reviewed before quantitative comparison.

Historical records may contain remote /inspire paths, which are background indices only. Scoring in this package does not depend on access to them; historical acceptance status must not be treated as a result of this ARCHE evaluation.

**Additional numerical boundary:** This case retains the original 18.9±1.0 and −24.7±2.0 kcal/mol thresholds. The historical product deviation of approximately −7.087 exceeds the latter, so numerical passing of the whole case has not been certified; qualitative agreement must not be used to mark this item as passed.
