# RapidAPI Listing Copy

## Name

WorldCupTravelDealsAPI

## Short Description

World Cup 2026 travel deal intelligence for flights, hotels, packages, official tickets, and safe tourism planning.

## Long Description

WorldCupTravelDealsAPI helps travel agencies, newsletters, AI agents, no-code builders, tourism apps, and event marketplaces build FIFA World Cup 2026 travel products faster.

The API covers all 16 host cities across the United States, Mexico, and Canada, with stadiums, airports, travel windows, demand tiers, cost baselines, official ticketing links, official hospitality links, hotel and flight search routes, and transparent deal scoring.

Use it to:

- Build World Cup 2026 travel dashboards.
- Generate safe flight + hotel package search links.
- Compare offer prices against event-travel baselines.
- Score whether a deal is excellent, good, fair, or weak.
- Route ticket buyers toward official FIFA channels instead of unsafe resale sources.
- Power AI travel assistants and deal newsletters.

This API is intentionally safety-first: ticket discovery is routed through FIFA official ticketing, official hospitality, and official resale/exchange information. It does not promote grey-market ticket scraping.

## Category

Travel

## Tags

world-cup-2026, travel-api, flight-deals, hotel-deals, tourism, fifa, sports-travel, rapidapi, travel-agency, ai-agents

## Suggested Plans

- Basic: USD 19/month, 2,500 requests/month.
- Pro: USD 59/month, 20,000 requests/month.
- Ultra: USD 149/month, 90,000 requests/month.
- Mega: USD 399/month, 200,000 requests/month.

Do not create a free public plan. Keep all public plans paid-only.

## Production Security

Set the backend environment variables:

- `REQUIRE_PAID_GATEWAY=true`
- `PAID_GATEWAY_SECRET=<strong-shared-secret>`

Configure RapidAPI to send that secret as `X-RapidAPI-Proxy-Secret` or `X-API-Gateway-Secret`. This prevents direct backend use outside the paid marketplace.

## Suggested Endpoint Highlights

- `/deals/search`: Generate World Cup travel package candidates with safe booking links and deal scores.
- `/cities`: Explore all host cities, airports, stadiums, demand levels, and match windows.
- `/score`: Score a real flight/hotel/package offer against a baseline.
- `/official-links`: FIFA official tickets, hospitality, and resale/exchange guidance.
