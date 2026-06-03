from __future__ import annotations

import math
import os
from datetime import UTC, date, datetime, timedelta
from urllib.parse import quote_plus

from flask import Flask, jsonify, request


API_NAME = "WorldCupTravelDealsAPI"
API_VERSION = "1.0.0"
OFFICIAL_TICKET_URL = "https://www.fifa.com/tickets"
OFFICIAL_HOSPITALITY_URL = "https://fifaworldcup26.hospitalityexperiences.fifa.com/"
OFFICIAL_RESALE_HELP_URL = (
    "https://gpcustomersupportfwc2026.tickets.fifa.com/hc/en-gb/sections/"
    "30546469442077-FIFA-Resale-Exchange-Marketplace"
)


HOST_CITIES = [
    {
        "slug": "atlanta",
        "city": "Atlanta",
        "country": "United States",
        "region": "USA",
        "stadium": "Mercedes-Benz Stadium",
        "timezone": "America/New_York",
        "airports": ["ATL"],
        "lat": 33.755,
        "lon": -84.401,
        "tourism_tier": "major",
        "expected_demand": "high",
        "hotel_cost_tier": 4,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-15", "end": "2026-07-15"},
    },
    {
        "slug": "boston",
        "city": "Boston",
        "country": "United States",
        "region": "USA",
        "stadium": "Gillette Stadium",
        "timezone": "America/New_York",
        "airports": ["BOS", "PVD"],
        "lat": 42.092,
        "lon": -71.264,
        "tourism_tier": "major",
        "expected_demand": "high",
        "hotel_cost_tier": 5,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-13", "end": "2026-07-09"},
    },
    {
        "slug": "dallas",
        "city": "Dallas",
        "country": "United States",
        "region": "USA",
        "stadium": "AT&T Stadium",
        "timezone": "America/Chicago",
        "airports": ["DFW", "DAL"],
        "lat": 32.747,
        "lon": -97.092,
        "tourism_tier": "major",
        "expected_demand": "very_high",
        "hotel_cost_tier": 4,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-14", "end": "2026-07-14"},
    },
    {
        "slug": "guadalajara",
        "city": "Guadalajara",
        "country": "Mexico",
        "region": "Mexico",
        "stadium": "Estadio Akron",
        "timezone": "America/Mexico_City",
        "airports": ["GDL"],
        "lat": 20.681,
        "lon": -103.462,
        "tourism_tier": "value",
        "expected_demand": "medium",
        "hotel_cost_tier": 2,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-11", "end": "2026-06-26"},
    },
    {
        "slug": "houston",
        "city": "Houston",
        "country": "United States",
        "region": "USA",
        "stadium": "NRG Stadium",
        "timezone": "America/Chicago",
        "airports": ["IAH", "HOU"],
        "lat": 29.684,
        "lon": -95.411,
        "tourism_tier": "major",
        "expected_demand": "high",
        "hotel_cost_tier": 3,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-14", "end": "2026-07-04"},
    },
    {
        "slug": "kansas-city",
        "city": "Kansas City",
        "country": "United States",
        "region": "USA",
        "stadium": "Arrowhead Stadium",
        "timezone": "America/Chicago",
        "airports": ["MCI"],
        "lat": 39.049,
        "lon": -94.484,
        "tourism_tier": "value",
        "expected_demand": "high",
        "hotel_cost_tier": 3,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-16", "end": "2026-07-11"},
    },
    {
        "slug": "los-angeles",
        "city": "Los Angeles",
        "country": "United States",
        "region": "USA",
        "stadium": "SoFi Stadium",
        "timezone": "America/Los_Angeles",
        "airports": ["LAX", "BUR", "SNA", "ONT"],
        "lat": 33.953,
        "lon": -118.339,
        "tourism_tier": "premium",
        "expected_demand": "very_high",
        "hotel_cost_tier": 5,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-12", "end": "2026-07-10"},
    },
    {
        "slug": "mexico-city",
        "city": "Mexico City",
        "country": "Mexico",
        "region": "Mexico",
        "stadium": "Estadio Azteca",
        "timezone": "America/Mexico_City",
        "airports": ["MEX", "NLU"],
        "lat": 19.303,
        "lon": -99.151,
        "tourism_tier": "value",
        "expected_demand": "very_high",
        "hotel_cost_tier": 3,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-11", "end": "2026-06-30"},
    },
    {
        "slug": "miami",
        "city": "Miami",
        "country": "United States",
        "region": "USA",
        "stadium": "Hard Rock Stadium",
        "timezone": "America/New_York",
        "airports": ["MIA", "FLL"],
        "lat": 25.958,
        "lon": -80.239,
        "tourism_tier": "premium",
        "expected_demand": "very_high",
        "hotel_cost_tier": 5,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-15", "end": "2026-07-18"},
    },
    {
        "slug": "monterrey",
        "city": "Monterrey",
        "country": "Mexico",
        "region": "Mexico",
        "stadium": "Estadio BBVA",
        "timezone": "America/Monterrey",
        "airports": ["MTY"],
        "lat": 25.668,
        "lon": -100.244,
        "tourism_tier": "value",
        "expected_demand": "medium",
        "hotel_cost_tier": 2,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-14", "end": "2026-06-29"},
    },
    {
        "slug": "new-york-new-jersey",
        "city": "New York / New Jersey",
        "country": "United States",
        "region": "USA",
        "stadium": "MetLife Stadium",
        "timezone": "America/New_York",
        "airports": ["JFK", "EWR", "LGA"],
        "lat": 40.813,
        "lon": -74.074,
        "tourism_tier": "premium",
        "expected_demand": "very_high",
        "hotel_cost_tier": 5,
        "flight_cost_tier": 5,
        "match_window": {"start": "2026-06-13", "end": "2026-07-19"},
    },
    {
        "slug": "philadelphia",
        "city": "Philadelphia",
        "country": "United States",
        "region": "USA",
        "stadium": "Lincoln Financial Field",
        "timezone": "America/New_York",
        "airports": ["PHL"],
        "lat": 39.901,
        "lon": -75.167,
        "tourism_tier": "major",
        "expected_demand": "high",
        "hotel_cost_tier": 4,
        "flight_cost_tier": 3,
        "match_window": {"start": "2026-06-14", "end": "2026-07-04"},
    },
    {
        "slug": "san-francisco-bay-area",
        "city": "San Francisco Bay Area",
        "country": "United States",
        "region": "USA",
        "stadium": "Levi's Stadium",
        "timezone": "America/Los_Angeles",
        "airports": ["SFO", "SJC", "OAK"],
        "lat": 37.403,
        "lon": -121.970,
        "tourism_tier": "premium",
        "expected_demand": "high",
        "hotel_cost_tier": 5,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-13", "end": "2026-07-01"},
    },
    {
        "slug": "seattle",
        "city": "Seattle",
        "country": "United States",
        "region": "USA",
        "stadium": "Lumen Field",
        "timezone": "America/Los_Angeles",
        "airports": ["SEA"],
        "lat": 47.595,
        "lon": -122.332,
        "tourism_tier": "major",
        "expected_demand": "high",
        "hotel_cost_tier": 4,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-15", "end": "2026-07-06"},
    },
    {
        "slug": "toronto",
        "city": "Toronto",
        "country": "Canada",
        "region": "Canada",
        "stadium": "BMO Field",
        "timezone": "America/Toronto",
        "airports": ["YYZ", "YTZ"],
        "lat": 43.633,
        "lon": -79.419,
        "tourism_tier": "major",
        "expected_demand": "high",
        "hotel_cost_tier": 4,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-12", "end": "2026-07-02"},
    },
    {
        "slug": "vancouver",
        "city": "Vancouver",
        "country": "Canada",
        "region": "Canada",
        "stadium": "BC Place",
        "timezone": "America/Vancouver",
        "airports": ["YVR"],
        "lat": 49.276,
        "lon": -123.111,
        "tourism_tier": "premium",
        "expected_demand": "high",
        "hotel_cost_tier": 5,
        "flight_cost_tier": 4,
        "match_window": {"start": "2026-06-13", "end": "2026-07-07"},
    },
]

