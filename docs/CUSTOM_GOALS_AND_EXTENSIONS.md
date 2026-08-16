# Custom Goals, Milestones & Persona Extensibility in Nirixa OS

Nirixa OS is designed to be completely user-programmable. You can define your own **life milestones**, **custom persona boards**, and **original thought assets (OTAs)** without writing complex boilerplate.

---

## 1. Defining Your Own Goals & Milestones

Nirixa OS stores your life goals and strategic milestones in `system/data/nirixa.db` under the `life_milestones` and `system_goals` tables.

### Option A: Via Python API
You can register new goals directly in Python:

```python
import sqlite3

def add_user_goal(milestone, target_year, category, notes=""):
conn = sqlite3.connect("system/data/nirixa.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS life_milestones (
id INTEGER PRIMARY KEY AUTOINCREMENT,
milestone TEXT,
target_year INTEGER,
category TEXT,
notes TEXT
)
""")
c.execute("""
INSERT INTO life_milestones (milestone, target_year, category, notes)
VALUES (?, ?, ?, ?)
""", (milestone, target_year, category, notes))
conn.commit()
conn.close()
print(f" Goal registered: '{milestone}' (Target: {target_year})")

# Example: Define your own targets
add_user_goal("Deliver Global Keynote / TED Talk on AI", 2029, "Keynote & Impact")
add_user_goal("Publish Living Knowledge Graph & Book", 2028, "Publication")
add_user_goal("Launch Independent AI Research Lab", 2030, "Enterprise")
```

### Option B: Via Local Dashboard UI
1. Open the local dashboard: `http://localhost:8000`.
2. Under the **System Goals & Milestones** panel, view active timelines and add new milestone targets.

---

## 2. Defining Your Own Custom Persona Advisory Board

Nirixa OS includes an adversarial multi-perspective sparring engine (`.agents/skills/persona-advisory-board/`). You can customize the simulated mentors who challenge your raw thoughts.

### How to Add a New Persona
Edit `.agents/skills/persona-advisory-board/SKILL.md` and add your custom thinker:

```markdown
### 4. Paul Graham (First-Principles Startup & Writing Lens)
- **Focus**: Relentlessly clear writing, doing things that don't scale, making things people want, avoiding intellectual pretension.
- **Tone**: Conversational, philosophical, razor-sharp essayist style.
- **Key Questions**:
- *"Are you making this complicated to sound smart, or is it fundamentally simple?"*
- *"What is the counter-intuitive truth that nobody agrees with you on?"*
- *"What would this look like if it were easy?"*
```

---

## 3. Creating Custom Original Thought Assets (OTAs)

Every genuine insight you develop can be tracked as an **OTA** with its own ID, hypothesis, and lineage ancestry:

```python
import sqlite3

def register_ota(ota_id, title, hypothesis, category):
conn = sqlite3.connect("system/data/nirixa.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS ota_registry (
ota_id TEXT PRIMARY KEY,
title TEXT,
hypothesis TEXT,
category TEXT,
status TEXT,
created_at TEXT
)
""")
c.execute("""
INSERT OR REPLACE INTO ota_registry (ota_id, title, hypothesis, category, status, created_at)
VALUES (?, ?, ?, ?, 'Active Research', datetime('now'))
""", (ota_id, title, hypothesis, category))
conn.commit()
conn.close()
print(f" Registered OTA: {ota_id} - {title}")

# Example: Register your custom breakthrough
register_ota(
"OTA-101",
"Selective Attention in Distributed Systems",
"Agent coordination overhead scales quadratically unless attention is strictly gated by domain boundaries.",
"Distributed Cognition"
)
```

---

## 4. The 3-Stage Distillation Pipeline

Whenever you capture a raw thought via Telegram:
1. **Buffer**: The 8s debouncer groups rapid thoughts.
2. **Sparring**: The Chief of Staff asks 2 probing questions to test assumptions against your **Goals** and active **OTAs**.
3. **Crystallization**: Refined assets are automatically linked to your career dashboard and saved into `inbox/YYYY-MM-mobile-inbox.md`.
