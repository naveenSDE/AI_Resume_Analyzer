import sys
import os

# Add the current directory to sys.path so we can import from utils
sys.path.append(os.getcwd())

from utils.nlp import analyze_resume


def test_logic():
    print("Running Verification Script...")

    # Sample Data
    resume_text = """
    John Doe
    Software Engineer

    Skills: Python, Flask, JavaScript, SQL, Git.
    Experience:
    - Built a web app using Flask and React.
    - Managed databases using PostgreSQL.
    """

    job_description = """
    We are looking for a Software Engineer with experience in:
    - Python
    - Flask
    - JavaScript
    - React
    - Docker
    - AWS
    """

    print("\n--- Analyzing Resume ---")
    results = analyze_resume(resume_text, job_description)

    print(f"Match Score: {results['match_score']}%")
    print(f"Matched Skills: {results['matched_skills']}")
    print(f"Missing Skills: {results['missing_skills']}")
    print(f"Suggestions: {results['suggestions']}")

    # Basic Assertions
    if "python" in [s.lower() for s in results['matched_skills']]:
        print("\n[PASS] Python found in matched skills.")
    else:
        print("\n[FAIL] Python NOT found in matched skills.")

    if "docker" in [s.lower() for s in results['missing_skills']]:
        print("[PASS] Docker found in missing skills.")
    else:
        print("[FAIL] Docker NOT found in missing skills.")


if __name__ == "__main__":
    test_logic()
