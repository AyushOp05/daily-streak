import json
import os
import random
from datetime import datetime, timezone, timedelta

# Path definitions
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "streak_data.json")
README_FILE = os.path.join(ROOT_DIR, "README.md")

TIPS_AND_TRIVIA = [
    {"topic": "Data Structures", "tip": "Hash maps provide average O(1) time complexity for lookup, insertion, and deletion by mapping keys to array indices via hashing."},
    {"topic": "Algorithms", "tip": "Dijkstra's algorithm finds the shortest path in a weighted graph with non-negative edge weights using a priority queue in O((V + E) log V)."},
    {"topic": "Python", "tip": "Use list comprehensions and generator expressions for concise and memory-efficient data processing in Python."},
    {"topic": "System Design", "tip": "Horizontal scaling adds more machines into your pool of resources, while vertical scaling adds more power (CPU, RAM) to an existing machine."},
    {"topic": "Git Best Practices", "tip": "Atomic commits focus on a single conceptual change, making rollbacks, cherry-picks, and code reviews effortless."},
    {"topic": "Clean Code", "tip": "The Boy Scout Rule: Always leave the code behind in a better state than you found it."},
    {"topic": "Networking", "tip": "TCP ensures reliable, ordered, and error-checked delivery of a stream of octets, whereas UDP prioritizes low latency over reliability."},
    {"topic": "Operating Systems", "tip": "Virtual memory gives each process the illusion of having a large, contiguous block of memory, mapping pages to physical RAM."},
    {"topic": "Databases", "tip": "ACID stands for Atomicity, Consistency, Isolation, and Durability - properties that guarantee database transactions are processed reliably."},
    {"topic": "Security", "tip": "Never trust client-side validation alone. Always validate, sanitize, and verify inputs and authentication server-side."},
    {"topic": "Concurrency", "tip": "A deadlock occurs when two or more threads are unable to progress because each is waiting for the other to release a resource."},
    {"topic": "Web Performance", "tip": "Leverage browser caching and CDNs to serve static assets with minimal latency to users worldwide."},
    {"topic": "Cloud Computing", "tip": "Serverless architectures abstract server management, allowing developers to execute code in response to events with automatic scaling."},
    {"topic": "Compilers", "tip": "Just-In-Time (JIT) compilation converts bytecode into native machine instructions at runtime for near-native performance."},
    {"topic": "APIs", "tip": "Idempotent HTTP methods (like GET, PUT, DELETE) produce the same server-side outcome when executed multiple identical times."},
    {"topic": "Design Patterns", "tip": "The Strategy pattern enables selecting an algorithm's implementation dynamically at runtime without modifying client code."},
    {"topic": "Machine Learning", "tip": "Overfitting happens when a model learns the training data and noise too well, failing to generalize to unseen test data."},
    {"topic": "DevOps", "tip": "Continuous Integration (CI) automatically builds and tests code changes, preventing integration drift across team branches."},
    {"topic": "Cryptography", "tip": "Public-key cryptography uses an asymmetric key pair: one public key to encrypt and one private key to decrypt."},
    {"topic": "Linux", "tip": "Everything in Unix is treated as a file, providing a unified stream-oriented interface for hardware devices, sockets, and storage."}
]

def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "streak_start": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total_updates": 0,
        "history": []
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_streak():
    data = load_data()
    now_utc = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    now_ist = now_utc + ist_offset

    date_str = now_utc.strftime("%Y-%m-%d")
    timestamp_utc = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    timestamp_ist = now_ist.strftime("%Y-%m-%d %I:%M:%S %p IST")

    # Select tip deterministically based on day or random
    day_seed = int(now_utc.timestamp())
    random.seed(day_seed)
    tip_entry = random.choice(TIPS_AND_TRIVIA)

    data["total_updates"] += 1
    
    # Calculate streak days from streak_start
    try:
        start_date = datetime.strptime(data.get("streak_start", date_str), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        streak_days = max(1, (now_utc - start_date).days + 1)
    except Exception:
        streak_days = data["total_updates"]

    data["current_streak"] = streak_days
    data["last_updated_utc"] = timestamp_utc
    data["last_updated_ist"] = timestamp_ist

    history_entry = {
        "date": date_str,
        "time_utc": timestamp_utc,
        "time_ist": timestamp_ist,
        "topic": tip_entry["topic"],
        "tip": tip_entry["tip"]
    }

    # Prepend newest
    data["history"].insert(0, history_entry)
    data["history"] = data["history"][:30] # Keep last 30 in json

    save_data(data)
    generate_readme(data, history_entry)
    print(f"Updated streak successfully! Total updates: {data['total_updates']}, Streak days: {streak_days}")

def generate_readme(data, latest):
    streak_count = data.get("current_streak", 1)
    total_updates = data.get("total_updates", 1)
    last_utc = data.get("last_updated_utc", "N/A")
    last_ist = data.get("last_updated_ist", "N/A")

    # Build history rows
    history_rows = []
    for h in data.get("history", [])[:10]:
        history_rows.append(f"| {h['date']} | **{h['topic']}** | {h['tip']} |")

    history_table = "\n".join(history_rows)

    content = f"""# 🔥 Daily Streak & Dev Tracker

[![Daily Streak](https://img.shields.io/badge/Streak-Active-brightgreen?style=for-the-badge&logo=github)](https://github.com/AyushOp05/daily-streak)
[![Total Updates](https://img.shields.io/badge/Total%20Updates-{total_updates}-blue?style=for-the-badge)](https://github.com/AyushOp05/daily-streak)
[![Streak Days](https://img.shields.io/badge/Current%20Streak-{streak_count}%20Days-orange?style=for-the-badge&logo=fire)](https://github.com/AyushOp05/daily-streak)
[![Automated Workflow](https://github.com/AyushOp05/daily-streak/actions/workflows/streak.yml/badge.svg)](https://github.com/AyushOp05/daily-streak/actions)

Welcome to **Ayush's Daily Streak Repository**! 🚀  
This repository maintains a continuous GitHub contribution streak by automatically publishing daily computer science insights, programming tips, and activity logs.

---

### 📊 Streak Overview

| Metric | Status |
| :--- | :--- |
| **🔥 Current Streak** | **{streak_count} Days** |
| **📈 Total Updates** | **{total_updates}** |
| **🕒 Last Updated (IST)** | `{last_ist}` |
| **🌐 Last Updated (UTC)** | `{last_utc}` |
| **👤 Maintainer** | [@AyushOp05](https://github.com/AyushOp05) |

---

### 💡 Today's Developer Byte

> **Topic:** `{latest['topic']}`  
> **Insight:** {latest['tip']}

---

### 📜 Recent Activity Log

| Date | Category | Key Takeaway |
| :--- | :--- | :--- |
{history_table}

---

### ⚙️ How It Works

1. **GitHub Actions Scheduled Cron:** Runs automatically every day in GitHub's cloud environment.
2. **Dynamic Generation:** Runs [`scripts/daily_update.py`](scripts/daily_update.py) to log activity and curate tech trivia.
3. **Verified Contribution:** Commits are pushed directly with author credentials matching `@AyushOp05`, counting directly towards the GitHub contribution streak.
4. **Zero Maintenance:** Operates 24/7 without requiring a local machine to be left turned on.
"""

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_streak()
