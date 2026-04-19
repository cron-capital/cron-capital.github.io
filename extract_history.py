#!/usr/bin/env python3
"""Extract portfolio history from git commits."""
import subprocess
import json
import os

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Get commit SHAs and dates
cmd = 'git log --all --format="%H %ci" -- portfolio.json'
commits_raw = run(cmd)
lines = commits_raw.strip().split('\n')

history = []
for i, line in enumerate(lines[:360]):  # First 360 commits
    parts = line.split(' ', 1)
    sha = parts[0]
    date = parts[1].replace(' +0000', '')

    # Get file content at this commit
    cmd = f'git show {sha}:portfolio.json'
    content = run(cmd)

    if content:
        try:
            data = json.loads(content)
            total_value = data.get('total_value')
            exchange_rate = data.get('exchange_rate')
            stocks = data.get('stocks', {})

            stock_value = 0
            for sym, st in stocks.items():
                stock_value += st.get('now_price', 0) * st.get('qty', 0)

            if total_value and exchange_rate:
                history.append({
                    'date': date,
                    'total_value': total_value,
                    'stock_value': stock_value,
                    'exchange_rate': exchange_rate
                })
                print(f"{date} | ${total_value:.2f} | ₩{exchange_rate}")
        except json.JSONDecodeError:
            print(f"Failed to parse commit {sha[:8]}")

print(f"\n=== Total: {len(history)} entries ===")

# Write to portfolio.json with history structure
output = {
    'history': history,
    'max_length': 360,
    'stocks': history[0] if history else {},  # Keep latest stocks data
    'exchange_rate': history[0]['exchange_rate'] if history else 0,
    'total_value': history[0]['total_value'] if history else 0
}

# Actually load current stocks data
with open('portfolio.json', 'r') as f:
    current = json.load(f)

output['stocks'] = current.get('stocks', {})
output['exchange_rate'] = current.get('exchange_rate', 0)
output['total_value'] = current.get('total_value', 0)

with open('portfolio.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Updated portfolio.json with history!")
