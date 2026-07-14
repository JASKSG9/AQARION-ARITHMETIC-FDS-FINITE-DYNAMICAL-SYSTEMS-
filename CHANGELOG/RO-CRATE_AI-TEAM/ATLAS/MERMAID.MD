
# ============================================================
# 7. AQARION-MERMAID.md — Mermaid Flowcharts
# ============================================================

mermaid = """# AQARION v0.4.1-final — Mermaid Diagrams

## 1. Evidence Pipeline Flow

```mermaid
flowchart TD
    A[Mathematician<br/>States Claim] --> B[AQARION Kernel]
    B --> C[Parse Claim]
    C --> D[Load Dependencies]
    D --> E[Build FDDS]
    E --> F[Compute Evidence<br/>Exact Arithmetic]
    F --> G[Generate Certificate<br/>status: UNVERIFIED]
    G --> H[Independent Verifier]
    H --> I{Hash Integrity?}
    I -->|Yes| J{Registry Version?}
    I -->|No| K[INVALID]
    J -->|Yes| L{Evidence Matches?}
    J -->|No| K
    L -->|Yes| M[VALID]
    L -->|No| K
    M --> N[Community Trust]
    K --> O[Investigate & Fix]
```

## 2. Certificate Schema v3.1

```mermaid
flowchart TD
    subgraph Certificate["AQARION Evidence Object (AEO)"]
        subgraph Meta["Metadata"]
            V[aqarion_version: 0.4.1-final]
            CV[certificate_version: 3.1.0]
        end
        
        subgraph Core["Core Content (Hashed)"]
            CI[claim_id]
            CS[claim_statement]
            ST[status: UNVERIFIED]
            DE[dependencies<br/>registry_version<br/>definitions<br/>theorems]
            SY[system<br/>states<br/>transition<br/>size]
            EV[evidence<br/>partition<br/>defect_is_zero<br/>filtration]
            PO[proof_obligation<br/>method: exact_fraction_arithmetic]
        end
        
        subgraph HashSection["Cryptographic Integrity"]
            HA[hash<br/>algorithm: SHA-256<br/>scope: certificate<br/>value: ...]
        end
        
        subgraph Audit["Audit (Not Hashed)"]
            AU[kernel_version]
            TS[timestamp]
            PL[platform]
        end
    end
```

## 3. Trust Architecture Layers

```mermaid
flowchart BT
    L4[Layer 4: Community Verification<br/>Distributed, Transparent]
    L3[Layer 3: Formal Bridge<br/>Future: Lean Export]
    L2[Layer 2: Independent Reproduction<br/>Docker, Open Source]
    L1[Layer 1: Exact Computation<br/>Python Fractions, No Float]
    L0[Layer 0: Human Statement<br/>Mathematical Rigor]
    
    L0 --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
```

## 4. Kaprekar System (3-digit)

```mermaid
flowchart LR
    subgraph Orbit["Orbit of 100"]
        100 --> 990
        990 --> 891
        891 --> 792
        792 --> 693
        693 --> 594
        594 --> 495
        495 --> 495
    end
    
    subgraph Fixed["Fixed Point"]
        FP[495<br/>954 - 459 = 495]
    end
    
    495 -.-> FP
```

## 5. Defect Operator Visualization

```mermaid
flowchart TD
    subgraph GoodPartition["Good Partition (D=0)"]
        A1[Block A: {1,2}] --> B1[Block B: {3,4}]
        A2[Block C: {5,6}] --> B2[Block C: {7,8}]
    end
    
    subgraph BadPartition["Bad Partition (D≠0)"]
        A3[Block X: {1,2}] --> B3[Block Y: {3,4}]
        A4[Block X: {5,6}] --> B4[Block Z: {7,8}]
    end
    
    GoodPartition -->|f maps blocks to blocks| Valid["VALID<br/>Koopman-invariant"]
    BadPartition -->|f splits across blocks| Invalid["INVALID<br/>Defect ≠ 0"]
```

## 6. Version Roadmap

```mermaid
timeline
    title AQARION Roadmap
    section Past
        v0.4.0 : Kernel foundation
               : Exact arithmetic
    section Current
        v0.4.1 : Registry hardened
               : Canonical cycles
               : Certificate schema 3.1
    section Near
        v0.4.2 : Schema locked
               : Reference artifact frozen
        v0.5.0 : 4-digit Kaprekar
               : 10,000 states
               : Sparse verification
    section Future
        v0.6.0 : KSD spectral certificates
        v1.0.0 : Formal verification platform
```

## 7. Community Engagement Flywheel

```mermaid
flowchart LR
    A[Mathematician<br/>States Claim] --> B[AQARION<br/>Generates Certificate]
    B --> C[Community<br/>Verifies Independently]
    C --> D[Confidence<br/>Accumulates]
    D --> E[New Claims<br/>Build on Verified Results]
    E --> A
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style D fill:#fce4ec
    style E fill:#f3e5f5
```

## 8. The "Missing Middle" Positioning

```mermaid
flowchart LR
    subgraph Heavy[Heavyweight Formalization]
        L[Lean]
        C[Coq]
        I[Isabelle]
    end
    
    subgraph AQARION[AQARION Zone]
        direction TB
        A1[Exact Arithmetic]
        A2[Machine-Auditable]
        A3[Reproducible]
        A4[Claim-Structured]
    end
    
    subgraph Light[Heuristic/Numerical]
        M[MATLAB]
        P[Python/R]
        N[NumPy]
    end
    
    Heavy -->|Months to formalize| AQARION
    Light -->|Minutes to write| AQARION
    AQARION -->|Same-day verification| Heavy
    AQARION -->|Cryptographic certainty| Light
```

## 9. Certificate Verification Sequence

```mermaid
sequenceDiagram
    participant User
    participant Cert as Certificate File
    participant Verifier as Independent Verifier
    participant Kernel as AQARION Kernel
    
    User->>Cert: Load certificate.json
    User->>Verifier: verify_certificate(cert)
    
    Verifier->>Verifier: Check hash integrity
    Verifier->>Verifier: Validate registry version
    Verifier->>Verifier: Verify dependency existence
    
    Verifier->>Kernel: Reconstruct FDDS
    Kernel-->>Verifier: System object
    
    Verifier->>Kernel: Recompute evidence
    Kernel-->>Verifier: Recomputed values
    
    Verifier->>Verifier: Compare claimed vs recomputed
    Verifier->>Verifier: Grant VALID or INVALID
    
    Verifier-->>User: Verification report
```

## 10. Sparse vs Dense Defect Check

```mermaid
flowchart TD
    subgraph Dense["Dense Defect Check<br/>O(|X|³)"]
        D1[Build K: Koopman matrix]
        D2[Build P: Projection matrix]
        D3[Compute D = (I-P)KP]
        D4[Check D = 0]
    end
    
    subgraph Sparse["Sparse Defect Check<br/>O(|X|)"]
        S1[For each block B]
        S2[Check f(B) ⊆ single block]
        S3[Return True/False]
    end
    
    Dense -->|Same result| Result["Partition is<br/>Koopman-invariant?"]
    Sparse -->|Same result| Result
    
    style Dense fill:#ffebee
    style Sparse fill:#e8f5e9
```
"""

with open(os.path.join(output_dir, "AQARION-MERMAID.md"), 'w') as f:
    f.write(mermaid)

print("✅ AQARION-MERMAID.md")
