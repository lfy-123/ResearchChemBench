# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to rationalize the slower reaction of the ortho-substituted nitroarene methyl 2-nitrobenzoate (1a) relative to nitrobenzene in photoinduced reductive C–N coupling. The authors claim that the singlet-to-triplet excitation requirement and the subsequent reaction with triphenylphosphine are higher for 1a because the ortho ester disrupts nitro-group planarity and creates steric interaction.

## 2. System and model boundary

The computed systems are neutral, triplet-state nitrobenzene and neutral, triplet-state methyl 2-nitrobenzoate, plus author-side PPh3-containing intermediates/transition states discussed in the mechanism. The reported gap comparison concerns the singlet-to-triplet excitation energies of the two nitroarenes. Solvent effects are represented with CPCM/toluene in the SI computational description.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize reactant, intermediate and transition-state geometries | Molecular structures and mechanistic starting geometries | DFT, Gaussian 09W | ωB97XD/def2SVP; CPCM with toluene | Optimized stationary points | ev_doc_911e18bce2df_000263_58dd61d6fb55; ev_doc_911e18bce2df_000264_773528fb8e51 |
| 2 | Validate stationary-point character | Optimized structures | Harmonic vibrational analysis in Gaussian 09W; modes inspected in GaussView 5 | Minima have no imaginary frequencies; TS has one reaction-coordinate imaginary frequency | Frequency validation and assigned structures | ev_doc_911e18bce2df_000263_58dd61d6fb55 |
| 3 | Compare singlet/triplet excitation requirements | Nitrobenzene and 1a electronic states | DFT energies from the optimized systems | Neutral singlet/triplet comparison; energy difference reported in kcal/mol | Excitation-gap comparison | ev_doc_0e8dda41ca74_000057_89b3e8847d13 |
| 4 | Relate excitation and PPh3 reaction energetics to reactivity | Nitroarene/PPh3 structures | Same DFT protocol | Ground-state-to-TS free-energy comparison; P–O distances interrogated | Mechanistic explanation of longer reaction time | ev_doc_0e8dda41ca74_000057_89b3e8847d13 |

## 4. Validation and analysis protocol

The SI says harmonic frequencies were used to distinguish minima from transition states and that vibrational modes were inspected for reaction-coordinate assignment. The paper compares the two excitation gaps and relates the difference to the observed longer time required for the ortho-substituted substrate. The mechanistic interpretation is bounded by the authors' wording (“suggests”/“plausible mechanism”) and by the fact that the calculations do not establish all photochemical kinetics.

## 5. Private reference results

The paper reports 58.24 kcal/mol for nitrobenzene and 71.79 kcal/mol for 1a. It reports ground-state-to-TS free energies of 4.32 kcal/mol for the nitrobenzene TS and 18.84 kcal/mol for the 1a TS, with P–O distances of 1.758 Å and 1.788 Å, respectively. The paper attributes the higher 1a values to loss of nitro-group planarity and steric interaction with PPh3.

## 6. Limitations and interpretation boundaries

The public benchmark scores the excitation-gap comparison, not a claim that one particular computational protocol is uniquely correct. Different defensible electronic-structure choices may shift absolute values; agents must disclose method, state definition, conformer treatment, solvent treatment and frequency validation. The source coordinate tables are layout-damaged in normalized extraction, so canonical connectivity is supplied publicly and starting geometries are not treated as hidden author inputs. Mechanistic conclusions should be stated as computational support within the defined model boundary, not as proof of complete photochemical kinetics.
