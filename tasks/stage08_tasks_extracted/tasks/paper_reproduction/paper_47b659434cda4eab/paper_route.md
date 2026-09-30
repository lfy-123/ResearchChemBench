# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to explain why fatty-acid chain length changes the olefin distribution in electrochemical decarboxylation.  The authors claim that the initially formed alpha carbocation can either lose H to form a terminal olefin, rearrange to a more stable carbocation and undergo OH-assisted quenching/dehydrogenation, or (for still longer chains) undergo beta–gamma C–C scission.  This mechanism is used to rationalize the lower performance of short-chain substrates and the higher terminal-olefin fraction for longer chains.

## 2. System and model boundary

The computational objects are linear hydrocarbon carbocations representing alpha and beta carbocations formed after fatty-acid decarboxylation, with carbon lengths illustrated by C10, C15 and C17.  Models without OH are cationic doublets; models containing OH are neutral singlets.  The paper's mechanistic comparison concerns dehydrogenation to olefin and, for the rearranged species, competition with OH quenching.  This task uses explicit linear-chain constitutional models as a reproducible public proxy for the named model class; it does not claim to reproduce omitted optimized coordinates.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build initial alpha/beta carbocation models from reaction characteristics | Linear-chain carbocation models; charge 1, multiplicity doublet without OH | Gaussian 09 / GaussView 5.08 | Initial models estimated from reaction characteristics | Starting geometries | ev_doc_d10988fd3618_000133_80e7106db0a0; ev_doc_d10988fd3618_000328_3bdfef950474 |
| 2 | Locate transition states for dehydrogenation and OH-assisted alternatives | Starting geometries | B3LYP DFT, Gaussian 09 Berny TS optimization | 6-31G(+)**; opt=(calcfc,ts,noeigen); one force-constant calculation | TS geometry, frequency and energy | ev_doc_d10988fd3618_000328_3bdfef950474 |
| 3 | Verify the reaction connection | Optimized TS | IRC in both directions at the same level | Forward and reverse IRC; one force-constant calculation | Connectivity-validated TS/path | ev_doc_d10988fd3618_000328_3bdfef950474 |
| 4 | Compare chain-length-dependent pathways | Validated paths and energies | Relative barrier comparison | Alpha/beta, C10/C15/C17 examples; OH and no-OH alternatives | Mechanistic interpretation | ev_doc_d10988fd3618_000133_80e7106db0a0; ev_doc_d10988fd3618_000337_b48fbf750ac3; ev_doc_d10988fd3618_000495_92ae5e7144dc |

## 4. Validation and analysis protocol

The authors require a transition-state frequency check and IRC in both directions.  They interpret a failed alpha-cation optimization as evidence that the alpha structure is not a stable minimum, and compare the surviving pathways by barrier and product connectivity.  The paper reports the qualitative pattern: the short-chain alpha cation is not stabilized; the corresponding beta cation favors OH quenching over high-barrier dehydrogenation; C15/C17 alpha cations support low-barrier dehydrogenation without OH assistance; and still longer chains can show beta–gamma scission.

## 5. Private reference results

The hidden reference is qualitative because the supplied snapshot does not include the Figure S31 numerical source data or Supplementary Data 1 coordinates.  Expected reference claims are: (i) C10 alpha instability/rearrangement; (ii) OH-assisted beta-cation quenching competing with dehydrogenation for the short-chain case; (iii) stabilized C15 and C17 alpha cations with direct dehydrogenation favored; and (iv) chain length changes the pathway and therefore terminal-olefin selectivity.  Exact barriers are not scored.

## 6. Limitations and interpretation boundaries

The public explicit SMILES make the task executable but are not asserted to be the authors' optimized coordinates.  Carbocation conformers, solvation, electrode fields and entropy conventions can change numerical barriers.  A calculation that cannot locate a TS may be reported as a bounded negative result only when the input, attempted search, frequency/IRC diagnostics and limitation are documented.  The task tests pathway discrimination and validation, not an exact reproduction of inaccessible source coordinates.
