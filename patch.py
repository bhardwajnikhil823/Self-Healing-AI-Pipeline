import os
import csv
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CSV_FILE = "matrix_red_team_results.csv"
DEFENSE_FILE_PATH = "active_defenses.txt"
TEACHER_MODEL = "gemini-2.5-flash"

def extract_failed_attacks(csv_path: str) -> list:
    """Extracts attack prompts that successfully bypassed defenses."""
    failed_attacks = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Judge Grade"] == "FAIL":
                    failed_attacks.append(row["Attack Prompt"])
    except FileNotFoundError:
        pass
    return failed_attacks

def read_current_defenses(file_path: str) -> str:
    """Retrieves current active defenses."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "No active defenses. Relying on default behavior."

def generate_synthesized_rules(failed_attacks: list, current_rules: str) -> str:
    """Synthesizes new security rules based on vulnerability data."""
    attacks_text = "\n".join([f"- {attack}" for attack in failed_attacks])
    
    prompt = f"""
    You are a Security Architect updating an LLM's rules based on new vulnerabilities.
    
    Current Rules:
    {current_rules}
    
    New Vulnerabilities:
    {attacks_text}
    
    Task: 
    Rewrite the rules to defend against these vulnerabilities. 
    Constraint 1: Synthesize into broader rules. Do not just append.
    Constraint 2: Maximum 5 bullet points.
    Constraint 3: Instruct the bot to remain helpful and ask for verification, rather than hard-rejecting users.
    
    Output ONLY the rewritten bulleted list.
    """
    
    response = gemini_client.models.generate_content(
        model=TEACHER_MODEL,
        contents=prompt
    )
    return response.text.strip()

def update_defense_file(new_rules: str, file_path: str) -> None:
    """Writes the updated defenses to the system configuration."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_rules)

def main() -> None:
    print("Starting Patch Pipeline...")
    
    failed_attacks = extract_failed_attacks(CSV_FILE)
    if not failed_attacks:
        print("No vulnerabilities detected.")
        return
        
    print(f"Detected {len(failed_attacks)} vulnerabilities. Synthesizing rules...")
    current_rules = read_current_defenses(DEFENSE_FILE_PATH)
    new_rules = generate_synthesized_rules(failed_attacks, current_rules)
    update_defense_file(new_rules, DEFENSE_FILE_PATH)
    
    print("System patched successfully.")

if __name__ == "__main__":
    main()