# case_11 Private scoring guide

**Do not provide to ARCHE.** Paper: Effect of Unique NNS Ligand in Manganese-Catalyzed Transfer Hydrogenation Reaction—A DFT Mechanistic Study; DOI 10.1002/cctc.202501586.

Source location: Main text p3–9 Fig.1–8; energy/coordinate tables in the SI DOCX. The original paper and SI are located in 03_论文原文_仅供评测者/case_11/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|active_nn|5|Actual coordination structure of the NN tricarbonyl candidate|
|active_nns|5|Actual coordination structure of the NNS dicarbonyl candidate|
|oxidation_connection|10|Hydrogen-transfer connectivity for isopropanol oxidation|
|reduction_connection|10|Hydrogen-transfer connectivity for acetophenone reduction|
|rest_Mn1_Me|3|Resting-state stabilization of Mn1-Me|
|rest_Mn1_tBu|2|Resting-state stabilization of Mn1-tBu|
|rest_Mn2_Me|3|Resting-state stabilization of Mn2-Me|
|rest_Mn2_tBu|2|Resting-state stabilization of Mn2-tBu|
|oxidation_order_Me|8|NN/NNS oxidation comparison with Me substitution|
|oxidation_order_tBu|7|NN/NNS oxidation comparison with tBu substitution|
|reduction_order_Me|5|S-channel NN/NNS reduction comparison with Me substitution|
|reduction_order_tBu|5|S-channel NN/NNS reduction comparison with tBu substitution|
|stereo_Mn1_Me|3|S/R preference for a fixed configuration of Mn1-Me|
|stereo_Mn1_tBu|3|S/R preference for a fixed configuration of Mn1-tBu|
|stereo_Mn2_Me|2|S/R preference for a fixed configuration of Mn2-Me|
|stereo_Mn2_tBu|2|S/R preference for a fixed configuration of Mn2-tBu|
|cycle_hydrogen_ledger|5|Organic transformation closed by the two half-reactions|
|activity_conclusion|10|Final: opposite effects of the coordination environment on the two half-reactions|
|stereo_conclusion|10|Final: configuration-dependent preference and its ensemble implications|

Whole-case success requires all mandatory scientific items to pass; the 100-point scientific score only helps display partial completion. No process points are awarded.

## Item-by-item criteria

### r_active_nn

Actual calculated structures support a complete neutral amido-type NN-Mn(I)(CO)3 candidate with an unbound sulfur arm, retaining the given ligand connectivity and CO inventory; state and support the electronic state used. Drawings or proposed hypotheses alone do not earn credit. Proof of actual solution populations or precursor-activation barriers is not required. Equivalent candidate mappings supported by evidence are acceptable.

### r_active_nns

Actual calculated structures support a complete neutral amido-type NNS-Mn(I)(CO)2 candidate with sulfur coordinated. Preserve the complete ligand identity shared with the NN tricarbonyl and explicitly account for CO loss and the electronic state. Candidate labels alone do not earn credit. Actual populations or additional precursor-activation calculations are not required.

### r_oxidation_connection

Actual stationary points and relevant vibrations/reaction connectivity support transfer of the isopropanol O–H and C–H hydrogens to form acetone and the corresponding amine-hydride; balance protons, hydrides, atoms and charges. Actual connections between reaction states are required and cannot be replaced by successful task execution or an arbitrary negative frequency. Replication of the verifier's IRC steps is not required, and no absolute-barrier window is imposed where sources conflict.

### r_reduction_connection

Actual stationary points and relevant vibrations/reaction connectivity support transfer from the matching amine-hydride to acetophenone of the Mn–H hydride to carbon and the N–H proton to oxygen, forming the correct 1-phenylethanol. Structures/atom mappings support the claimed product face. Distinguish this from the oxidation half-reaction; the oxidation barrier cannot substitute for it. No absolute-barrier window is imposed where sources conflict.

### r_rest_Mn1_Me

For Mn1-Me (Mn1 is the NN tricarbonyl and Mn2 is the NNS dicarbonyl), actual free energies support the N-protonated Mn isopropoxide resting state lying below the matching amido+iPrOH. Consequently, the effective barrier of the same oxidation TS relative to this resting state is higher than its ordinate relative to the separated reactants. Use the same TS, balanced particles/charges and consistent thermal terms. Evaluate the sign of stabilization and the change in reference zero independently; matching numerical values that conflict between sources is not required.

### r_rest_Mn1_tBu

For Mn1-tBu (Mn1 is the NN tricarbonyl and Mn2 is the NNS dicarbonyl), actual free energies support the N-protonated Mn isopropoxide resting state lying below the matching amido+iPrOH. Consequently, the effective barrier of the same oxidation TS relative to this resting state is higher than its ordinate relative to the separated reactants. Use the same TS, balanced particles/charges and consistent thermal terms. Evaluate the sign of stabilization and the change in reference zero independently; matching numerical values that conflict between sources is not required.

### r_rest_Mn2_Me

For Mn2-Me (Mn1 is the NN tricarbonyl and Mn2 is the NNS dicarbonyl), actual free energies support the N-protonated Mn isopropoxide resting state lying below the matching amido+iPrOH. Consequently, the effective barrier of the same oxidation TS relative to this resting state is higher than its ordinate relative to the separated reactants. Use the same TS, balanced particles/charges and consistent thermal terms. Evaluate the sign of stabilization and the change in reference zero independently; matching numerical values that conflict between sources is not required.

### r_rest_Mn2_tBu