CITY_BY_SLUG = {city["slug"]: city for city in HOST_CITIES}


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.before_request
def enforce_paid_gateway():
    if request.method == "OPTIONS":
        return None
    if os.getenv("REQUIRE_PAID_GATEWAY", "false").lower() not in {"1", "true", "yes"}:
        return None
    expected = os.getenv("PAID_GATEWAY_SECRET")
    if not expected:
        return jsonify({"error": "Paid gateway is required but not configured."}), 503
    provided = (
        request.headers.get("X-RapidAPI-Proxy-Secret")
        or request.headers.get("X-API-Gateway-Secret")
        or request.headers.get("X-WorldCupTravelDeals-Secret")
    )
    if provided != expected:
        return (
            jsonify(
                {
                    "error": "Access denied. Subscribe through the authorized API marketplace to use this API.",
                    "marketplace": "RapidAPI",
                }
            ),
            402,
        )
    return None


def parse_date(value: str | None, default: date) -> date:
    if not value:
        return default
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid date '{value}'. Use YYYY-MM-DD.") from exc


def parse_int(name: str, default: int, minimum: int = 1, maximum: int = 99) -> int:
    raw = request.args.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer.") from exc
    return max(minimum, min(maximum, value))


def money(value: float) -> int:
    return int(round(value))


