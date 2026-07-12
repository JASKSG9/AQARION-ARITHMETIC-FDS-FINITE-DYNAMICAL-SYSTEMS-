# ======================================================================
# AQARION-ARITHMETIC — Official Makefile
# Version: v21.0-LOCKED
# Purpose: Single entry point for build, test, certification, and release.
# Author: AQARION Research Node #10878
# ======================================================================

# ---- Variables ----
PYTHON  ?= python3
LAKE    ?= lake
CC      ?= gcc
CXX     ?= g++

LEAN_DIR   := formal/lean
ORACLE_DIR := oracle
VERIFY_DIR := verification
PAPERS_DIR := papers
OUTPUT_DIR := /mnt/agents/output

# ---- Default Target ----
.DEFAULT_GOAL := help

# ---- Phony Targets (does not correspond to actual files) ----
.PHONY: help setup build build-python build-lean build-cpp \
        test test-python test-lean \
        clean dist certify all

# ---- 1. Help ----
help:
	@echo "======================================================================"
	@echo " AQARION-ARITHMETIC Official Makefile"
	@echo "======================================================================"
	@echo " Usage: make [TARGET]"
	@echo ""
	@echo " Targets:"
	@echo "   setup       : Install Python dependencies and setup Lean/elan"
	@echo "   build       : Build all components (Python, Lean, C++)"
	@echo "   test        : Run full test suite (Python + Lean)"
	@echo "   certify     : Generate SHA-256 hashes and certificate manifests"
	@echo "   clean       : Clean build artifacts and caches"
	@echo "   dist        : Create final RO-Crate artifact and package for release"
	@echo "   all         : Full pipeline (setup → build → test → certify → dist)"
	@echo "======================================================================"

# ---- 2. Setup Environment ----
setup:
	@echo "[AQARION] Setting up Python environment..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "[AQARION] Setting up Lean 4 / Elan..."
	curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh
	elan install leanprover/lean4:stable
	cd $(LEAN_DIR) && $(LAKE) exe cache get
	cd $(LEAN_DIR) && $(LAKE) build
	@echo "[AQARION] Setup complete."

# ---- 3. Build Components ----
build-python:
	@echo "[AQARION] Building Python verification modules..."
	# Use pyflakes or mypy to check syntax if you wish
	$(PYTHON) -c "import numpy, fractions; print('Python environment ready.')"

build-lean:
	@echo "[AQARION] Building Lean 4 formalization..."
	cd $(LEAN_DIR) && $(LAKE) build
	@echo "[AQARION] Lean build complete. LC1-LC3 verified."

build-cpp:
	@echo "[AQARION] Building C++ independent oracle..."
	cd $(ORACLE_DIR) && $(MAKE)
	@echo "[AQARION] C++ oracle compiled."

build: build-python build-lean build-cpp
	@echo "[AQARION] All components built successfully."

# ---- 4. Testing & Verification ----
test-python:
	@echo "[AQARION] Running Python verification pipeline..."
	# Run the master verification script
	cd $(VERIFY_DIR) && $(PYTHON) verify_aqarion.py
	@echo "[AQARION] Python test suite passed."

test-lean:
	@echo "[AQARION] Running Lean 4 Linter & Checks..."
	cd $(LEAN_DIR) && $(LAKE) exe runLinter
	cd $(LEAN_DIR) && $(LAKE) build AQARION.Tests
	@echo "[AQARION] Lean verification checks passed."

test: test-python test-lean
	@echo "[AQARION] All verification gates PASS."

# ---- 5. Certification & Hashing ----
certify:
	@echo "[AQARION] Generating SHA-256 certification manifests..."
	# Generate the full verification certificate
	$(PYTHON) $(VERIFY_DIR)/generate_manifest.py
	# Verify all hashes against stored checksums
	sha256sum -c checksums.sha256
	@echo "[AQARION] Certification complete. Evidence locks are secure."

# ---- 6. Distribution & RO-Crate ----
dist:
	@echo "[AQARION] Packaging RO-Crate publication artifact..."
	mkdir -p $(OUTPUT_DIR)/aqarion_v21_dist
	# Copy all essential files to the output directory
	cp -r $(LEAN_DIR) $(OUTPUT_DIR)/aqarion_v21_dist/formal/
	cp -r $(VERIFY_DIR) $(OUTPUT_DIR)/aqarion_v21_dist/verification/
	cp -r $(ORACLE_DIR) $(OUTPUT_DIR)/aqarion_v21_dist/oracle/
	cp CHECKPOINT.md README.md LICENSE cert_manifest.json $(OUTPUT_DIR)/aqarion_v21_dist/
	# Generate the RO-Crate JSON-LD
	$(PYTHON) scripts/generate_rocrate.py --input $(OUTPUT_DIR)/aqarion_v21_dist --output $(OUTPUT_DIR)/ro-crate-metadata.json
	# Create a compressed archive
	cd $(OUTPUT_DIR) && tar -czf aqarion_v21.tar.gz aqarion_v21_dist/
	@echo "[AQARION] Distribution package created at $(OUTPUT_DIR)/aqarion_v21.tar.gz"
	@echo "[AQARION] RO-Crate metadata generated."

# ---- 7. Clean ----
clean:
	@echo "[AQARION] Cleaning build caches..."
	# Python cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	# Lean cache
	rm -rf $(LEAN_DIR)/lake-packages $(LEAN_DIR)/build $(LEAN_DIR)/.lake
	# C++ objects
	cd $(ORACLE_DIR) && $(MAKE) clean || true
	# Distribution output
	rm -rf $(OUTPUT_DIR)/aqarion_v21_dist $(OUTPUT_DIR)/aqarion_v21.tar.gz
	@echo "[AQARION] Project directory cleaned."

# ---- 8. All Pipeline ----
all: setup build test certify dist
	@echo "======================================================================"
	@echo " AQARION Pipeline Complete."
	@echo " Status: ✅ Core Verified · ⏳ Lean Active · 🟡 Open Problems Framed"
	@echo "======================================================================"

# ======================================================================
# End of Makefile
# ======================================================================
