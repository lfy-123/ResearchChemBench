# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain regioselectivity in Pd-catalyzed, directing-group-free C–H arylation of tert-butylbenzene with cyclohex-2-en-1-ol. The selectivity-determining Int3 → TS2 → Int4 C–H activation is claimed to favor the meta pathway for this substrate; the broader study attributes selectivity to dual-ligand organization and noncovalent interactions.

## 2. System and model boundary

The modeled system contains tert-butylbenzene, N-acetylphenylalanine, quinoxaline ligand L22, Pd/Ag-containing catalytic components, HFIP, and cyclohex-2-en-1-ol. The scored comparison is the relative Gibbs barriers for meta-, para-, and ortho-C–H activation from Int3. Later catalytic-cycle steps are outside this task.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and optimize stationary points | Reactant complex, Int3, TS2 candidates, Int4 | Gaussian 16 | B3LYP-D3; 6-31G(d,p) for main-group atoms; SDD/ECP for Pd and Ag; SMD(HFIP) | Optimized geometries and energies | ev_doc_cfb7ab174285_001280_aedd9148d4b3; ev_doc_cfb7ab174285_001362_ae8751630578 |
| 2 | Refine electronic energies | Optimized geometries | Gaussian 16 single points | 6-311++G(d,p) for main-group atoms; SDD for Pd/Ag; SMD(HFIP) | Refined energies | ev_doc_cfb7ab174285_001290_4717bed5d882 |
| 3 | Add thermochemistry | Optimized minima and TSs | Gaussian 16 frequency analysis | 298.15 K, 1 atm standard condition | Gibbs free energies | ev_doc_cfb7ab174285_001293_ada77097b7ea; ev_doc_cfb7ab174285_001294_5b3f13255997 |
| 4 | Validate TSs and connections | TS2 structures | Gaussian 16 | One imaginary mode; IRC to correct minima | Validated TS assignments | ev_doc_cfb7ab174285_001280_aedd9148d4b3 |
| 5 | Compare regioisomeric pathways | Int3, m-TS2, p-TS2, o-TS2, Int4 | Relative Gibbs-energy analysis | Barriers referenced to Int3 | ev_doc_4fc1c130af18_000189_3e4a5f40e7b8; ev_doc_cfb7ab174285_001302_df0bae744c4a |
| 6 | Interpret selectivity | m-TS2 and p-TS2 | NCI analysis with Multiwfn; visualization with VMD | Fragment analysis of substrate/rest of system | NCI-based interpretation | ev_doc_cfb7ab174285_001302_df0bae744c4a |

## 4. Validation and analysis protocol

The SI states that TSs were confirmed as first-order saddle points with one imaginary frequency corresponding to the reaction coordinate, and IRC calculations were used to confirm connection to the correct minima. The authors examined alternative meta C–H activation modes and the ortho and para pathways, then compared Gibbs barriers and analyzed NCI differences between meta and para structures.

## 5. Private reference results

For the tert-butylbenzene selectivity model, the published relative Gibbs barriers from Int3 are 11.6 kcal/mol (m-TS2), 12.2 kcal/mol (p-TS2), and 18.2 kcal/mol (o-TS2). The meta step is reported as exergonic by 2.8 kcal/mol to Int4. The main-paper discussion identifies meta as the lowest of these three pathways. The SI further reports an amide-O-triggered meta mode as the most facile mode and discusses a C–H···π interaction in m-TS2.

## 6. Limitations and interpretation boundaries

These references are method-specific computational results, not direct experimental activation energies. Conformer coverage, functional/basis sensitivity, standard-state conventions, and the treatment of solvent can shift absolute values. The task should score transparent validation and a consistent comparison, and should not treat an unvalidated stationary point or a different chemical model as equivalent to a validated reproduction.
