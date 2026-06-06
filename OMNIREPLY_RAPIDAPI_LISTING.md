# OmniReplyAIAPI RapidAPI Listing Draft

## Title

OmniReply AI API

## Short Description

Paid multilingual AI reply API for WhatsApp, Telegram, Messenger, Instagram,
webchat, SMS and email customer-service workflows.

## Long Description

OmniReplyAIAPI helps businesses answer customers faster across WhatsApp,
Telegram, Messenger, Instagram, webchat, SMS and email.

Send a customer message plus a business profile and receive:

- polished multilingual reply text
- detected language
- detected intent
- sentiment
- confidence score
- quick replies
- escalation flag
- recommended next action
- safety note for sensitive conversations

Use it for small-business support, ecommerce questions, sales qualification,
appointment booking, FAQ automation, agency chat tools, CRM inboxes and AI
assistant workflows.

Commercial endpoints are paid-gateway protected. The API does not expose a free
direct backend endpoint. Real outbound WhatsApp, Messenger, Instagram or
Telegram sending requires the buyer's own official channel credentials.

## Suggested Category

Artificial Intelligence, Messaging, Customer Support, Business, Automation.

## Tags

whatsapp bot, telegram bot, ai customer support, multilingual chatbot,
messenger automation, instagram dm automation, business replies, ecommerce
support, crm inbox, ai agent, webchat, sms, email automation

## Recommended Plans

No free tier.

| Plan | Price | Requests |
| --- | ---: | ---: |
| Starter | USD 7.99/month | 2,000 |
| Growth | USD 29.99/month | 20,000 |
| Business | USD 79.99/month | 75,000 |
| Agency | USD 199/month | 250,000 |

## Base URL

```text
https://worldcup-travel-deals-api.onrender.com/omni
```

## Main Endpoints

- `GET /health`
- `POST /reply`
- `POST /batch/reply`
- `GET /channels`
- `POST /webhooks/telegram/{tenant_id}`
- `GET /webhooks/meta/{tenant_id}`
- `POST /webhooks/meta/{tenant_id}`
- `GET /openapi.json`

## Security

Configure RapidAPI to send the gateway secret to one of these headers:

- `X-RapidAPI-Proxy-Secret`
- `X-API-Gateway-Secret`
- `X-OmniReplyAI-Secret`

Do not publish gateway secrets, Meta tokens, Telegram bot tokens, cookies or
browser session tokens.
