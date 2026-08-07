# Runtime Cache

This directory contains regenerable runtime state. It must not contain the
toolbox's canonical model weights or native software installations.

The default layout is:

```text
.runtime_cache/
├── semantic_embeddings/   # Generated Action and software-document indexes
├── huggingface/           # Hugging Face Hub/Xet transfer cache
├── matplotlib/            # Font discovery cache
├── mesa_shader_cache/     # Mesa/OpenGL shader cache
├── opencode/              # OpenCode helper assets and provider metadata
├── OPENFF_NAGL_MODELS/    # Dynamically fetched OpenFF NAGL models, if any
└── pip/                    # pip HTTP and self-check cache
```

ResearchChemBench sets `XDG_CACHE_HOME` to this directory for toolbox runtime
profiles. Override the location with `RESEARCHCHEMBENCH_RUNTIME_CACHE` when the
cache must live on local scratch storage.

All contents except this README and tracked directory placeholders may be
deleted when no benchmark process is running. Programs recreate generic caches
on demand. Rebuild semantic indexes with:

```bash
.envs/researchchembench/bin/python \
  chemistry_toolbox/scripts/cache_minilm_model.py
```

The model used to generate those indexes remains in
`.model_cache/all-MiniLM-L6-v2/`.