def city_baseline(city: dict, nights: int, travelers: int, origin: str | None = None) -> dict:
    hotel_night = 95 + city["hotel_cost_tier"] * 45
    flight_base = 260 + city["flight_cost_tier"] * 115
    local_daily = 55 + city["hotel_cost_tier"] * 14
    demand_multiplier = {
        "medium": 1.10,
        "high": 1.28,
        "very_high": 1.45,
    }.get(city["expected_demand"], 1.2)
    if origin and origin.upper() in city["airports"]:
        flight_base = 0

    return {
        "currency": "USD",
        "flight_per_person": money(flight_base * demand_multiplier),
        "hotel_per_room_night": money(hotel_night * demand_multiplier),
        "local_daily_per_person": money(local_daily * demand_multiplier),
        "estimated_total": money(
            (flight_base * travelers)
            + (hotel_night * nights * max(1, math.ceil(travelers / 2)))
            + (local_daily * nights * travelers)
        ),
        "method": "Heuristic event-travel baseline. Use /score to compare real offers from your providers.",
    }


def safety_notes() -> list[str]:
    return [
        "World Cup ticket purchases should be routed through FIFA official ticketing, FIFA official resale/exchange, or official hospitality providers.",
        "This API does not validate unofficial ticket inventory and does not endorse grey-market resale listings.",
        "Flight and hotel deep links are search links unless a live provider key is configured.",
    ]


def build_search_links(city: dict, origin: str, start: date, end: date, travelers: int) -> dict:
    destination = city["airports"][0]
    query_city = quote_plus(city["city"])
    start_s = start.isoformat()
    end_s = end.isoformat()
    return {
        "official_tickets": OFFICIAL_TICKET_URL,
        "official_hospitality": OFFICIAL_HOSPITALITY_URL,
        "official_resale_help": OFFICIAL_RESALE_HELP_URL,
        "google_flights": (
            "https://www.google.com/travel/flights?q="
            f"Flights%20from%20{quote_plus(origin.upper())}%20to%20{destination}%20"
            f"on%20{start_s}%20returning%20{end_s}"
        ),
        "booking_hotels": (
            "https://www.booking.com/searchresults.html?"
            f"ss={query_city}&checkin={start_s}&checkout={end_s}&group_adults={travelers}"
        ),
        "google_hotels": (
            "https://www.google.com/travel/hotels/"
            f"{query_city}?checkin={start_s}&checkout={end_s}&adults={travelers}"
        ),
    }


