---
software_id: lobster
versions: ["5"]
topics: [troubleshooting, errors]
aliases: [LOBSTER failed, basis error, charge spilling]
---
# LOBSTER Troubleshooting

## Missing or incompatible input
Confirm every required upstream file is staged under its exact filename. Rebuild the upstream VASP calculation when structures, POTCAR order, k-points, band count, or wavefunction format are inconsistent.

## Projection quality
High spilling is a scientific validation failure even when LOBSTER terminates normally. Revisit the basis, band coverage, and upstream electronic settings before interpreting bonding curves.
