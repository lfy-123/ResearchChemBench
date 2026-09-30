# Private paper route

## 1. Scientific objective and author claim

The paper tests whether para substituents tune the electronic character and strength of the azo bond in Azo-R recognition molecules. The authors claim that an electron-withdrawing p-nitrophenyl substituent gives a more electrophilic alpha nitrogen and a larger N=N bond dissociation energy than p-cyanophenyl, consistent with faster azoreductase reduction.

## 2. System and model boundary

The computational system is the neutral, closed-shell Azo-R recognition molecule containing a 2,5-dimethoxy/propargyloxy aryl azo unit and a para-substituted phenyl ring. This task uses the unambiguous aromatic members Azo-pNO2 and Azo-pCN. The measured bond is the azo N=N bond; the alpha nitrogen is the azo nitrogen bonded to the substituted phenyl ring.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize each Azo-R geometry | Molecular structures | Gaussian 16 DFT | B3LYP/6-31G | Optimized geometry | ev_doc_f911254dde1b_000322_62beb117886a |
| 2 | Determine alpha-nitrogen charge | Optimized geometry | Gaussian 16 frequency/charge analysis | B3LYP/6-31G | Electrostatic charge | ev_doc_f911254dde1b_000322_62beb117886a |
| 3 | Determine azo-bond dissociation energy | Optimized molecule and fragments | Gaussian 16 DFT | B3LYP/6-31G | BDE in kJ mol-1 | ev_doc_f911254dde1b_000322_62beb117886a |
| 4 | Compare substituent trends | Charges and BDEs | Table comparison | Ordering and numerical comparison | Electronic-modulation interpretation | ev_doc_fb34754decd5_000143_f3c8fb51d60f; ev_doc_fb34754decd5_000145_16b1b6499036 |

## 4. Validation and analysis protocol

The authors optimized the structures, then calculated alpha-nitrogen electrostatic charges and azo N=N bond dissociation energies. Their discussion compares the eight-member series by charge and BDE ordering and interprets a more positive alpha nitrogen as greater electrophilicity. The reported values for the two released members are used only in the private evaluator.

## 5. Private reference results

Table 1 reports Azo-pNO2: alpha-nitrogen charge -0.033 e and BDE 451.81 kJ mol-1; Azo-pCN: -0.063 e and 449.81 kJ mol-1. The charge ordering is pNO2 above pCN, and the BDE ordering is pNO2 above pCN.

## 6. Limitations and interpretation boundaries

The paper does not provide Cartesian coordinates, and the SI prose is ambiguous for several non-aromatic labels; those members are excluded. Charge values depend on charge partitioning and conformer treatment, so comparison is to the reported convention and broad trend. A BDE is not a kinetic barrier and does not by itself prove an enzymatic mechanism.
