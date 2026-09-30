# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to model 1:1 Ln3+ complexes of H2KHQ and compare syn and anti arrangements of the two 8-hydroxyquinoline arms. It reports that syn is favored over anti across the lanthanide series, supporting the conformational/thermodynamic interpretation of H2KHQ binding and size selectivity.

## 2. System and model boundary

The La benchmark system is [La-KHQ]+, modeled as a +1, singlet cation containing one La center and the fully deprotonated KHQ ligand (C32H38N4O6). The two endpoints are the syn and anti arm arrangements. The author calculations use continuum water corrections and 298 K solution standard-state thermochemistry; explicit solvent and counterions are not included in the endpoint calculations.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate syn starting geometry | crystal-derived [La-HKHQ]2+ arrangement, remove H8 to model +1 species | structural preparation | La3+ center; syn arms | syn [La-KHQ]+ starting structure | ev_doc_924dc5cd83b8_000328_56a66f50478b, ev_doc_ee2b6aed5d22_000308_18269a7ce1cd |
| 2 | Optimize each endpoint | syn and anti starting geometries | Gaussian16 Rev. C.01, ωB97XD | def2svp for C/H/N/O; LCRECP and associated basis for Ln; nosymm; int=ultrafine; pseudosinglet | optimized geometries and energies | ev_doc_924dc5cd83b8_000328_56a66f50478b |
| 3 | Confirm minima | optimized geometries | Gaussian16 frequency calculation | absence of imaginary frequencies | vibrational validation and thermal terms | ev_doc_924dc5cd83b8_000348_97770d902739 |
| 4 | Add aqueous electronic-energy correction | optimized geometries | Gaussian16 single point with SMD | water solvent; parameterized Ln ionic radii | solvated electronic energies | ev_doc_924dc5cd83b8_000349_304791c92618 |
| 5 | Obtain solution free energies | frequency and SMD results | GoodVibes with Grimme quasi-harmonic treatment | 100 cm-1 cutoff; scale factor 1.0; 298 K; 1 M complex standard state; water 55.5 M correction | G°aq for each endpoint | ev_doc_924dc5cd83b8_000353_fda087bdcc59, ev_doc_924dc5cd83b8_000354_b3f40026500e, ev_doc_924dc5cd83b8_000355_045c63dabe2b, ev_doc_924dc5cd83b8_000357_368ebcd7142d |
| 6 | Compare conformers | endpoint G°aq values | Equation S2 arithmetic | ΔG°conf = G°aq(anti) − G°aq(syn) | conformational preference | ev_doc_924dc5cd83b8_000371_badc800c4c37, ev_doc_924dc5cd83b8_000393_c31bbb7d8bdf |

## 4. Validation and analysis protocol

The authors used frequency calculations to identify local minima and compared the aqueous Gibbs energies of syn and anti structures. Their broader series analysis also screened multiple C2-symmetric conformations and used the conformational comparison to interpret binding and ligand-strain trends. The paper cautions that calculated trends are qualitative and that gas-phase ion-energy treatment can produce quantitative discrepancies.

## 5. Private reference results

For La, the SI coordinate/log section reports G(298 K) = -1941.809708 for La-syn-KHQ(1+) and -1941.800071 for La-anti-KHQ(1+), in the author gas-phase log outputs. The SI Table S2 reports aqueous free energies of -1218165.73 (syn) and -1218161.53 (anti) kcal mol-1 and ΔG°conf = +4.2 kcal mol-1. Thus anti minus syn is positive and syn is preferred in the published calculation.

## 6. Limitations and interpretation boundaries

The reference is a relative conformational result within the stated model, not an experimental free energy. The endpoint structures are local-minimum calculations and do not prove exhaustive global conformational sampling. Protonation state, explicit hydration, standard-state conventions, ECP treatment, and low-frequency entropy treatment can affect absolute values; comparisons must preserve a consistent convention.
