"""
Full project health check — runs all 4 modules in sequence and reports results.
Run with: .\\venv\\Scripts\\python check.py
"""
import os

print("=" * 55)
print("  LEAD GENERATION AUTOMATION — HEALTH CHECK")
print("=" * 55)

# ── Test 1: scraper ────────────────────────────────────────
print("\n[1/4] scraper.py — collect_leads()")
try:
    from scraper import collect_leads
    leads = collect_leads()
    assert len(leads) >= 30, f"Expected 30+ leads, got {len(leads)}"
    assert all(k in leads[0] for k in ["name", "email", "website", "location", "category"])
    print(f"      Leads collected  : {len(leads)}")
    print(f"      Sample name      : {leads[0]['name']}")
    print(f"      Sample location  : {leads[0]['location']}")
    print("      STATUS: PASS")
except Exception as e:
    print(f"      STATUS: FAIL — {e}")

# ── Test 2: email domain extraction ───────────────────────
print("\n[2/4] email_guesser.py — generate_email()")
try:
    from email_guesser import generate_email, extract_domain
    assert extract_domain("https://www.example.com/page") == "example.com"
    assert extract_domain("N/A") == ""
    r = generate_email("Test Co", "https://www.trixinc.com")
    assert r["primary"] == "contact@trixinc.com"
    assert len(r["alternatives"]) == 4
    print(f"      Domain extracted : {extract_domain('https://www.example.com/page')}")
    print(f"      Primary email    : {r['primary']}")
    print(f"      Alternatives     : {', '.join(r['alternatives'])}")
    print("      STATUS: PASS")
except Exception as e:
    print(f"      STATUS: FAIL — {e}")

# ── Test 3: email enrichment ───────────────────────────────
print("\n[3/4] email_guesser.py — enrich_leads_with_emails()")
try:
    from email_guesser import enrich_leads_with_emails
    enriched = enrich_leads_with_emails(leads)
    has_email = sum(1 for l in enriched if l["email"] != "N/A")
    no_email  = len(enriched) - has_email
    assert len(enriched) == len(leads)
    print(f"      Enriched leads   : {len(enriched)}")
    print(f"      Emails guessed   : {has_email}")
    print(f"      Still N/A        : {no_email}  (no website for these entries)")
    print("      STATUS: PASS")
except Exception as e:
    print(f"      STATUS: FAIL — {e}")

# ── Test 4: Excel export ───────────────────────────────────
print("\n[4/4] save_leads.py — save_leads_to_excel()")
try:
    from save_leads import save_leads_to_excel
    path = save_leads_to_excel(output_dir=".", prefix="contact")
    assert path and os.path.exists(path), "File was not created"
    size_kb = os.path.getsize(path) // 1024
    print(f"      File saved to    : {path}")
    print(f"      File size        : {size_kb} KB")
    print("      STATUS: PASS")
except Exception as e:
    print(f"      STATUS: FAIL — {e}")

print("\n" + "=" * 55)
print("  HEALTH CHECK COMPLETE")
print("=" * 55)
print("\nHow to run the project:")
print("  One-shot  : .\\venv\\Scripts\\python lead_generator.py")
print("  Scheduled : .\\venv\\Scripts\\python scheduler.py --schedule")
