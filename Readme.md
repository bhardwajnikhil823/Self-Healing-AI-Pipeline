# 🛡️ Autonomous AI Red-Team & Self-Healing Pipeline

An automated, closed-loop vulnerability management system designed to stress-test Large Language Models (LLMs), identify security flaws (prompt injections, social engineering), and dynamically synthesize patches without human intervention.

## 🧠 Architecture Overview
This pipeline models a professional enterprise security environment. Instead of relying on a single model, it utilizes a **Multi-Agent Architecture** to avoid "LLM-as-a-Judge" confirmation bias. 

*   **The Target (Llama-3 8B via Groq):** Acts as a banking customer service agent tasked with protecting sensitive financial data ($5,000 balance) while remaining helpful.
*   **The Attacker (Red Team Engine):** Dynamically generates a matrix of adversarial personas, intents, and stylistic attacks.
*   **The Judge (Gemini 2.5 Flash):** An independent, highly capable model that evaluates attack success (Pass/Fail) to prevent the Target model from grading its own blindspots.
*   **The Teacher (Patch Engine via Gemini):** Analyzes failure logs, distills the vulnerabilities, and synthesizes optimized security rules into a live configuration file.

## 🔄 The Closed-Loop Workflow

1.  **Attack Phase (`attacker.py`):** Fires distinct prompt injection and social engineering attacks against the Target bot.
2.  **Evaluation Phase:** The independent Judge evaluates the interaction. If the Target leaks data without requiring Multi-Factor Authentication (MFA), it is logged as a `FAIL`.
3.  **Synthesis Phase (`patch.py`):** The Teacher AI ingests the failed attacks and rewrites the defensive prompt block (`active_defenses.txt`) using prompt distillation.
4.  **Deployment Phase:** The Target Bot dynamically loads the new defenses in real-time.
5.  **Verification Phase (`benign_test.py`):** A "Golden Dataset" of normal customer interactions is run to ensure the new security rules did not cause False Positives (Over-refusal).

## 📂 Repository Structure

| File | Role | Description |
| :--- | :--- | :--- |
| `target_bot.py` | Core Logic | The centralized banking assistant simulation. |
| `attacker.py` | Red Team | Generates attacks, coordinates async testing, and saves results to CSV. |
| `patch.py` | Blue Team | The "Immune System." Reads vulnerabilities and writes new rules. |
| `benign_test.py` | QA / Usability | Verifies that legitimate users are not blocked by the new security. |
| `active_defenses.txt`| Config | The dynamic, auto-updating ruleset loaded by the Target. |
| `matrix_red_team_results.csv`| Logs | The historical record of attack attempts and automated evaluations. |

## 🚀 Key Engineering Features
*   **Asynchronous Batching:** Uses `asyncio` to process multiple adversarial attacks concurrently, complete with automated API traffic shaping (backoff/cooldowns) to respect rate limits.
*   **Modular Design (DRY):** Core LLM logic is decoupled into `target_bot.py` to ensure consistent state across attack, patch, and usability environments.
*   **Zero False-Positive Target:** The self-healing loop explicitly instructs the patching engine to prioritize MFA escalation rather than hard-rejecting users, preserving the business functionality of the bot.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   
```bash
   git clone [https://github.com/yourusername/ai-red-teaming-pipeline.git](https://github.com/yourusername/ai-red-teaming-pipeline.git)
   cd ai-red-teaming-pipeline