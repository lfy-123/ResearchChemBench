# case_08 Private scoring guide

**Do not provide to ARCHE.** Paper: Lewis acid catalyzed enantioselective dearomative (3+2) cycloaddition of aromatic N-heterocycles with bicyclobutanes; DOI 10.1016/j.cclet.2025.111963.

Source locations: Main text p3 Table 1, p5–6 Scheme 6; SI p126–130. The main text and SI are located in 03_论文原文_仅供评测者/case_08/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|ni_substrate_binding|8|The specified Ni–chiral-ligand system forms a reaction-relevant binding structure with acylimidazole BCB|
|ni_ring_opening|10|Benzothiazole N bonds to a BCB bridgehead while the bridgehead C–C bond opens|
|ni_r_closure|8|Established dearomative C–C ring-closure connection leading to the R product|
|ni_s_closure|8|Established competing dearomative C–C ring-closure connection leading to the S product|
|ni_r_competition|9|A common-reference comparison supports a more favorable R-forming channel|
|ni_selectivity_features|12|Direct computational evidence for different physical environments in R/S-forming structures|
|ni_formation_answer|15|Final: a connected catalytic formation explanation accounts for the supplied cycloaddition product|
|ni_mapped_r_answer|10|Final: explicitly predict R as the major enantiomer at the supplied saturated CH|
|ni_origin_answer|10|Final: a bounded physical explanation connects environmental differences to R preference|
|ni_strength_answer|10|Final: a bounded comparison of computationally supported selectivity strength with the experimental 92.5:7.5 ratio|

Whole-case success requires all required scientific items to pass; the 100-point scientific score only helps display partial completion. There are no process points.

## Item-by-item criteria

### r_ni_substrate_binding

Actual structural or electronic evidence supports binding of the specified Ni(OTf)2/(S,S)-tert-butyl PyBOX system to the acylimidazole site of the supplied BCB, establishing substrate positioning or an activation environment relevant to subsequent transformation. The authors' O,N-bidentate IM5 with one inner-sphere OTf is a reference; equivalent binding models supported by evidence are permitted. Ranking IM5A/B/C, matching a binding energy or determining complete solution speciation is not required. Merely constructing the correct identities, an isolated catalyst or repeating a Lewis-acid label is insufficient.

### r_ni_ring_opening

Actual connectivity evidence supports formation of a C–N bond between benzothiazole N and the originally phenyl-substituted BCB bridgehead while the original BCB bridgehead C–C bond opens, yielding an open-ring skeleton capable of proceeding to the supplied product. The authors' IM5+1a to IM6 is a reference; preserve the correct atom inventory and atom mapping. The authors did not supply this chiral ring-opening TS; providing this TS, a full IRC or using the ambiguous SI +2.3 value as a local energy target is not required. Equivalent routes supporting the same net connectivity event are acceptable.

### r_ni_r_closure

Actual calculations support C–C bond formation between the acyl-substituted BCB bridgehead and the carbon derived from benzothiazole C2, connecting to the R-related branch of the supplied product skeleton. Enantiomer labels must correspond to the saturated CH specified in PI4. The authors' TS3R/IM7R is a reference; TS claims require relevant single-imaginary-frequency motion and evidence for the claimed chemical connections on both sides. Scientifically equivalent connectivity checks are permitted; a full IRC or reproduction of −242.04 cm−1 is not mandatory. Names or the final product graph alone cannot establish this result.

### r_ni_s_closure

Actual calculations support the same net C–C ring-closure event along the competing branch leading to S at the saturated CH specified in PI4, with product connectivity, composition and the catalyst model comparable to the R branch. The authors' TS3S/IM7S is a reference; TS claims require relevant single-imaginary-frequency motion and evidence for the claimed chemical connections on both sides. Scientifically equivalent connectivity checks are permitted; a full IRC or reproduction of −200.59 cm−1 is not mandatory. Merely relabeling R as S or optimizing a product without connectivity evidence cannot establish this result.

