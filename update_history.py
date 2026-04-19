#!/usr/bin/env python3
import json
import sys
from datetime import datetime

MAX_LENGTH = 360


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_history.py '<json_data>'")
        sys.exit(1)

    new_data = json.loads(sys.argv[1])

    with open("portfolio.json", "r") as f:
        data = json.load(f)

    history = data.get("history", [])

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_value": new_data.get("total_value"),
        "exchange_rate": new_data.get("exchange_rate"),
    }
    history.insert(0, entry)

    if len(history) > MAX_LENGTH:
        history = history[:MAX_LENGTH]

    data["history"] = history
    data["max_length"] = MAX_LENGTH

    with open("portfolio.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Updated history: {len(history)} entries")


if __name__ == "__main__":
    main()
