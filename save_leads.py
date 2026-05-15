import pandas as pd
from scraper import collect_leads
from email_guesser import enrich_leads_with_emails
from datetime import datetime
import os


def save_leads_to_excel(output_dir: str = ".", prefix: str = "contact") -> str:
    """
    Collects leads, enriches them with guessed emails, deduplicates,
    and saves to a timestamped Excel file.

    Args:
        output_dir: Directory to save the Excel file.
        prefix:     Email prefix for guessing (contact/info/hello/support/sales).

    Returns:
        Full path to the saved .xlsx file, or empty string on failure.
    """
    print("Collecting leads...")
    leads = collect_leads()

    if not leads:
        print("No leads collected. Exiting.")
        return ""

    print(f"Collected {len(leads)} leads. Enriching emails...")
    leads = enrich_leads_with_emails(leads, prefix=prefix)

    # Build DataFrame with a clean column order
    df = pd.DataFrame(leads, columns=[
        "name", "email", "email_alternatives", "website", "domain", "location", "category"
    ])

    # Flatten alternatives list to a readable string
    df["email_alternatives"] = df["email_alternatives"].apply(
        lambda alts: " | ".join(alts) if isinstance(alts, list) else ""
    )

    # Drop duplicates on name + location
    df.drop_duplicates(subset=["name", "location"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Timestamp the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"leads_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)

    # Write to Excel with auto-sized columns and frozen header
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Leads")

        worksheet = writer.sheets["Leads"]

        # Freeze the header row
        worksheet.freeze_panes = "A2"

        # Auto-adjust column widths
        for col in worksheet.columns:
            max_length = max(
                (len(str(cell.value)) if cell.value else 0) for cell in col
            )
            worksheet.column_dimensions[col[0].column_letter].width = min(max_length + 4, 65)

    print(f"Saved {len(df)} unique leads -> {filepath}")
    return filepath


if __name__ == "__main__":
    save_leads_to_excel()
