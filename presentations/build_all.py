import subprocess
import sys
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scripts = [
        "builder_pptx.py",
        "builder_pdf.py",
        "builder_docs.py"
    ]
    print("=" * 60)
    print("NEXTGEN AI — PRESENTATION SUITE GENERATOR")
    print("=" * 60)
    for s in scripts:
        script_path = os.path.join(base_dir, s)
        print(f"Running {s}...")
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error in {s}:\n{res.stderr}")
            sys.exit(1)
        else:
            print(res.stdout.strip())
    print("=" * 60)
    print("All 6 presentation deliverables have been successfully generated!")
    print("=" * 60)

if __name__ == "__main__":
    main()
