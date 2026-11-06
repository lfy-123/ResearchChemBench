# Private source-grounded construction route

This file, all evaluation files, the workflow review, and task metadata are private. Only the autonomous task instructions, canonical submission contract, and neutral system input are solver-facing.

## Frozen scientific core

The immutable Stage05 research contract is copied without changing any field or source quote. Its original scientific question is used exactly. The phenomenon is a homogeneous solution photochemical skeletal rearrangement of a neutral organic cyclic ketone, not a coordination or ligand-exchange calculation. The authors explicitly say they conducted DFT on model substrate 1a, report a reaction profile and crossing calculations, and describe their method in the SI. These actually performed computations, not an experiment-only replacement or an isolated prescribed computational substep, motivate the shared explanatory question.

The public projection retains three inputs in their original ID/kind/order. A separate task_definition ledger removes opaque source labels and clarifies the substrate ring numbering. The substrate and product systematic names are verified rather than copied on trust. No source-name correction is needed and no author mechanism or optimized geometry is exposed in the autonomous view. There are no extra public assets, source PDFs, raw pages, structure screenshots, or source-export scripts.

## Identity closure

The original substrate drawing on SI S6 agrees with methyl 2-oxo-1-(2-phenylallyl)cyclopentane-1-carboxylate: the ester-bearing ring carbon is also bonded to CH2–C(phenyl)=CH2 and is adjacent to the ketone carbonyl. Its precursor/allylation description in the main text is consistent with that graph. The original product drawing on SI S41 and the reaction drawing on main page 3 agree with methyl 5-oxo-7-phenylbicyclo[5.1.0]octane-1-carboxylate. The ester and phenyl substituent bonds in S41 are both dashed, providing the same-face relative configuration. Absolute configuration is not fixed by the public problem.

Identity-only inspection of the supplied coordinate records checks heavy-atom connectivity, formula C16H18O3, and substituent sides of the cyclopropane plane. It does not optimize a structure, calculate an energy, execute the research, or recalculate any author reference. In the S106/S107 coordinate ordering, substrate ring C1,C2,C3,C4,C5 map to heavy-atom rows 4,5,1,2,3; the allyl chain uses rows 7,8,10 with phenyl attached through row 9, and the ester carbonyl is row 16. Both coordinate graphs match the drawn/name-defined substrate.

For the S119-S120 cis record, product C1 through C8 map to heavy-atom rows 4,3,2,1,8,7,6,5; the ketone oxygen is row 9, ester carbonyl is row 10, and phenyl ipso carbon is row 14. Thus the ketone is at C5, the ester at bridgehead C1, and phenyl at bridgehead C7. Ester and phenyl bond vectors have the same sign against the cyclopropane-plane normal. For the S120-S121 trans record, C1 through C8 map to heavy-atom rows 4,3,2,1,5,8,7,6, with ketone oxygen row 13, ester carbonyl row 9 and phenyl ipso carbon row 14. It has the same named graph and opposite substituent-face signs. No unresolved essential identity conflict is found. These source coordinates remain private and are not autonomous starting geometries.

## Author computations, conditions and limits

The actual method paragraph reports Gaussian 16, omegaB97X-D/def2-SVP geometry and frequency calculations with SMD(DMSO), def2-TZVP single points, Grimme quasi-harmonic corrections with a 100 cm-1 cutoff in Shermo, sobMECP, and ABCluster with up to the reported 20 low-energy conformers subsequently optimized by DFT. No exact temperature or additional unreported starting settings are invented. The source claims frequency-based stationary-point classification; the Builder does not claim an author IRC calculation. Its lowest-conformer assertion is a reported methodological claim, not independent proof that all conformers were found.

The four frozen references retain their original IDs, values, methods, energy definitions, conditions, comparison scopes, uncertainty, and source bindings: CR1 is the substrate singlet/triplet Gibbs separation (52.2 displayed; 56.8 electronic, with frozen value null retained); CR2 is the 9.7 first-addition Gibbs barrier relative to the model triplet substrate; CR3 is the approximately 3.7 cis/trans crossing electronic-energy difference; CR4 is the 23.5 cis/trans product Gibbs-energy preference. The TXO 65.5 benchmark is contextual rather than an author-computed substrate reference. These quantities are not reaction rates or unique proof of an explanation.

Both original energy diagrams were viewed. Main prose gives HAT 12.1 while the diagrams give 12.2; prose gives intermediate 3B -13.6 while both diagrams give Gibbs -14.4 (electronic -17.5). These optional context discrepancies remain explicit and are not resolved by choosing a convenient value. They do not contradict the four selected frozen comparisons or the substrate/product identities, and no exact scoring rule is built from them. The thermal-isomerization experiments discussed by the authors concern other products, 22 and 27, not a measured rate for model product 2. Diagnostic trapping, quenching, racemization, intermediates, excited-state assignments and all calculated answers remain private in autonomous mode.

## Paired view and evaluation