def deal_score(price: float, baseline: float, safety: str = "official_or_direct") -> dict:
    if price <= 0 or baseline <= 0:
        raise ValueError("price and baseline must be greater than zero.")
    savings_pct = max(-100.0, (baseline - price) / baseline * 100)
    safety_bonus = {
        "official": 12,
        "official_or_direct": 9,
        "provider_verified": 6,
        "unknown": -20,
    }.get(safety, 0)
    raw_score = 55 + savings_pct * 1.1 + safety_bonus
    score = max(0, min(100, round(raw_score, 1)))
    if score >= 82:
        label = "excellent"
    elif score >= 68:
        label = "good"
    elif score >= 52:
        label = "fair"
    else:
        label = "weak"
    return {
        "score": score,
        "label": label,
        "savings_percent": round(savings_pct, 2),
        "baseline": money(baseline),
        "price": money(price),
        "safety": safety,
    }


def live_provider_status() -> dict:
    return {
        "amadeus": {
            "enabled": bool(os.getenv("AMADEUS_CLIENT_ID") and os.getenv("AMADEUS_CLIENT_SECRET")),
            "capability": "flight_price_search",
        },
        "travelpayouts": {
            "enabled": bool(os.getenv("TRAVELPAYOUTS_TOKEN")),
            "capability": "flight_calendar_prices",
        },
        "hotelbeds": {
            "enabled": bool(os.getenv("HOTELBEDS_API_KEY") and os.getenv("HOTELBEDS_SECRET")),
            "capability": "hotel_availability",
        },
    }


@app.errorhandler(ValueError)
def value_error(error):
    return jsonify({"error": str(error)}), 400


