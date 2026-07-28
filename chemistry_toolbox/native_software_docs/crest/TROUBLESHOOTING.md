---
software_id: crest
versions: ["3"]
topics: [troubleshooting, errors]
aliases: [CREST failed, incompatible CREST flags]
---
# CREST Troubleshooting

## Immediate option failure
Check the installed version and remove mutually exclusive run modes. Verify that the XYZ target exists in the job directory and that charge and unpaired-electron settings are consistent.

## Runtime failure
Match CREST thread settings to the scheduler CPU request. Inspect the underlying xTB error before increasing resources or retrying.
