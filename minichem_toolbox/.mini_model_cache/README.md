# MiniChem Model Cache

The core chemistry calculations do not require a learned local model. This directory only retains
the optional `sentence-transformers/all-MiniLM-L6-v2` ONNX files used for semantic Action and
software-documentation search. The model was originally downloaded from Hugging Face and is placed
at `all-MiniLM-L6-v2/`.

The Agent harness model (`deepseek-v4-flash` in the OpenCode test) is accessed through its configured
API and is not stored in this directory.
