# AQARION Daily Equation Challenge
# Replit-compatible prototype

from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('/mnt/agents/workspace')
from aqarion_core import kaprekar_map, zeckendorf_encode, nega_fib_encode, gap_observable

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('challenge.html')

@app.route('/api/step', methods=['POST'])
def kaprekar_step():
    data = request.get_json()
    n = int(data.get('number', 6174))
    if n < 0 or n > 9999:
        return jsonify({'error': 'Must be 0-9999'})
    
    result = kaprekar_map(n)
    
    return jsonify({
        'input': n,
        'output': result,
        'gap': gap_observable(result),
        'depth': 0,  # To be computed
        'zeckendorf': zeckendorf_encode(result),
        'nega_fib': nega_fib_encode(result),
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# api/heatmap.py
import numpy as np
from collections import defaultdict

def kaprekar_depth(n):
    """Return number of steps to reach 6174, or -1 for repdigit null."""
    if len(set(str(n).zfill(4))) == 1:
        return -1
    visited = {}
    x = n
    steps = 0
    while x not in visited:
        if x == 6174:
            return steps
        visited[x] = steps
        s = str(x).zfill(4)
        desc = int(''.join(sorted(s, reverse=True)))
        asc = int(''.join(sorted(s)))
        x = desc - asc
        steps += 1
    return -1  # should not happen for non-repdigits

def compute_heatmap():
    grid = [[0]*100 for _ in range(100)]
    depths = []
    nulls = 0
    for n in range(10000):
        d = kaprekar_depth(n)
        row = n // 100
        col = n % 100
        grid[row][col] = d
        if d == -1:
            nulls += 1
        else:
            depths.append(d)
    return {
        "grid": grid,
        "stats": {
            "max": max(depths) if depths else 0,
            "converged": len(depths),
            "nulls": nulls,
            "mean": np.mean(depths) if depths else 0,
            "histogram": dict(Counter(depths))
        }
