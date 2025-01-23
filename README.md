[![Ruff](https://github.com/poppy-io/shacl2datalog/actions/workflows/ruff.yml/badge.svg)](https://github.com/poppy-io/shacl2datalog/actions/workflows/ruff.yml)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fpoppy-io%2FSHACLog%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

# shacl2datalog
Proof-of-concept SHACL to Datalog transpiler written in Python.

## Usage
With Nix:
```nix run```

## Minimum required extensions to Datalog in order to represent SHACL
- Logical:
  - Negation (which can be used to implement XOR)
  - Disjunction (possible workaround with multiple rules?)
  - Comparison(?): ensuring variables are distinct for cardinality rules
- Arithmetic:
  - Integer comparison (lt, eq, possibly also Suc?)
- Strings:
  - Comparison (for language constraints)
  - Length
  - Regex (!!)
- Date / Time handling; difficult due to lack of complex expressions as parameters, but various (extremely verbose)
workarounds