### r_ni_r_competition

With correct reactants, ligand stereochemistry, compatible composition/charge/spin and a common reactant reference, actual energies or other valid competition evidence support more favorable R formation than S formation. The authors' C–C ring-closure TS3R lying approximately 2.2 kcal/mol below TS3S is a reference, with no numerical window. Product stability, absolute energies of incomparable models or the supplied er cannot directly substitute for formation competition. This item assesses the direction of competition and does not replace the final selection of the product's absolute configuration.

### r_ni_selectivity_features

For comparable R/S-forming structures, actual structural, density or energy analyses reveal ligand–substrate environmental differences capable of explaining the competition difference. The authors' local C–H···π weak-contact observations provide a reference: some R-side contact features are enhanced, consistent with R preference. Every contact need not trend in the same direction; greater total attraction for R, exact red-circle counts or a specified IGMH metric are not required. Evidence-supported interaction, deformation or other physical analyses with compatible scope are acceptable. Energy ordering alone or an unpaired contact plot is insufficient.

### r_ni_formation_answer

In the final conclusion, explicitly adopt a connected chemical explanation from the starting materials to the supplied product supported by actual calculations, and explain how the specified Ni–chiral-ligand system participates in substrate binding and bond formation. Connect the required C–N formation/BCB ring opening and dearomative C–C closure to product connectivity. The authors' stepwise nucleophilic route is a reference; equivalent routes supporting the same net transformation are acceptable. Isolated stationary points, one energy or repetition of product observations are insufficient. A complete catalytic cycle, chiral ring-opening barrier, yield or global rate prediction is not required.

### r_ni_mapped_r_answer

In the final conclusion, explicitly select R as the major enantiomer at the saturated CH derived from benzothiazole C2 in PI4, and connect the actually more favorable formation branch to this product absolute configuration through atom correspondence. Do not substitute the ligand's S configuration, arbitrary atom numbering, a statement only that the R channel is lower or a list of two candidates for a product configurational assignment. Source atom numbering differs between IM6 and TS/IM7 and need not be replicated. This item adds final selection and mapping of the reaction branch to the experimental product.

### r_ni_origin_answer

In the final conclusion, use actual R/S environmental differences and competition evidence to explain the physical origin of R preference. A local weak-contact explanation compatible with the authors' account or an equivalent explanation supported by actual evidence is acceptable. Explain why the physical difference used is consistent with the energetic preference; local density descriptors cannot directly establish additive stabilization energies, enhanced total attraction or a unique/quantitatively dominant cause. If using the current source analysis, preserve the limitations that the attractive subdomain favors S and that contact trends are mixed. The evaluated Agent need not reproduce the validator's integrations, decompositions or analysis workflow.

### r_ni_strength_answer

In the final conclusion, relate the R preference and its strength supported by actual competition evidence to the supplied experimental ratio of 92.5:7.5, explaining the computed direction/degree of enrichment and the model's limits on inferring its magnitude. A consistently defined ratio estimate or an evidence-supported qualitative comparison of strength is acceptable; exact er, a specified energy gap or an additional kinetic network is not required. If quantitatively converting a single TS pair, use a compatible temperature, energy/rate relationship and prefactor assumptions, and do not misrepresent a conditional prediction as an experimental measurement or exact reproduction. Repeating the supplied ratio or making a generic uncertainty statement alone is insufficient.

## Package changes and reference boundaries

Do not borrow achiral Ni(ClO4)2/DCM energies for the chiral Ni(OTf)2/CHCl3 system. IM6 +2.3 is a plotted height; its increment relative to IM5 −4.7 is +7.0. The +1/triplet model is a reference reconstruction, not a known input fact.

Historical records may contain remote /inspire paths, which are background indices only. Scoring in this package does not depend on access to them; historical acceptance status must not be treated as a result of this ARCHE evaluation.
