# RapidAPI Listing Copy

## Name

WorldCupTravelDealsAPI

## Short Description

World Cup 2026 travel planning, official ticketing routes, package search routes, reference estimates, and transparent deal scoring.

## Long Description

WorldCupTravelDealsAPI helps travel agencies, newsletters, AI agents, no-code builders, tourism apps, and event marketplaces build FIFA World Cup 2026 travel products faster.

The API covers all 16 host cities across the United States, Mexico, and Canada, with stadiums, airports, travel windows, demand tiers, cost baselines, official ticketing links, official hospitality links, hotel and flight search routes, and transparent deal scoring.

The API is built for World Cup travel planning and offer scoring. Buyers use provider routes to collect current market quotes, then use `/score` to compare their own flight, hotel, or package offers against event-travel baselines.

Use it to:

- Build World Cup 2026 travel dashboards.
- Generate safe flight + hotel package search links.
- Compare offer prices against event-travel baselines.
- Score whether a deal is excellent, good, fair, or weak.
- Route ticket buyers toward official FIFA channels and trusted hospitality paths.
- Power AI travel assistants and deal newsletters.

This API is intentionally official-source-first: ticket discovery is routed through FIFA official ticketing, official hospitality, and official resale/exchange information.

## Category

Travel

## Tags

world-cup-2026, travel-api, flight-deals, hotel-deals, tourism, fifa, sports-travel, rapidapi, travel-agency, ai-agents

## Suggested Plans

- Starter: USD 4.99/month, 1,000 requests/month.
- Pro: USD 9.99/month, 10,000 requests/month.
- Ultra: USD 29/month, 50,000 requests/month.
- Mega: USD 79/month, 200,000 requests/month.

Every plan is paid. Direct backend usage remains blocked outside the authorized
marketplace.

## Production Security

Set the backend environment variables:

- `REQUIRE_PAID_GATEWAY=true`
- `PAID_GATEWAY_SECRET=<rapidapi-secret>` for one marketplace, or
  `PAID_GATEWAY_SECRETS=<rapidapi-secret>,<other-market-secret>` for several.

Configure RapidAPI to send that secret as `X-RapidAPI-Proxy-Secret` or `X-API-Gateway-Secret`. This prevents direct backend use outside the paid marketplace.

## Suggested Endpoint Highlights

- `/deals/search`: Generate World Cup travel package candidates with safe booking links and deal scores.
- `/cities`: Explore all host cities, airports, stadiums, demand levels, and match windows.
- `/score`: Score a real flight/hotel/package offer against a baseline.
- `/official-links`: FIFA official tickets, hospitality, and resale/exchange guidance.

## Required Listing Improvements

- Add a spotlight linking to the public product page.
- Add a tutorial showing a World Cup city comparison workflow.
- Add example responses that clearly display `pricing_context`.
- Emphasize provider routes, buyer-supplied offers, and normalized deal scoring.