@app.get("/")
def index():
    return jsonify(
        {
            "api": API_NAME,
            "version": API_VERSION,
            "positioning": "World Cup 2026 travel deal intelligence for agencies, apps, newsletters, and AI agents.",
            "endpoints": {
                "health": "/health",
                "cities": "/cities",
                "city_detail": "/cities/<slug>",
                "search_deals": "/deals/search",
                "score_offer": "/score",
                "official_links": "/official-links",
                "pricing": "/pricing-recommendation",
            },
            "sources": {
                "official_tickets": OFFICIAL_TICKET_URL,
                "official_hospitality": OFFICIAL_HOSPITALITY_URL,
                "official_resale_help": OFFICIAL_RESALE_HELP_URL,
            },
            "safety_notes": safety_notes(),
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "api": API_NAME,
            "version": API_VERSION,
            "host_city_count": len(HOST_CITIES),
            "live_providers": live_provider_status(),
            "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        }
    )


@app.get("/cities")
def cities():
    region = request.args.get("region")
    rows = HOST_CITIES
    if region:
        rows = [city for city in rows if city["region"].lower() == region.lower()]
    return jsonify({"count": len(rows), "cities": rows})


@app.get("/cities/<slug>")
def city_detail(slug: str):
    city = CITY_BY_SLUG.get(slug)
    if not city:
        return jsonify({"error": "City not found.", "available_slugs": sorted(CITY_BY_SLUG)}), 404
    nights = parse_int("nights", 4, 1, 30)
    travelers = parse_int("travelers", 2, 1, 20)
    origin = request.args.get("origin")
    start = parse_date(request.args.get("start"), date.fromisoformat(city["match_window"]["start"]))
    end = parse_date(request.args.get("end"), start + timedelta(days=nights))
    return jsonify(
        {
            "city": city,
            "baseline": city_baseline(city, nights=nights, travelers=travelers, origin=origin),
            "search_links": build_search_links(city, origin or "ANY", start, end, travelers),
            "safety_notes": safety_notes(),
        }
    )


@app.get("/official-links")
def official_links():
    return jsonify(
        {
            "ticketing": {
                "official_tickets": OFFICIAL_TICKET_URL,
                "official_hospitality": OFFICIAL_HOSPITALITY_URL,
                "official_resale_help": OFFICIAL_RESALE_HELP_URL,
            },
            "warning": "Avoid unofficial ticket sellers unless the buyer understands transfer, resale, and fraud risk.",
            "safety_notes": safety_notes(),
        }
    )


@app.get("/deals/search")
def search_deals():
    origin = request.args.get("origin", "EZE").upper()
    city_slug = request.args.get("city", "miami")
    city = CITY_BY_SLUG.get(city_slug)
    if not city:
        raise ValueError(f"Unknown city '{city_slug}'. Use /cities for supported slugs.")

    travelers = parse_int("travelers", 2, 1, 20)
    nights = parse_int("nights", 5, 1, 30)
    start = parse_date(request.args.get("start"), date.fromisoformat(city["match_window"]["start"]))
    end = parse_date(request.args.get("end"), start + timedelta(days=nights))
    budget = request.args.get("budget")
    budget_value = float(budget) if budget else None
    baseline = city_baseline(city, nights=nights, travelers=travelers, origin=origin)
    estimated = budget_value or baseline["estimated_total"]

    suggestions = []
    for delta, label, price_factor in [
        (-2, "arrive_early", 0.92),
        (0, "event_window", 1.0),
        (2, "flexible_departure", 0.9),
    ]:
        shifted_start = start + timedelta(days=delta)
        shifted_end = end + timedelta(days=delta)
        price = estimated * price_factor
        suggestions.append(
            {
                "type": "package_search",
                "label": label,
                "city": city["slug"],
                "origin": origin,
                "start": shifted_start.isoformat(),
                "end": shifted_end.isoformat(),
                "travelers": travelers,
                "estimated_reference_price": money(price),
                "deal_score": deal_score(price, baseline["estimated_total"], "official_or_direct"),
                "links": build_search_links(city, origin, shifted_start, shifted_end, travelers),
            }
        )

    return jsonify(
        {
            "query": {
                "origin": origin,
                "city": city_slug,
                "start": start.isoformat(),
                "end": end.isoformat(),
                "travelers": travelers,
                "nights": nights,
                "budget": budget_value,
            },
            "live_providers": live_provider_status(),
            "baseline": baseline,
            "results": suggestions,
            "disclaimer": "Results are deal-intelligence search candidates. Configure provider API keys for live fare/hotel inventory.",
            "safety_notes": safety_notes(),
        }
    )


@app.get("/score")
def score():
    price = float(request.args.get("price", "0"))
    baseline = float(request.args.get("baseline", "0"))
    safety = request.args.get("safety", "official_or_direct")
    return jsonify({"deal_score": deal_score(price, baseline, safety)})


@app.get("/pricing-recommendation")
def pricing_recommendation():
    return jsonify(
        {
            "rapidapi_plans": [
                {
                    "name": "Basic",
                    "price_usd_monthly": 19,
                    "quota": "2,500 requests/month",
                    "buyer": "small newsletters, indie apps, no-code builders",
                },
                {
                    "name": "Pro",
                    "price_usd_monthly": 59,
                    "quota": "20,000 requests/month",
                    "buyer": "travel agencies, job/event boards, content sites",
                },
                {
                    "name": "Business",
                    "price_usd_monthly": 149,
                    "quota": "100,000 requests/month",
                    "buyer": "agencies, AI assistants, tourism marketplaces",
                },
                {
                    "name": "Enterprise",
                    "price_usd_monthly": 399,
                    "quota": "custom",
                    "buyer": "high-volume travel products and affiliate networks",
                },
            ],
            "note": "Use paid-only RapidAPI plans. Do not expose a public free tier; direct backend access is blocked by the paid gateway secret.",
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
