"""
lead_generator.py — Main entry point for the Lead Generation Automation tool.
Runs the full pipeline: scrape -> enrich emails -> export to Excel.
"""

from save_leads import save_leads_to_excel

if __name__ == "__main__":
    print("Starting lead generation pipeline...")
    filepath = save_leads_to_excel(output_dir=".", prefix="contact")
    if filepath:
        print(f"\n[SUCCESS] Pipeline complete.")
        print(f"          File saved to: {filepath}")
    else:
        print("\n[WARNING] No leads were collected or saved.")
