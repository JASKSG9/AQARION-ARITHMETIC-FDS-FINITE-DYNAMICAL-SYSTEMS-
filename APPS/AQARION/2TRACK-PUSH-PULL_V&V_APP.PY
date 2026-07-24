import gradio as gr
import numpy as np
import json
import hashlib
from collections import defaultdict
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# ---------- Core AQARION Algorithms (Two‑Track) ----------
def refine_forward(T):
    n = len(T)
    part = [0] * n
    history = [list(part)]
    while True:
        blocks = defaultdict(list)
        for i, b in enumerate(part):
            blocks[b].append(i)
        new = [None] * n
        nid = 0
        for b in sorted(blocks):
            groups = defaultdict(list)
            for s in blocks[b]:
                groups[part[T[s]]].append(s)
            for g in groups.values():
                for s in g:
                    new[s] = nid
                nid += 1
        if new == part:
            break
        part = new
        history.append(list(part))
    return part, history

def refine_bisim(T):
    n = len(T)
    pre = [[] for _ in range(n)]
    for i, ti in enumerate(T):
        pre[ti].append(i)
    part = [0] * n
    history = [list(part)]
    while True:
        blocks = defaultdict(list)
        for i, b in enumerate(part):
            blocks[b].append(i)
        blist = sorted(blocks)
        new = [None] * n
        nid = 0
        for bid in blist:
            groups = defaultdict(list)
            for s in blocks[bid]:
                img = part[T[s]]
                # preimage counts per block of current partition
                pc = tuple(len([p for p in pre[s] if part[p] == b]) for b in blist)
                groups[(img, pc)].append(s)
            for g in groups.values():
                for s in g:
                    new[s] = nid
                nid += 1
        if new == part:
            break
        part = new
        history.append(list(part))
    return part, history

def build_P(partition):
    n = len(partition)
    P = np.zeros((n, n))
    blocks = defaultdict(list)
    for i, b in enumerate(partition):
        blocks[b].append(i)
    for block in blocks.values():
        m = len(block)
        for i in block:
            for j in block:
                P[i, j] = 1.0 / m
    return P

def defect_operators(T, partition):
    n = len(T)
    P = build_P(partition)
    U = np.zeros((n, n))
    for i in range(n):
        U[i, T[i]] = 1
    D_F = (np.eye(n) - P) @ U @ P
    D_B = P @ U @ (np.eye(n) - P)
    return D_F, D_B

def principal_angle_sin(T, partition):
    D_F, _ = defect_operators(T, partition)
    return float(np.linalg.norm(D_F, 2))

# ---------- Visualization ----------
def plot_partition(partition, T):
    """Simple scatter of states colored by block."""
    n = len(partition)
    # We can't really draw a graph easily, but we can show a colormap.
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.imshow([partition], aspect='auto', cmap='tab20')
    ax.set_yticks([])
    ax.set_xlabel('State index')
    ax.set_title('Partition (colors = blocks)')
    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# ---------- Main Gradio Interface ----------
def process_graph(json_input):
    try:
        T = json.loads(json_input)
        if not isinstance(T, list) or any(not isinstance(x, int) for x in T):
            return "Invalid input: must be a JSON list of integers.", None, None, None, None, None
        n = len(T)
        if any(t < 0 or t >= n for t in T):
            return "Invalid transition: indices must be 0..n-1.", None, None, None, None, None
    except Exception as e:
        return f"JSON parse error: {str(e)}", None, None, None, None, None

    # Compute both tracks
    part_F, hist_F = refine_forward(T)
    part_B, hist_B = refine_bisim(T)

    Df, Db = defect_operators(T, part_F)
    Df_norm = float(np.linalg.norm(Df, 2))
    Db_norm = float(np.linalg.norm(Db, 2))

    DfB, DbB = defect_operators(T, part_B)
    DfB_norm = float(np.linalg.norm(DfB, 2))
    DbB_norm = float(np.linalg.norm(DbB, 2))

    # Principal angle
    theta_sin = principal_angle_sin(T, part_F)

    # Output text
    summary = f"""
**Track F (coarsest forward-invariant):**
- Partition: {part_F}
- Number of blocks: {len(set(part_F))}
- ‖D_F‖₂ = {Df_norm:.2e}
- ‖D_B‖₂ = {Db_norm:.2e}

**Track B (coarsest bisimulation):**
- Partition: {part_B}
- Number of blocks: {len(set(part_B))}
- ‖D_F‖₂ = {DfB_norm:.2e}
- ‖D_B‖₂ = {DbB_norm:.2e}

**Principal angle (Shah & Cortés 2026):**
- sin(θ_max) = ‖D_F‖₂ = {theta_sin:.3e}
- (Equivalence: defect norm = geometric misalignment)

**Refinement history (Track F):**
- Steps: {len(hist_F)}
- Final forward-invariant: {'Yes' if Df_norm < 1e-9 else 'No'}
"""

    # Generate certificate
    cert = {
        "input_T": T,
        "Track_F_partition": part_F,
        "Track_B_partition": part_B,
        "D_F_norm": Df_norm,
        "D_B_norm": Db_norm,
        "principal_angle_sin": theta_sin,
        "algorithm": "AQARION v20.6"
    }
    cert_json = json.dumps(cert, indent=2)
    cert_hash = hashlib.sha256(cert_json.encode()).hexdigest()[:16]

    # Plot partition visualization (for Track F)
    img_base64 = plot_partition(part_F, T)

    # Build RO-Crate snippet
    ro_crate = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [{
            "@id": "./",
            "@type": "Dataset",
            "name": f"AQARION certificate {cert_hash}",
            "hasPart": [{"@id": "certificate.json"}]
        }, {
            "@id": "certificate.json",
            "@type": "File",
            "encodingFormat": "application/json",
            "sha256": cert_hash
        }]
    }
    ro_json = json.dumps(ro_crate, indent=2)

    return summary, cert_json, ro_json, f'<img src="data:image/png;base64,{img_base64}"/>'

# ---------- UI ----------
with gr.Blocks(title="AQARION Playground") as demo:
    gr.Markdown("# ♾️ AQARION Playground — Interactive Observable Quotient Certification")
    gr.Markdown("Enter a functional graph as a JSON list of transitions (e.g., `[2, 2, 2]` for 3 states).")
    gr.Markdown("The app computes the **coarsest forward‑invariant partition** and the **coarsest bisimulation**, shows the defect operators, principal angle, and exports a certificate.")
    gr.Markdown("*Run entirely on Hugging Face / Replit — no installation, free for all.*")

    with gr.Row():
        inp = gr.Textbox(label="Transition list (JSON)", placeholder='[2,2,2]', lines=2)
        btn = gr.Button("Compute Quotient", variant="primary")

    with gr.Row():
        summary = gr.Markdown()
    with gr.Row():
        cert_out = gr.Textbox(label="Certificate JSON", lines=6)
        ro_out = gr.Textbox(label="RO-Crate Metadata", lines=6)
    with gr.Row():
        plot_out = gr.HTML()

    btn.click(fn=process_graph, inputs=inp, outputs=[summary, cert_out, ro_out, plot_out])

demo.launch()
