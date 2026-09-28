#!/usr/bin/env python3
"""Build a Yelp lead list (phone, website, address, rating) for a search term in a city."""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

def run_actor(actor, run_input):
    """Run an Apify Actor and return its dataset items. Needs APIFY_TOKEN in the environment."""
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first (free account: https://console.apify.com/sign-up, "
                 "token: https://console.apify.com/settings/integrations).")
    client = ApifyClient(token)
    print(f"Running {actor} ...", file=sys.stderr)
    run = client.actor(actor).call(run_input=run_input)
    # apify-client 3.x returns a Run object, older versions a dict
    field = lambda snake, camel: (run.get(camel) if isinstance(run, dict) else getattr(run, snake, None)) if run else None
    status = getattr(field("status", "status"), "value", field("status", "status"))
    if status != "SUCCEEDED":
        sys.exit(f"Run did not succeed: {status}. Open https://console.apify.com/actors/runs for the log.")
    return list(client.dataset(field("default_dataset_id", "defaultDatasetId")).iterate_items())


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("term", help='e.g. "plumbers"')
    p.add_argument("location", help='e.g. "Austin, TX" or a ZIP code')
    p.add_argument("--max", type=int, default=200, help="max businesses (above 240 the whole area is tiled)")
    p.add_argument("--with-website-only", action="store_true")
    p.add_argument("--out", default="leads.csv")
    a = p.parse_args()
    items = run_actor("headply/yelp-scraper", {"searchTerms": [a.term], "locations": [a.location],
                                               "maxBusinessesPerSearch": a.max, "coverWholeArea": True})
    rows = []
    for it in items:
        if it.get("type") != "business":
            continue
        addr = it.get("address") or {}
        row = {"name": it.get("name"), "phone": it.get("phone"), "website": it.get("website"), "rating": it.get("rating"),
               "reviewCount": it.get("reviewCount"), "categories": ", ".join(it.get("categories") or []),
               "street": addr.get("street"), "city": addr.get("city"), "region": addr.get("region"),
               "postalCode": addr.get("postalCode"), "yelpUrl": it.get("url"), "isClaimed": it.get("isClaimed")}
        if a.with_website_only and not row["website"]:
            continue
        rows.append(row)
    write_csv(a.out, rows, list(rows[0]) if rows else ["name"])


if __name__ == "__main__":
    main()
