# Private paper route

## 1. Scientific objective and author claim

Compare low-frequency lateral Y2 modes in Y2@Ih and Y2@D5h C80(CH2Ph); authors report higher D5h modes and longer T1.

## 2. System and model boundary

Neutral S=1/2 96-atom molecules, 87 C, 7 H, 2 Y, SI optimized geometries.

## 3. Authors' implemented computational route

|Step|Purpose|Input|Method/software|Key parameters|Output|Source evidence|
|---|---|---|---|---|---|---|
|1|optimize|geometries|ORCA DFT|PBE/def2-TZVP, Dolg ECP Y|Hessian|ev_doc_3788c5dd4ff8_000085_a691892a67f1|
|2|frequencies|Hessian|ORCA|same|normal modes|ev_doc_3788c5dd4ff8_000085_a691892a67f1|

## 4. Validation and analysis protocol

Inspect Y2 participation and distinguish lateral transverse from longitudinal stretching.

## 5. Private reference results

Ih 49.9,54.9,65.2,68.9; D5h 67.4,81.9,90.2,93.8 cm-1. Both are four-mode sets: main PDF p8 and SI Table S3a/S3b (PDF pp21-22). The old Ih list omitted 68.9 and its key point approximated the first frequency as 48 rather than 49.9; the numeric target field also incorrectly repeated the tolerance as 12.0. These source-transcription errors were corrected on 2026-09-18, retaining the 12 cm-1 tolerance, public geometry, scientific objective and schema. No EPR/g/hyperfine tensor production is required by this fixed-geometry vibrational subtask.

## 6. Limitations and interpretation boundaries

Low-frequency harmonic modes are method- and anharmonicity-sensitive.
