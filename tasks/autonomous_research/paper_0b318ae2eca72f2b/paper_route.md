# Private paper route

## 1. Scientific objective and author claim

The paper investigates how oxygen coordination in VO₂ polymorphs controls proton intercalation and transport. For VO₂(B), the computational claim is that intermediate HₓVO₂ compositions are thermodynamically favorable and that protons preferentially bind the less-coordinated O1(2TM) oxygen network; this supports a continuous solid-solution pathway and hydrogen-bond-mediated transport.

## 2. System and model boundary

The relevant model is monoclinic VO₂(B), space group C2/m, with the conventional cell containing V₈O₁₆ (Z=8). The SI reports a=12.06944 Å, b=3.69153 Å, c=6.42105 Å, β=107.0365°, and asymmetric V1, V2, O1, O2, O3, and O4 coordinates. H₀.₂₅VO₂(B) therefore contains two H atoms in this conventional cell. The authors considered 0≤x≤1 configurations, relaxed both lattice parameters and atomic positions, and evaluated convex-hull/formation energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate proton configurations | VO₂(A/B) host cells and oxygen sites | Initial H placement near O, O–H directed toward nearest O | ~1.0 Å initial O–H; 120 A and 175 B configurations | Candidate HₓVO₂ structures | ev_doc_ce17ff654dd4_000370_555accdd14ae |
| 2 | Optimize structures and energies | HₙV₈O₁₆ for VO₂(B) | Spin-polarized VASP 5.4.4, PBE-PAW + U | 520 eV cutoff; U(V 3d)=3.25 eV; 3×10×6 Γ-centered mesh for B; forces <0.05 eV Å⁻¹; lattice and ions relaxed | Relaxed structures and total energies | ev_doc_ce17ff654dd4_000535_45ee0a29fc86; ev_doc_ce17ff654dd4_000538_b2eef9d36e53; ev_doc_ce17ff654dd4_000540_2357890ca95b; ev_doc_ce17ff654dd4_000543_74b480bd8cf2; ev_doc_ce17ff654dd4_000546_5f82b991cc5f |
| 3 | Determine stable compositions | Relaxed energies across x | Convex hull and formation-energy analysis | End members x=0 and x=1; H chemical potential from H₂ and JANAF entropy term | Formation-energy curve and stable configurations | ev_doc_ce17ff654dd4_000552_afb49ad18514; ev_doc_ce17ff654dd4_000553_b48111c10c65; ev_doc_ce17ff654dd4_000554_44ac2e5c5be3 |
| 4 | Analyze proton transport | Selected proton endpoints in VO₂(A/B) | CI-NEB | Unit-cell path; force criterion 0.1 eV Å⁻¹; barrier is max–min path energy | Migration paths and barriers | ev_doc_ce17ff654dd4_000026_ceed3def17b1; ev_doc_ce17ff654dd4_000049_766750a5c810 |

## 4. Validation and analysis protocol

The authors compare relaxed configurations by total energy, construct a convex hull, inspect proton binding sites and O–H···O networks, and compare calculated voltage profiles with galvanostatic data. For migration, they distinguish interoxygen hopping and O–H reorientation and define the CI-NEB barrier as the highest minus lowest optimized-path energy. The paper reports a low barrier below 0.36 eV for the favorable VO₂(A) c-axis path and identifies O1(2TM) as the dominant VO₂(B) acceptor, with O4(3TM) participating at higher proton content.

## 5. Private reference results

For VO₂(B), the source reports negative formation energies for 0<x≤0.75, no stable x=1.0 configuration, and primary proton binding at O1(2TM), with O4(3TM) contributing at higher x. It states that filling the available O1 sites corresponds to H₁/₂VO₂. The source does not expose an exact tabulated H₀.₂₅VO₂(B) formation-energy number in the recovered text; evaluation therefore uses source-supported sign/site conclusions rather than an invented numerical target.

## 6. Limitations and interpretation boundaries

The published search used finite cells and a finite configuration enumeration; the authors explicitly note that the minimal model does not bind the less-stable O3 site. Results are method- and cell-dependent and should be reported as a computational comparison, not as a universal thermodynamic phase diagram. Experimental solid-solution behavior is contextual validation, not a substitute for the submitted calculation.
