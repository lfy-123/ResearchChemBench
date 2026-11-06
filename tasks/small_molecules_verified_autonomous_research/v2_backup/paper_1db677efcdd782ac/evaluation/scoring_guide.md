# case_05 Private scoring guide

**Do not provide to ARCHE.** Paper: A Biomimetic Study of the Behavior of N-Cyclopropyl-Based Single Electron Transfer Probes in the Context of Monoamine Oxidase-Catalyzed Oxidations; DOI 10.1021/acs.joc.5c02528.

Source location: Main text p7 Table 3/Fig.9; SI p49–51. The main text and SI are located in 03_论文原文_仅供评测者/case_05/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|h_ring_opening|12|Ring opening of the H-substituted system is unfavorable within the compared model|
|cis_me_ring_opening|12|cis-Me ring opening is favorable within a compatible reference model|
|trans_me_ring_opening|12|trans-Me ring opening is unfavorable within a compatible reference model|
|methyl_closed_trans_stability|14|The trans ring-closed state of the methyl system is lower in energy than the cis ring-closed state and the relevant ring-opened states|
|phenyl_open_preference|18|The Ph-substituted system favors ring opening in the tested branch|
|nonuniversal_ring_fate|18|Final conclusion: substituent and stereochemical effects rule out a universal assumption of fast irreversible ring opening|
|cis_trans_interconversion|14|Final conclusion: ring opening and the more stable trans ring-closed state explain cis→trans conversion|

Whole-case success requires all required scientific items to pass; the scientific score out of 100 only helps display partial completion. No process points are awarded.

## Item-by-item criteria

### r_h_ring_opening

With the correct S_H molecular framework, electronic state and ring-closed/ring-opened references, actual calculations support ring opening being energetically uphill relative to the ring-closed state. The authors' radical cation serves as the reference model; equivalent models supported by actual evidence for the same ring-fate proposition are accepted. A ring-closed structure alone or observation of a ring-retained product is insufficient. This item does not require all H B1/B2 conformers or exact agreement with 5.8 or 3.2 kcal/mol.

### r_cis_me_ring_opening

Preserve the correct relative stereochemistry of S_Mcis, and support energetically favorable ring opening through actual ring-closed/ring-opened comparisons. The authors' main M06-2X model serves as the reference; species, references and energy conventions must correspond. Near-zero values obtained with other functionals or thermal corrections must not be presented as the same target. Both the main-text −2.5 and SI −0.8 kcal/mol values for cis-Me B2 are retained; neither is a uniquely specified exact target. The fine ordering of B1/B2 is outside this item.

### r_trans_me_ring_opening

Preserve the correct relative stereochemistry of S_Mtrans, and support ring opening being energetically uphill relative to the ring-closed state through actual ring-closed/ring-opened comparisons. The authors' main M06-2X model serves as the reference; other functionals in the source can change the sign, so assessment must use compatible physical definitions. Do not construct an uphill result by mixing methods. This item does not infer an independent experimental product distribution starting from trans, and sets no exact window around 1.8 or 2.1 kcal/mol.

### r_methyl_closed_trans_stability

With the same composition, the same charge/spin and a common energy zero, actual calculations support the trans ring-closed state of the methyl system being more stable than the cis ring-closed state and the relevant ring-opened states compared. cis/trans must be identified by molecular relative stereochemistry, not filenames alone. A difference between local ring-opening energies cannot replace a comparison across isomers using a common reference; the authors' B1/B2 labels or enumeration of all conformers are not additional quotas.

### r_phenyl_open_preference

Preserve the S_Ptrans framework and relative stereochemistry. Actual structural/energy evidence must support a preference for ring opening in the tested branch, with no supported stable trap established in the ring-closing direction. The authors' profile showing increasing energy as the cleaved C–C bond is shortened, and optimization from a ring-closed structure to a ring-opened structure, serve as references; equivalent physical tests are allowed. A single ring-opened minimum is insufficient to establish this item. A finite profile does not establish the absence of ring-closed minima over the entire potential-energy surface, nor does it amount to a computed complete bimolecular dissociative electron-transfer trajectory.

### r_nonuniversal_ring_fate

The final answer integrates actual ring-reaction evidence for H, the methyl stereoisomers and Ph to show that ring-opening accessibility and ring-closed stability depend on substituents/stereochemistry; these N-cyclopropyl probes cannot universally be assumed to undergo fast irreversible ring opening upon oxidation. Within the compared models, cis-Me ring opening is more accessible than that of H and trans-Me, while the tested Ph branch favors ring opening more strongly. Actual comparisons supporting relative accessibility are required; reaction energies alone cannot serve as barriers. This conclusion does not require exact rates, fine B1/B2 ordering, or promotion of method-dependent source trends to a universal law.

### r_cis_trans_interconversion

The final answer connects actual evidence for methyl ring opening, the greater stability of the trans ring-closed state under a common reference, and the public observation that trans appears after starting from cis. Together, these support a compatible explanation in which ring opening can lead to the more stable trans ring-closed state; evidence-supported alternative routes establishing the same conversion relationship are allowed. The additional conclusion explains the observed isomerization; merely listing an energy ordering is insufficient. Do not describe this explanation as having established a separate isomerization barrier, rate or equilibrium ratio, and do not introduce a new target for the product distribution starting from trans.

## Package changes and reference boundaries

The scope is narrowed to ring fate after oxidation; oxidation-potential, aldehyde/isotope and full light-dependence items are removed. The 7 retained items are reweighted to a total of 100 points. No new ARCHE results were used to fit the scores.

The cis-Me B2 reaction energy of −2.5 in the main text conflicts with approximately −0.8 in the SI; this task assigns no numerical acceptance window to this scalar. Near-zero energy differences and ordering changes across methods are reviewed using compatible models.

Historical records may contain remote /inspire paths, which serve only as background indexes. Scoring for this package does not depend on accessing them; historical acceptance statuses must not be treated as results of the current ARCHE test.
