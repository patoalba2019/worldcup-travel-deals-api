# WorldCupTravelDealsAPI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-Paid-orange.svg)](https://rapidapi.com/patoalba2019/api/worldcuptraveldealsapi)

![WorldCupTravelDealsAPI logo](assets/worldcup-travel-deals-logo-500.png)

**⚽ Professional travel-intelligence API for FIFA World Cup 2026 tourism products**

[Subscribe on RapidAPI](https://rapidapi.com/patoalba2019/api/worldcuptraveldealsapi?utm_source=github&utm_medium=repository&utm_campaign=worldcup_readme) |
[View product details](https://patoapis-paid-apis.onrender.com/world-cup-travel-api.html?utm_source=github&utm_medium=repository&utm_campaign=worldcup_readme) |
[Live Demo](https://patoapis-paid-apis.onrender.com/)

> Commercial API access is paid and delivered through RapidAPI. The direct
> production backend rejects requests that do not carry the private marketplace
> gateway credential.

## 🎯 Why WorldCupTravelDealsAPI?

**Build safer World Cup 2026 travel experiences with official data and transparent deal scoring.**

WorldCupTravelDealsAPI is a professional travel-intelligence API for FIFA World Cup 2026 tourism products. It helps travel agencies, deal newsletters, no-code builders, AI agents, and event-tourism apps discover host-city opportunities, build safe booking routes, compare packages, and score whether a flight + hotel offer is actually attractive.

The API is designed to be safe and sellable on RapidAPI: ticket links point to official FIFA channels, travel searches are structured as outbound provider searches, and every response clearly discloses that the current version does not return live flight, hotel, or ticket inventory.

**Perfect for:**
- Travel agencies and tour operators
- Deal comparison websites
- AI travel assistants
- Event tourism apps
- Travel newsletters
- No-code travel builders

## ✨ Key Features

- **🏟️ Complete City Data**: All 16 FIFA World Cup 2026 host cities with stadiums, airports, time zones
- **💰 Cost Intelligence**: Travel cost tiers, demand levels, and price estimates
- **🔍 Smart Search**: Generate flight, hotel, ticket, and hospitality search links
- **📊 Deal Scoring**: Transparent scoring system for real offers
- **🔒 Official Channels Only**: No grey-market scraping, all ticket links go to official FIFA sources
- **📅 Match Windows**: Accurate match dates and travel windows for each city
- **🌍 Multi-Region**: USA, Mexico, and Canada host cities covered
- **⚡ Fast Responses**: Cached data for quick API calls
- **🛡️ Safety First**: Explicit inventory disclosures to prevent fraud

## 🛠️ API Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /` | API overview, positioning, endpoints, and official sources |
| `GET /health` | Runtime status and provider-key readiness |
| `GET /cities` | Host-city dataset, optional `region` filter |
| `GET /cities/<slug>` | City details, baseline estimate, and booking/search links |
| `GET /deals/search` | Deal-intelligence package candidates by origin, city, date, nights, and travelers |
| `GET /score` | Score a real offer supplied by the buyer |
| `GET /official-links` | FIFA official ticketing, hospitality, and resale help links |
| `GET /pricing-recommendation` | Suggested RapidAPI plan structure |

## Example

```bash
curl "https://your-domain.example/deals/search?origin=EZE&city=miami&start=2026-06-15&nights=5&travelers=2"
```

## Inventory Disclosure

The current version provides structured planning data, provider search links,
heuristic reference estimates, and scoring for real offers supplied by the
buyer. It does **not** return live flight fares, hotel availability, or ticket
inventory.

Responses include an `inventory_disclosure` object and mark generated package
candidates with `is_live_offer: false`. Provider integrations can be added in a
future version after approved credentials and implementation are available.

## Paid-Only Gateway Protection

For production, set:

```bash
REQUIRE_PAID_GATEWAY=true
PAID_GATEWAY_SECRET=<strong-shared-secret>
```

Then configure RapidAPI to send the same value as `X-RapidAPI-Proxy-Secret` or `X-API-Gateway-Secret`. Direct backend calls without that secret receive `402 Payment Required`.

For deployments managed from version control, set
`PAID_GATEWAY_SECRET_HASHES=<sha256-of-shared-secret>` instead. RapidAPI keeps
the original private secret, while GitHub and Render store only its
non-reversible fingerprint.

## 📈 Pricing

### RapidAPI Plans
- **Starter**: $4.99/month - 1,000 requests/month
- **Pro**: $9.99/month - 10,000 requests/month  
- **Ultra**: $29/month - 50,000 requests/month
- **Mega**: $79/month - 200,000 requests/month

[Subscribe on RapidAPI](https://rapidapi.com/patoalba2019/api/worldcuptraveldealsapi)

## 📊 Use Cases

- **Travel Agencies**: Build World Cup travel packages with accurate data
- **Deal Comparison**: Score and compare travel offers
- **AI Travel Assistants**: Feed city data to AI-powered travel planning
- **Event Tourism Apps**: Create World Cup travel experiences
- **Newsletters**: Generate World Cup travel deal content
- **No-Code Builders**: Integrate World Cup data into no-code platforms

## 🔗 Links

- [RapidAPI Marketplace](https://rapidapi.com/patoalba2019/api/worldcuptraveldealsapi)
- [Product Website](https://patoapis-paid-apis.onrender.com/world-cup-travel-api.html)
- [Documentation](https://patoapis-paid-apis.onrender.com/guides/world-cup-city-comparison.html)
- [Support](https://rapidapi.com/patoalba2019/api/worldcuptraveldealsapi/support)

## Safety Positioning

World Cup 2026 ticket demand is high and fraud risk is real. This API intentionally routes ticket-related discovery through official FIFA ticketing, official hospitality, and official resale/exchange help pages.

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/patoalba2019/worldcup-travel-deals-api.git
cd worldcup-travel-deals-api

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

### Test the API
```bash
# Health check
curl http://localhost:5000/health

# Get all cities
curl http://localhost:5000/cities

# Search for deals
curl "http://localhost:5000/deals/search?origin=EZE&city=miami&start=2026-06-15&nights=5&travelers=2"
```

## Test

```bash
python3 -m unittest discover -s tests
```

## License

Proprietary software. All rights reserved. See [LICENSE](LICENSE).
Access to the hosted API requires an active paid RapidAPI subscription.
