import re


# Common contact email prefixes to try, in priority order
EMAIL_PREFIXES = ["contact", "info", "hello", "support", "sales"]


def extract_domain(website: str) -> str:
    """
    Uses regex to extract the bare domain (e.g. 'example.com') from a URL.

    Examples:
        https://www.example.com/page  ->  example.com
        http://sub.company.org        ->  company.org
        www.startup.io                ->  startup.io
    """
    if not website or website.strip().lower() in ("n/a", ""):
        return ""

    # Strip protocol (http:// or https://)
    domain = re.sub(r"^https?://", "", website.strip(), flags=re.IGNORECASE)

    # Strip 'www.' prefix
    domain = re.sub(r"^www\.", "", domain, flags=re.IGNORECASE)

    # Strip everything after the first '/' (path, query, fragment)
    domain = re.split(r"[/?#]", domain)[0]

    # Validate it looks like a domain (letters, digits, dots, hyphens)
    if re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain):
        return domain.lower()

    return ""


def generate_email(name: str, website: str, prefix: str = "contact") -> dict:
    """
    Guesses a contact email address for a business based on its website domain.

    Args:
        name:    Business name (used as fallback label only).
        website: Full website URL string.
        prefix:  Email prefix to use (default: 'contact'). Options: contact, info, hello, support, sales.

    Returns:
        A dict with:
            - 'domain'      : extracted domain string
            - 'primary'     : the guessed email with the requested prefix
            - 'alternatives': list of alternative guesses with other common prefixes
    """
    domain = extract_domain(website)

    if not domain:
        return {
            "domain": "",
            "primary": "N/A",
            "alternatives": []
        }

    # Ensure the chosen prefix is valid
    if prefix not in EMAIL_PREFIXES:
        prefix = "contact"

    primary_email = f"{prefix}@{domain}"

    # Build alternatives (all other prefixes)
    alternatives = [f"{p}@{domain}" for p in EMAIL_PREFIXES if p != prefix]

    return {
        "domain": domain,
        "primary": primary_email,
        "alternatives": alternatives
    }


def enrich_leads_with_emails(leads: list, prefix: str = "contact") -> list:
    """
    Takes a list of lead dicts (from collect_leads()) and enriches each one
    with a guessed email if the original email is 'N/A'.

    Args:
        leads:  List of lead dictionaries.
        prefix: Email prefix to use for guessing.

    Returns:
        The same list, with 'email' fields updated where they were 'N/A'.
    """
    enriched = []
    for lead in leads:
        enriched_lead = lead.copy()

        # Only guess if email is not already found
        if lead.get("email", "N/A") == "N/A":
            result = generate_email(lead.get("name", ""), lead.get("website", "N/A"))
            enriched_lead["email"] = result["primary"]
            enriched_lead["email_alternatives"] = result["alternatives"]
            enriched_lead["domain"] = result["domain"]
        else:
            enriched_lead["email_alternatives"] = []
            enriched_lead["domain"] = extract_domain(lead.get("website", ""))

        enriched.append(enriched_lead)

    return enriched


# ── Quick demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ("QASEL",                    "https://qasel.org/"),
        ("Trixinc",                  "https://www.trixinc.com/solutions"),
        ("Mission Systems Dev Corp", "http://www.missionsystems.ca"),
        ("No Website Co",            "N/A"),
        ("Bad URL Corp",             "not-a-url"),
        ("Sub Domain Inc",           "https://app.startup.io/dashboard"),
    ]

    print(f"{'Name':<30} {'Website':<40} {'Guessed Email'}")
    print("-" * 90)
    for name, website in test_cases:
        result = generate_email(name, website)
        print(f"{name:<30} {website:<40} {result['primary']}")

    print("\n--- Alternatives for 'Trixinc' ---")
    r = generate_email("Trixinc", "https://www.trixinc.com")
    for alt in r["alternatives"]:
        print(f"  {alt}")
