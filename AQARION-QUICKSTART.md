```markdown

# AQARION — Quickstart Guide

Welcome to AQARION! This guide gets you from zero to fingerprint in under five minutes.

---

## 1. Prerequisites

- Python 3.8 or higher
- `pip` (or `pip3`)

## 2. Installation

Install the required packages:

```bash
pip install sympy numpy
```

If you prefer using the Makefile (see below), run make install.

3. Run the test suite

Verify everything works:

```bash
python aqarion.py
```

You should see a summary like RESULTS: 33 passed, 0 failed.

4. Basic usage example

Create a Python script (e.g., example.py) with the following code:

```python
from aqarion import UniformPartition, UniformAnalyzer

# 1. Define a uniform partition: 3 blocks of size 3
blocks = [[0,1,2], [3,4,5], [6,7,8]]
partition = UniformPartition(blocks)

# 2. Define a deterministic transition (permutation)
transition = [1,2,0, 4,5,3, 7,8,6]

# 3. Create an analyser
analyzer = UniformAnalyzer(partition, transition)

# 4. Print the full fingerprint as JSON
print(analyzer.fingerprint.to_json())
```

Run it:

```bash
python example.py
```

5. Interpreting the fingerprint

The output is a JSON dictionary with these main sections:

Section Content
system Number of states (n), blocks (m), and partition type (k or block_sizes).
exact Exact rational invariants: rank, nullity, trace, nilpotent index, Frobenius norm².
geometric Orthonormal bases for image and kernel of the defect operator.
spectral Numeric singular values, entropy, stable rank, condition number.
associated Norms and ranks of related operators (commutator, dual defect, etc.).
classification Qualitative labels: rank_class, defect_class, maturity.

The most important metrics are:

· operator_rank – number of independent defect modes. Zero means the partition is invariant.
· nilpotent_index – must be 1 or 2 for valid projections.
· singular_values – reveal the spectral structure of the defect.

6. GPF (non‑uniform partitions)

If your blocks have different sizes, use GeneralPartition and GeneralAnalyzer:

```python
from aqarion import GeneralPartition, GeneralAnalyzer

blocks = [[0], [1,2,4,8], [3,5,6,9,10,12], [7,11,13,14], [15]]
partition = GeneralPartition.from_blocks_list(blocks)
transition = list(range(1,16)) + [0]
analyzer = GeneralAnalyzer(partition, transition)
print(analyzer.fingerprint.to_json())
```

7. Validate a fingerprint

Every fingerprint object has a validate() method:

```python
valid, msg = analyzer.fingerprint.validate()
print(valid, msg)   # (True, "valid") if all checks pass
```

8. Next steps

· Read the full source code – it's thoroughly commented.
· Extend the framework with your own operators.
· Contribute back improvements or new theorems.

Happy coarse‑graining!

```

---

## Minimal Makefile

Save the following as `Makefile` in your project root.

```makefile
# Minimal Makefile for AQARION

.PHONY: help install test clean example fingerprint

help:
	@echo "Available targets:"
	@echo "  install      Install required Python packages"
	@echo "  test         Run the test suite"
	@echo "  example      Run a simple example (creates example.py if missing)"
	@echo "  fingerprint  Generate a fingerprint JSON file (demo)"
	@echo "  clean        Remove __pycache__ and temporary files"

install:
	pip install sympy numpy

test:
	python aqarion.py

example:
	@if [ ! -f example.py ]; then \
		echo "Creating example.py..."; \
		echo 'from aqarion import UniformPartition, UniformAnalyzer' > example.py; \
		echo 'blocks = [[0,1,2], [3,4,5], [6,7,8]]' >> example.py; \
		echo 'partition = UniformPartition(blocks)' >> example.py; \
		echo 'transition = [1,2,0, 4,5,3, 7,8,6]' >> example.py; \
		echo 'analyzer = UniformAnalyzer(partition, transition)' >> example.py; \
		echo 'print(analyzer.fingerprint.to_json())' >> example.py; \
	fi
	python example.py

fingerprint:
	python -c "from aqarion import UniformPartition, UniformAnalyzer; \
	           p = UniformPartition([[0,1,2],[3,4,5],[6,7,8]]); \
	           a = UniformAnalyzer(p, [1,2,0,4,5,3,7,8,6]); \
	           print(a.fingerprint.to_json())" > fingerprint.json
	@echo "Fingerprint written to fingerprint.json"

clean:
	rm -rf __pycache__ *.pyc *.pyo
	rm -f example.py fingerprint.json
```

---

How to use the Makefile

· make install – installs dependencies.
· make test – runs the full test suite.
· make example – creates a minimal example script and runs it.
· make fingerprint – runs a demo and saves the fingerprint to fingerprint.json.
· make clean – removes generated files and cache.

---

The polished aqarion.py script you requested is already provided in my previous response. You can now package the three files together: aqarion.py, QUICKSTART.md, and Makefile. Enjoy using AQARION!
