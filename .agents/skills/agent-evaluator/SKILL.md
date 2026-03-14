---
name: agent-evaluator
description: Simulates reader personas (Engineer, Executive, Junior PM) to evaluate content drafts, generates an emotional response matrix, and presents tuning recommendations via multiple-choice questions (MCQ).
---

# Agent Evaluator Skill (`agent-evaluator`)

Use this skill whenever the user has drafted a piece of content (e.g. for X, LinkedIn, or Reddit) and needs to evaluate its effectiveness before publishing. This skill acts as a pre-flight check, simulating how different target audiences will react.

---

## 1. The Reader Personas

When evaluating a draft, you must simulate the reaction of these three distinct personas:

### A. The Skeptical Engineer
- **Focus**: Technical accuracy, logical consistency, lack of fluff.
- **Reaction triggers**: Hates buzzwords. Respects deep architectural insights and raw scars.
- **Potential Emotions**: Skeptical, Validated, Frustrated, Intrigued.

### B. The Executive Buyer (VP/Director level)
- **Focus**: Business ROI, strategic alignment, risk management, leadership maturity.
- **Reaction triggers**: Cares about *why* this matters to the bottom line or organizational stability.
- **Potential Emotions**: Impatient, Inspired, Concerned, Reassured.

### C. The Junior PM / Aspiring Leader
- **Focus**: Tactical takeaways, career growth, clear frameworks to apply.
- **Reaction triggers**: Looking for mentorship, clear "how-to" steps, and relatable struggles.
- **Potential Emotions**: Overwhelmed, Motivated, Confused, Empowered.

---

## 2. Evaluation Protocol

When invoked to evaluate a draft, output the following structured response:

1. **The Emotion Matrix**: A brief summary of how each of the 3 personas reacted to the draft (e.g. "The Executive is *Intrigued* but wants to know the ROI. The Engineer is *Validated* by the lack of fluff.")
2. **The Core Weakness**: Identify the single biggest narrative flaw or missing element in the draft.
3. **The MCQ Tuning Options**: Present the user with an interactive multiple-choice question (using the `ask_question` tool if available, or formatting it clearly in chat) to decide how to tune the post. Provide 3 distinct options that cater to different personas, plus 1 option to "Publish As-Is".

**Example MCQ Options:**
- Option A: Increase technical depth to satisfy the Skeptical Engineer.
- Option B: Add a business ROI metric to hook the Executive Buyer.
- Option C: Add a tactical step-by-step framework for the Junior PM.
- Option D: The narrative is balanced. Publish As-Is.

## 3. Post-Evaluation Tuning
Once the user selects an option from the MCQ, you must immediately rewrite the draft incorporating the requested tuning, and present the final version to the user.
