# RapidAPI Listing Copy

## Name

WorldCupTravelDealsAPI

## Short Description

World Cup 2026 travel planning, safe official links, package search routes, reference estimates, and transparent deal scoring.

## Long Description

WorldCupTravelDealsAPI helps travel agencies, newsletters, AI agents, no-code builders, tourism apps, and event marketplaces build FIFA World Cup 2026 travel products faster.

The API covers all 16 host cities across the United States, Mexico, and Canada, with stadiums, airports, travel windows, demand tiers, cost baselines, official ticketing links, official hospitality links, hotel and flight search routes, and transparent deal scoring.

The current version is a planning and scoring API. It does not claim to return live flight fares, hotel availability, or ticket inventory. Generated package candidates are clearly marked as heuristic references, and buyers can use `/score` with real offers from their own providers.

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

- Basic evaluation: USD 0, 25 requests/month hard limit.
- Pro: USD 9.99/month, 10,000 requests/month.
- Ultra: USD 29/month, 50,000 requests/month.
- Mega: USD 79/month, 200,000 requests/month.

The Basic plan is only for integration verification. Direct backend usage
remains blocked outside the authorized marketplace.

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

## Required Listing Improvements

- Add a spotlight linking to the public product page.
- Add a tutorial showing a World Cup city comparison workflow.
- Add example responses that clearly display `inventory_disclosure`.
- Never call generated estimates or provider search links live offers.
