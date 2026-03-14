# Contributing to Nirixa OS

Thank you for your interest in contributing to **Nirixa OS**! We are building an open-source, local-first personal AI operating system framework for engineers, founders, and system architects.

---

## 🛠️ How to Contribute

### 1. Reporting Bugs & Feature Requests
- Check open GitHub Issues before submitting a new one.
- Provide clear reproduction steps, environment details (OS, Python version), and log outputs.

### 2. Developing & Submitting Code
1. **Fork the Repository**: Create a personal fork on GitHub.
2. **Clone & Set Up**:
   ```bash
   git clone https://github.com/your-username/Nirixa.git
   cd Nirixa
   python system/scripts/setup.py
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Run Automated System Health Evals**:
   Before submitting your PR, make sure all Track A automated system health regression tests pass:
   ```bash
   python system/engine/evals/run_system_evals.py
   ```
5. **Submit a Pull Request**: Push your branch and open a PR against `main` with a clear description of the problem solved.

---

## 📐 System Operating Axioms

When writing code or adding engine capabilities to Nirixa OS, always adhere to our core design axioms:

- **Local-First Security**: Never write user databases, credentials, or private notes outside local disk or air-gapped repositories.
- **Rule 1 (Dialogue-First Boundary)**: AI reasoning suggests drafts as `status='draft'`; raw thoughts are never auto-published without explicit human approval.
- **Rule 7 (High-Signal Copywriting)**: AI outputs must adhere to Naval Ravikant & Aviral Bhatnagar copywriting standards (zero hype marketing, zero tacky emojis `🔴, 🟢, 🔥, 🚀, 👈, 👇`).

---

## 📄 License
By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
