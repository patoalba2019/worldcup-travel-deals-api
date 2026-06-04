# WorldCupTravelDealsAPI

![WorldCupTravelDealsAPI logo](assets/worldcup-travel-deals-logo-500.png)

WorldCupTravelDealsAPI is a professional travel-intelligence API for FIFA World Cup 2026 tourism products. It helps travel agencies, deal newsletters, no-code builders, AI agents, and event-tourism apps discover host-city opportunities, build safe booking routes, compare packages, and score whether a flight + hotel offer is actually attractive.

The API is designed to be safe and sellable on RapidAPI: ticket links point to official FIFA channels, travel searches are structured as outbound provider searches, and every response clearly discloses that the current version does not return live flight, hotel, or ticket inventory.

## What It Does

- Lists all 16 FIFA World Cup 2026 host cities with stadiums, airports, time zones, demand level, travel cost tier, and match windows.
- Generates flight, hotel, ticket, hospitality, and official resale search links for each city/date/traveler combination.
- Scores real offers with a transparent deal score based on baseline, price, savings, and source safety.
- Provides RapidAPI-friendly endpoints and OpenAPI docs.
- Keeps ticket safety front and center: no grey-market scraping, no fake ticket claims, no unsafe resale promotion.

## Endpoints

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

## RapidAPI Pricing Suggestion

- **Starter**: USD 4.99/month, 1,000 requests/month.
- **Pro**: USD 9.99/month, 10,000 requests/month.
- **Ultra**: USD 29/month, 50,000 requests/month.
- **Mega**: USD 79/month, 200,000 requests/month.

Every plan is paid. Direct backend access remains blocked by the paid gateway
secret.

## Safety Positioning

World Cup 2026 ticket demand is high and fraud risk is real. This API intentionally routes ticket-related discovery through official FIFA ticketing, official hospitality, and official resale/exchange help pages.

## Run Locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python server.py
```

## Test

```bash
python3 -m unittest discover -s tests
```
