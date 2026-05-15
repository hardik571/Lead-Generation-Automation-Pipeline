# Lead Generation Automation Pipeline

> An automated Python pipeline that scrapes web data, extracts B2B leads, and schedules formatted Excel report generation.

---

## Project Description

This project automates the process of collecting B2B leads from a public
business directory (YellowPages.ca). It extracts structured data — business
name, location, category, and website — then uses regex-based domain parsing
to generate likely contact email addresses (e.g. `contact@company.com`).
Results are exported to a clean, formatted Excel file, and the tool can be
scheduled to run automatically every day at 08:00.

---

## Tools & Libraries Used

| Library | Purpose |
|---|---|
| `requests` | Sends HTTP GET requests to fetch web pages |
| `BeautifulSoup4` | Parses raw HTML and extracts structured data |
| `pandas` | Organises lead data into a DataFrame for easy manipulation |
| `openpyxl` | Writes the DataFrame to a formatted `.xlsx` Excel file |
| `schedule` | Schedules the pipeline to run automatically at a set time |

---

## Project Structure

```
lead_gen_automation/
├── venv/                  # Virtual environment (not committed)
├── requirements.txt       # All dependencies
├── scraper.py             # collect_leads()         — scrapes business listings
├── email_guesser.py       # generate_email()        — extracts domain, guesses emails
├── save_leads.py          # save_leads_to_excel()   — deduplicates & exports
├── scheduler.py           # start_scheduler()       — daily job runner
├── lead_generator.py      # Entry point             — run this to start the pipeline
└── README.md              # Project documentation
```

---

## Installation

> ⚠️ Always use the **virtual environment Python**, not the system Python.
> Running with system Python will cause `ModuleNotFoundError: No module named 'bs4'`.

```bash
# Step 1: Clone or download the project folder
cd lead_gen_automation

# Step 2: Create the virtual environment
python -m venv venv

# Step 3: Activate it
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # macOS / Linux

# Step 4: Install all dependencies
pip install -r requirements.txt
```

---

## How to Run

### Option 1 — Run once (recommended for testing)
```bash
.\venv\Scripts\python lead_generator.py
```

### Option 2 — Run via the full CLI (with options)
```bash
# Run once with 'info' email prefix
.\venv\Scripts\python main.py --prefix info

# Save output to a specific folder
.\venv\Scripts\python main.py --output C:\Users\HP\Desktop\leads
```

### Option 3 — Run on a daily schedule at 08:00
```bash
# Runs immediately, then every day at 08:00
.\venv\Scripts\python scheduler.py --schedule
```

### Expected Terminal Output
```
Starting lead generation pipeline...
Collecting leads...
Collected 35 leads. Enriching emails...
Saved 33 unique leads -> .\leads_20260515_112354.xlsx

[SUCCESS] Pipeline complete.
          File saved to: .\leads_20260515_112354.xlsx
```

---

## Output (Excel File)

Each run generates a timestamped file like `leads_20260515_112354.xlsx` with
the following columns:

| Column | Description |
|---|---|
| `name` | Business name |
| `email` | Scraped email, or guessed `prefix@domain.com` |
| `email_alternatives` | Other guesses: `info@`, `hello@`, `support@`, `sales@` |
| `website` | Business website URL |
| `domain` | Extracted bare domain (`example.com`) |
| `location` | Full street address |
| `category` | Business category |

---

## My Approach — Internship Submission

I built this project to demonstrate practical skills in web scraping,
data processing, and automation using Python. The scraper uses `requests`
to fetch publicly available business listings and `BeautifulSoup` to parse
the HTML and extract structured fields like name, address, category, and
website. Since contact emails are rarely exposed in directories, I wrote a
regex-based `generate_email()` function that strips the domain from a website
URL and produces common guesses such as `contact@domain.com` or
`info@domain.com`. The enriched data is deduplicated with `pandas` and
exported to a clean, auto-formatted Excel file using `openpyxl`. Finally, I
integrated the `schedule` library to allow the entire pipeline to run
automatically every day at 08:00, making the tool production-ready for
real-world lead generation workflows.

---

## Notes

- The `ModuleNotFoundError: No module named 'bs4'` error means you are using
  the **system Python** instead of the virtual environment. Always activate
  `venv` first, or run via `.\venv\Scripts\python`.
- Emails are **guessed**, not scraped. Always verify before outreach.
- The scraper targets publicly available data and respects the site's
  structure. Extend responsibly and check `robots.txt` before targeting
  other sites.