One autonomous scientific core is constructed. The program can derive the guided reproduction task solely by inserting reproduction_protocol.guidance_markdown immediately before the shared public-input heading. The protocol contains complete verbatim source blocks for the actual reported mechanism and methods, plus source-bound figure/connectivity readings and preserved limitations. The shared task conditionally requests execution and assessment of this baseline only when it is disclosed. Justified substitutions are reported in the same investigation fields and report; there is no extra reproduction goal, dataset, reference, deliverable, tolerance, or scoring rule.

The two core scored conclusions concern explaining the actual transformation and relative stereochemistry; neither statement nor expected text prescribes the authors' mechanism or pathway numbers. All author computations and interpretations are separately available as unweighted conditional references. Process rules reward relevant testable explanations, informative models/tests, real execution, claim-appropriate validation, evidence-driven decisions and calibrated uncertainty. Their combined weight is 75; question-resolution criteria total 25. No exact-energy scoring target or numeric tolerance is imposed because the question is explanatory and methods are not uniquely prescribed. Omitting an optional author descriptor or hypothesis is not a failure or score deduction when another relevant explanation is supported. Honest unresolved research may earn process credit without automatic resolution credit.

The evidence map embeds complete frozen source-block text with UTF-8 SHA256, including all Stage05 source bindings and every new ledger/protocol/identity reference. Page-marker excerpts are location/provenance markers only; the scientific visual readings below describe what was actually viewed. Original PDFs and source pages are not copied into the output package.

## Actual private visual inspection

Documents were listed with document_query --list. Relevant pages were rendered from the original PDFs with document_query --document DOC --render-page N --output scratch/page.png and opened with the image-view tool. Enlarged private crops were also viewed only for the main and SI energy diagrams. The originals inspected were:

- `pdf-page-doc_94166c8efba9-p3`: Reaction drawing, thioxanthone structure, conditions, isolated-yield entry and product relative stereochemistry.
- `pdf-page-doc_94166c8efba9-p7`: Diagnostic panels and computational profile, including parenthesized electronic energies and the syn/anti crossing labels; the profile was also inspected enlarged.
- `pdf-page-doc_f1d010f20b60-p6`: Named substrate and its graph-explicit line drawing.
- `pdf-page-doc_f1d010f20b60-p41`: General solution reaction procedure, named product, drawn 5-oxo product graph and two same-face dashed substituent bonds.
- `pdf-page-doc_f1d010f20b60-p105`: Actual computational-method paragraph and supplementary profile; the profile was also inspected enlarged, including the optional HAT branch.
- `pdf-page-doc_f1d010f20b60-p106`: Neutral singlet substrate label, charge/multiplicity, structure thumbnail and Cartesian coordinate record.
- `pdf-page-doc_f1d010f20b60-p107`: Computed triplet substrate label, charge/multiplicity, structure thumbnail and coordinate record.
- `pdf-page-doc_f1d010f20b60-p119`: cis product label, charge/multiplicity, structure thumbnail and start of coordinate record.
- `pdf-page-doc_f1d010f20b60-p120`: cis coordinate continuation followed by trans product label, charge/multiplicity, structure thumbnail and start of coordinate record.
- `pdf-page-doc_f1d010f20b60-p121`: Top-of-page trans coordinate continuation; unrelated following product data are not used as identities or extra goals.

## Primary source bindings

- `ev_doc_f1d010f20b60_000033_27333f5604c1`: doc_f1d010f20b60, page 6.
- `ev_doc_f1d010f20b60_000267_1e6f183b304f`: doc_f1d010f20b60, page 41.
- `ev_doc_94166c8efba9_000019_70e2154e0e71`: doc_94166c8efba9, page 2.
- `ev_doc_94166c8efba9_000025_6f1e6a8fc206`: doc_94166c8efba9, page 3.
- `ev_doc_94166c8efba9_000049_7b7253538bca`: doc_94166c8efba9, page 6.
- `ev_doc_94166c8efba9_000062_19228e69f205`: doc_94166c8efba9, page 8.
- `ev_doc_f1d010f20b60_000717_7bb6c40958e0`: doc_f1d010f20b60, page 105.
- `ev_doc_94166c8efba9_000056_a5943517c9d8`: doc_94166c8efba9, page 7.
- `ev_doc_f1d010f20b60_000718_a50356ae3a3a`: doc_f1d010f20b60, page 105.
- `ev_rescue_20261018_g03_p11_main007_figure_3d`: doc_94166c8efba9, page 7.
- `layout-doc_f1d010f20b60-p106-b5`: doc_f1d010f20b60, page 106.
- `layout-doc_f1d010f20b60-p107-b5`: doc_f1d010f20b60, page 107.
- `layout-doc_f1d010f20b60-p119-b5`: doc_f1d010f20b60, page 119.
- `layout-doc_f1d010f20b60-p120-b0`: doc_f1d010f20b60, page 120.
- `layout-doc_f1d010f20b60-p120-b5`: doc_f1d010f20b60, page 120.
- `layout-doc_f1d010f20b60-p121-b0`: doc_f1d010f20b60, page 121.
