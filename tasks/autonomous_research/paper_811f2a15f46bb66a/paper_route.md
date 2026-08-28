# Private paper route

## 1. Scientific objective and author claim

The paper uses first-principles energetics to explain why hydrogen reduces undoped and Gd-doped ceria but produces an apparent oxidation/stabilization of lattice oxygen in Pr-doped ceria. The computational claim is that hydrogen incorporation and the oxygen-abstraction response differ among CeO2, Ce{Pr}O2, and Ce{Gd}O2.

## 2. System and model boundary

The modeled system is bulk fluorite CeO2 represented by a 2x2x1 supercell, with one Ce substituted by Pr or Gd, and hydrogen considered in an otherwise oxygen-complete lattice and after creation of one oxygen vacancy. Oxygen abstraction removes one O atom to vacuum. Hydrogen binding uses an isolated H atom reference; oxygen abstraction uses an isolated O atom reference. Bader analysis is applied to the incorporated H.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize bulk host and doped cells | 2x2x1 fluorite cells | VASP periodic DFT | PBE/PAW, 520 eV, 2x2x2 Monkhorst-Pack, U=5 eV Ce and 4 eV Pr/Gd, force 0.01 eV/A, energy 1e-8 eV/atom | relaxed CeO2, Ce{Pr}O2, Ce{Gd}O2 | ev_doc_42f227c213eb_000265_0195a1d0fc1f; ev_doc_42f227c213eb_000266_0c3204bae2be; ev_doc_42f227c213eb_000269_9775c3c7a91a; ev_doc_e90732311070_000148_18cd532a39a9 |
| 2 | Test H incorporation | relaxed stoichiometric cells plus H | VASP | E_H = E(host-H)-E(host)-E(H atom) | H binding energies and optimized H geometries | ev_doc_42f227c213eb_000291_77eab4ce87b6; ev_doc_42f227c213eb_000292_e801fc4bd53f; ev_doc_e90732311070_000253_c4cb7d40d536 |
| 3 | Test oxygen abstraction with/without H | relaxed host and H-containing cells, one O removed | VASP | E_Oabs = E(host)-E(host-O vacancy)-E(O atom), with the same convention for H-containing cells | oxygen-abstraction energies and H/vacancy structures | ev_doc_42f227c213eb_000283_0c6c26e628b8; ev_doc_42f227c213eb_000287_a906b5c74e65; ev_doc_e90732311070_000259_4e2056bebbde |
| 4 | Assign electronic character | converged H-containing charge densities | Bader analysis | charge partitioning of H | H charges | ev_doc_e90732311070_000391_5c328fc28046; ev_doc_e90732311070_000436_74ea32afb9fe |
| 5 | Interpret bonding | optimized VASP densities | LOBSTER pbeVaspFit2015 | charge spilling limited to 1% | PDOS/COHP interpretation | ev_doc_e90732311070_000100_6f8e1e4b8f1; ev_doc_e90732311070_000237_8e9a5e1c89 |

## 4. Validation and analysis protocol

The authors compare all three compositions on a common energy convention, distinguish stoichiometric H adducts from vacancy-occupied H, and use Bader charge plus local geometry to classify hydridic/protic character. The central comparison is the change in oxygen-abstraction energy on adding H.

## 5. Private reference results

Reported stoichiometric H binding energies are +0.64 eV (CeO2), -3.50 eV (Ce{Pr}O2), and -1.58 eV (Ce{Gd}O2). Reported H Bader charges are -0.12, +0.56, and +0.42 e, respectively. For CeO2, oxygen abstraction changes from +6.48 to +3.97 eV with H; for Ce{Pr}O2 it changes from +4.92 to +5.48 eV. The Gd change is reported as nearly unchanged. The qualitative conclusion is H-facilitated reduction for CeO2/Gd and H-associated oxygen stabilization for Pr.

## 6. Limitations and interpretation boundaries

The paper does not provide Cartesian/POSCAR files or a complete enumeration of adsorption sites. The released task therefore fixes a deterministic conventional-fluorite construction and asks for an independently justified site search. Absolute values are model-dependent; comparison requires reporting cell construction, charge/multiplicity, relaxation status, reference atom calculations, and uncertainty/sensitivity.