For Mn2-tBu (Mn1 is the NN tricarbonyl and Mn2 is the NNS dicarbonyl), actual free energies support the N-protonated Mn isopropoxide resting state lying below the matching amido+iPrOH. Consequently, the effective barrier of the same oxidation TS relative to this resting state is higher than its ordinate relative to the separated reactants. Use the same TS, balanced particles/charges and consistent thermal terms. Evaluate the sign of stabilization and the change in reference zero independently; matching numerical values that conflict between sources is not required.

### r_oxidation_order_Me

With the same Me substituent, isopropanol medium, 298.15 K and consistent 1 atm conditions or transparent conversions, actual calculations using matching amido+iPrOH references support a lower oxidation barrier for the NN tricarbonyl than for the NNS dicarbonyl. Assess the family ordering; the internal Me/tBu ordering or matching absolute barriers is not required. Incompatible reference zeros must not be compared.

### r_oxidation_order_tBu

With the same tBu substituent, isopropanol medium, 298.15 K and consistent 1 atm conditions or transparent conversions, actual calculations using matching amido+iPrOH references support a lower oxidation barrier for the NN tricarbonyl than for the NNS dicarbonyl. Assess the family ordering; the internal Me/tBu ordering or matching absolute barriers is not required. Incompatible reference zeros must not be compared.

### r_reduction_order_Me

With matching Me substituents, the same substrate face and mapped catalyst configurations, actual calculations support a lower S-channel reduction barrier for the NNS dicarbonyl than for the NN tricarbonyl. Use the corresponding amine-hydride+acetophenone reference for each and maintain the same thermodynamic conditions. The cross-family R-channel ordering or numerical windows are not required where sources conflict.

### r_reduction_order_tBu

With matching tBu substituents, the same substrate face and mapped catalyst configurations, actual calculations support a lower S-channel reduction barrier for the NNS dicarbonyl than for the NN tricarbonyl. Use the corresponding amine-hydride+acetophenone reference for each and maintain the same thermodynamic conditions. The cross-family R-channel ordering or numerical windows are not required where sources conflict.

### r_stereo_Mn1_Me

For the same chiral catalyst configuration, composition and thermodynamic conditions of Mn1-Me, paired actual calculations support the S-face reduction TS lying below the R-face TS when mapped to the authors' configuration. A mirror-image catalyst must reverse the product-face mapping accordingly; an unmapped configuration or reversed direction does not pass. This qualitative difference does not require matching conflicting ΔΔG values in the main text or SI and does not represent macroscopic ee.

### r_stereo_Mn1_tBu

For the same chiral catalyst configuration, composition and thermodynamic conditions of Mn1-tBu, paired actual calculations support the S-face reduction TS lying below the R-face TS when mapped to the authors' configuration. A mirror-image catalyst must reverse the product-face mapping accordingly; an unmapped configuration or reversed direction does not pass. This qualitative difference does not require matching conflicting ΔΔG values in the main text or SI and does not represent macroscopic ee.

### r_stereo_Mn2_Me

For the same chiral catalyst configuration, composition and thermodynamic conditions of Mn2-Me, paired actual calculations support the S-face reduction TS lying below the R-face TS when mapped to the authors' configuration. A mirror-image catalyst must reverse the product-face mapping accordingly; an unmapped configuration or reversed direction does not pass. This qualitative difference does not require matching conflicting ΔΔG values in the main text or SI and does not represent macroscopic ee.

### r_stereo_Mn2_tBu

For the same chiral catalyst configuration, composition and thermodynamic conditions of Mn2-tBu, paired actual calculations support the S-face reduction TS lying below the R-face TS when mapped to the authors' configuration. A mirror-image catalyst must reverse the product-face mapping accordingly; an unmapped configuration or reversed direction does not pass. This qualitative difference does not require matching conflicting ΔΔG values in the main text or SI and does not represent macroscopic ee.

### r_cycle_hydrogen_ledger

Actual oxidation and reduction states jointly support the net reaction acetophenone+iPrOH→1-phenylethanol+acetone and close hydrogen, atom and charge accounting through compatible amido/amine-hydride states. The additional scientific information assessed here is that the two local processes can form the same transfer-hydrogenation cycle. Merely listing two unrelated routes or diagrams does not pass; a complete equilibrium of actual solution species is not required.

### r_activity_conclusion

Finally, integrate actual reaction-state, family-comparison and resting-state results to explain that the NN tricarbonyl favors alcohol oxidation, whereas the NNS dicarbonyl can favor ketone reduction through the S channel. Comparison of effective oxidation barriers supports alcohol oxidation as the slower half-cycle within these candidate models. Make an explicit computationally supported choice/explanation; merely listing candidates or trends is insufficient. Do not infer a uniquely true active species, actual populations or precise rates.

### r_stereo_conclusion

Finally, infer from actual paired structures/energies and mirror-image relationships that a fixed catalyst configuration can produce an S/R difference and that its mirror image corresponds to the opposite product mapping. Results for a single configuration with achiral ligands cannot establish experimental macroscopic ee. Support this ensemble interpretation with actual mappings and comparisons; a generic statement that there are limitations is insufficient. Additional determination of actual configuration populations or the complete mirror-image reaction network is not required.

## Package changes and reference boundaries

Some thermal terms and local orderings conflict between the main text and SI; use bounded family comparisons without adding numerical windows. An S/R preference for a fixed catalyst configuration is not the net ee of an achiral system.

Historical records may contain remote /inspire paths, which serve only as background indexes. Scoring in this package does not depend on accessing them; historical acceptance statuses must not be treated as results of this ARCHE evaluation.
