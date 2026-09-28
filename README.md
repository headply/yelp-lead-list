# Yelp lead list: every business in a city, with phone and website

Yelp shows at most **240 results per search**, and the Yelp Fusion API returns **3 reviews per business**
and costs $7.99-$14.99 per 1,000 calls. This CLI returns **every** business for a search term in a city,
with phone, website, address, rating, review count and categories, as a CSV ready for your CRM.

```bash
pip install -r requirements.txt
export APIFY_TOKEN=...        # free account: https://console.apify.com/sign-up
python leads.py "plumbers" "Austin, TX" --max 500
python leads.py "dentists" "60614" --with-website-only
```

### Sample output (plumbers, Austin TX)

| name | phone | website | rating | reviews |
|---|---|---|---|---|
| Blue Dragon Plumbing | (512) 947-2491 | bluedragonplumbing.com | 4.9 | 532 |
| Rooterman Plumbing | (512) 900-7676 | rootermanofaustin.com | 4.7 | 516 |
| Proven Plumbing & Air | (512) 775-1234 | callproven.com | 4.9 | 417 |

## How it works

Runs the [Yelp Scraper & API](https://apify.com/headply/yelp-scraper) Actor on Apify, which tiles the map past Yelp's
240-result cap: **$3 per 1,000 businesses**. For reviews (all of them, owner replies, only-new monitoring)
use [Yelp Reviews Scraper](https://apify.com/headply/yelp-reviews-scraper): $0.30 per 1,000 reviews.

MIT licensed.
