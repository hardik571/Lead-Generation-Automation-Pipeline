import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, parse_qs

def collect_leads():
    """
    Scrapes business leads from YellowPages.ca for 'Software' in 'Toronto ON'.
    Returns a list of dictionaries with name, email, website, location, and category.
    """
    url = "https://www.yellowpages.ca/search/si/1/Software/Toronto+ON"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    leads = []
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("div", class_="listing")
        
        for listing in listings:
            # Extract Name
            name_tag = listing.find("a", class_="listing__name--link")
            name = name_tag.text.strip() if name_tag else "N/A"
            
            # Extract Website
            # Title format is "BUSINESS NAME - Business Website"
            website = "N/A"
            web_tag = listing.find("a", title=lambda t: t and "Business Website" in t)
            if web_tag and web_tag.has_attr("href"):
                href = web_tag["href"]
                if "redirect=" in href:
                    # Parse the actual website from the redirect URL
                    parsed_url = urlparse(href)
                    query_params = parse_qs(parsed_url.query)
                    website = query_params.get("redirect", ["N/A"])[0]
            
            # Extract Location
            loc_tag = listing.find("span", class_="listing__address--full")
            location = loc_tag.text.strip() if loc_tag else "N/A"
            
            # Extract Category
            # Look for the first link that isn't name, directions, or website
            cat_tag = listing.find("a", class_="listing__category--link")
            category = cat_tag.text.strip() if cat_tag else "Software"
            
            # Extract Email (if available)
            email = "N/A"
            # Note: YellowPages usually hides emails behind contact forms or requires detail page visits.
            # We'll check for any mailto link as a fallback.
            mailto_tag = listing.find("a", href=lambda x: x and x.startswith("mailto:"))
            if mailto_tag:
                email = mailto_tag["href"].replace("mailto:", "")

            leads.append({
                "name": name,
                "email": email,
                "website": website,
                "location": location,
                "category": category
            })
            
            if len(leads) >= 40: # Aim for 30+, page has ~35
                break
                
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return leads

if __name__ == "__main__":
    results = collect_leads()
    print(f"Collected {len(results)} leads.")
    for i, lead in enumerate(results[:5], 1):
        print(f"{i}. {lead['name']} - {lead['category']} - {lead['location']}")
