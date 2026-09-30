# Private paper route

## 1. Scientific objective and author claim
The paper tests whether retaining lignin-derived ortho-methoxy groups creates an intramolecular hydrogen bond to a curing-generated hydroxyl, lowering polarity and dielectric constant. The quantum-chemical comparison uses EPI1 (without methoxy) and EPI2 (with methoxy).

## 2. System and model boundary
The computational objects are neutral, closed-shell characteristic cured-epoxy fragments shown in Fig. 4D/E and tabulated in SI section 2.0. EPI1 and EPI2 contain the same cured fragment, with EPI2 carrying the ortho-methoxy substituent. Reported properties are gas-phase molecular dipole and hydroxyl-oxygen electrostatic potential; the polymer dielectric measurements are contextual, not directly computed.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize EPI1 geometry and assess minimum | SI EPI1 coordinates | Gaussian 16 A.03; B3LYP with Grimme D3(BJ) | 6-31G*; frequency calculation | optimized EPI1 geometry and frequencies | ev_doc_6fcbe6c501d3_000190_8ba207dcd7ac; ev_doc_6fcbe6c501d3_000191_ab4d5ab200d1 |
| 2 | Optimize EPI2 geometry and assess minimum | SI EPI2 coordinates | Gaussian 16 A.03; B3LYP-D3(BJ) | 6-31G*; frequency calculation | optimized EPI2 geometry and frequencies | ev_doc_6fcbe6c501d3_000190_8ba207dcd7ac; ev_doc_6fcbe6c501d3_000191_ab4d5ab200d1 |
| 3 | Evaluate electronic properties | optimized geometries | B3LYP-D3(BJ) single point; Gaussian 16; Multiwfn 3.8(dev) for ESP | ma-def2-TZVPP with dispersion; vdW-surface ESP | dipole moments and hydroxyl-O ESP | ev_doc_6fcbe6c501d3_000191_ab4d5ab200d1; ev_doc_6fcbe6c501d3_000302_18a146d62fe2 |
| 4 | Compare substituent effect | EPI1/EPI2 properties | arithmetic comparison | percent change relative to EPI1 | polarity change and mechanistic interpretation | ev_doc_6fcbe6c501d3_000303_deaaaad57e30; ev_doc_6fcbe6c501d3_000304_9eb7ebf8962d |

## 4. Validation and analysis protocol
The authors optimized both structures at the same theoretical level, used frequency calculations to establish minima, inspected the EPI2 side-on geometry for an intramolecular hydrogen bond, and compared dipoles and ESP maps. The paper also relates the calculation to temperature-dependent O-H FTIR behavior and lower water uptake in methoxy-containing cured resins.

## 5. Private reference results
The paper reports EPI2 dipole 1.9036 D, EPI1 dipole 2.2223 D, a 14.3% EPI2 reduction, hydroxyl-O ESP values of -33.14 and -36.009 kcal mol-1 for EPI2 and EPI1 respectively, and an eight-membered intramolecular hydrogen-bond motif. These values are evaluator-only.

## 6. Limitations and interpretation boundaries
The article text and Fig. 4 caption are inconsistent about the displayed geometry level (the methods section specifies B3LYP-D3(BJ)/6-31G* optimization, while the caption labels structures CAMB3LYP/6-311G(d,p)); this is recorded as a source limitation. A gas-phase fragment dipole is a mechanistic proxy, not a direct bulk dielectric constant prediction, and conformational sampling and method sensitivity can affect absolute values.
