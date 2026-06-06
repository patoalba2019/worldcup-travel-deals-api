from __future__ import annotations

import hmac
import os
import re
from datetime import UTC, datetime
from typing import Any

from flask import Blueprint, jsonify, request


OMNI_API_NAME = "OmniReplyAIAPI"
OMNI_API_VERSION = "1.0.0"
SUPPORTED_CHANNELS = {
    "whatsapp",
    "telegram",
    "messenger",
    "instagram",
    "webchat",
    "sms",
    "email",
    "meta",
}
SUPPORTED_LOCALES = {"en", "es", "pt", "fr", "it", "de", "ja"}
MAX_CONTEXT_MESSAGES = int(os.environ.get("OMNI_MAX_CONTEXT_MESSAGES", "12"))
MAX_BATCH_SIZE = int(os.environ.get("OMNI_MAX_BATCH_SIZE", "25"))

omni_blueprint = Blueprint("omnireply", __name__, url_prefix="/omni")


LANGUAGE_HINTS = {
    "es": (
        "hola",
        "precio",
        "cuanto",
        "cuánto",
        "envio",
        "envío",
        "turno",
        "horario",
        "gracias",
        "reclamo",
        "comprar",
        "necesito",
    ),
    "en": (
        "hello",
        "price",
        "how much",
        "shipping",
        "hours",
        "appointment",
        "refund",
        "thanks",
        "buy",
        "need",
    ),
    "pt": ("olá", "preço", "quanto", "envio", "horário", "obrigado", "comprar"),
    "fr": ("bonjour", "prix", "combien", "livraison", "horaire", "merci", "acheter"),
    "it": ("ciao", "prezzo", "quanto", "spedizione", "orario", "grazie", "comprare"),
    "de": ("hallo", "preis", "versand", "öffnungszeiten", "danke", "kaufen"),
    "ja": ("こんにちは", "価格", "値段", "配送", "営業時間", "ありがとう", "購入"),
}

INTENT_KEYWORDS = {
    "greeting": ("hola", "hello", "hi", "buenas", "bonjour", "olá", "ciao", "hallo", "こんにちは"),
    "pricing": (
        "precio",
        "price",
        "cost",
        "cuanto",
        "cuánto",
        "tarifa",
        "plan",
        "quote",
        "budget",
        "cotizacion",
        "cotización",
        "valor",
    ),
    "hours": ("horario", "hours", "open", "cerrado", "abierto", "opening", "schedule"),
    "location": ("direccion", "dirección", "address", "ubicacion", "ubicación", "location", "where", "donde", "dónde"),
    "shipping": ("envio", "envío", "shipping", "delivery", "entrega", "ship", "tracking"),
    "appointment": ("turno", "appointment", "reserva", "booking", "agendar", "schedule", "cita"),
    "refund": ("devolucion", "devolución", "refund", "return", "cancel", "cancelar", "reembolso"),
    "complaint": ("reclamo", "complaint", "angry", "molesto", "malo", "bad", "terrible", "estafa", "scam"),
    "human": ("humano", "asesor", "representante", "human", "agent", "persona", "manager"),
    "thanks": ("gracias", "thanks", "thank you", "merci", "obrigado", "grazie", "danke"),
}

NEGATIVE_HINTS = (
    "angry",
    "terrible",
    "malo",
    "malisimo",
    "malísimo",
    "estafa",
    "scam",
    "fraud",
    "reclamo",
    "complaint",
    "cancelar",
)

DEFAULT_BUSINESS = {
    "business_name": "the business",
    "tone": "professional",
    "hours": "",
    "location": "",
    "pricing_note": "",
    "shipping_note": "",
    "appointment_url": "",
    "human_handoff": "",
}

REPLY_TEMPLATES = {
    "en": {
        "greeting": "Hi, thanks for contacting {business_name}. How can I help you today?",
        "pricing": "Thanks for asking. {pricing_note} If you tell me what you need, I can guide you to the best option.",
        "hours": "Our current hours are: {hours}.",
        "location": "You can find us here: {location}.",
        "shipping": "{shipping_note} Share your order number or destination and I can help you check the next step.",
        "appointment": "I can help you schedule it. {appointment_url}",
        "refund": "I am sorry about that. Please send the order number and what happened so we can review the case.",
        "complaint": "I am sorry this happened. I will collect the details and escalate it to a person if needed.",
        "human": "Of course. {human_handoff}",
        "thanks": "You are welcome. I am here if you need anything else.",
        "general": "Thanks for writing. Could you share a little more detail so I can help you correctly?",
    },
    "es": {
        "greeting": "Hola, gracias por contactar a {business_name}. ¿En qué puedo ayudarte?",
        "pricing": "Gracias por consultar. {pricing_note} Si me cuentas qué necesitas, te oriento con la mejor opción.",
        "hours": "Nuestro horario actual es: {hours}.",
        "location": "Puedes encontrarnos aquí: {location}.",
        "shipping": "{shipping_note} Envíame tu número de pedido o destino y reviso el próximo paso.",
        "appointment": "Puedo ayudarte a agendarlo. {appointment_url}",
        "refund": "Lamento lo ocurrido. Envíame el número de pedido y qué pasó para revisar el caso.",
        "complaint": "Lamento que haya pasado esto. Voy a tomar los datos y escalarlo con una persona si hace falta.",
        "human": "Claro. {human_handoff}",
        "thanks": "De nada. Estoy aquí por si necesitas algo más.",
        "general": "Gracias por escribir. ¿Puedes contarme un poco más para ayudarte correctamente?",
    },
    "pt": {
        "greeting": "Olá, obrigado por entrar em contato com {business_name}. Como posso ajudar?",
        "pricing": "Obrigado pela pergunta. {pricing_note} Conte o que você precisa e eu indico a melhor opção.",
        "hours": "Nosso horário atual é: {hours}.",
        "location": "Você pode nos encontrar aqui: {location}.",
        "shipping": "{shipping_note} Envie o número do pedido ou destino para eu ajudar com o próximo passo.",
        "appointment": "Posso ajudar a agendar. {appointment_url}",
        "refund": "Sinto muito por isso. Envie o número do pedido e o que aconteceu para avaliarmos.",
        "complaint": "Sinto muito pelo ocorrido. Vou coletar os detalhes e encaminhar para uma pessoa se necessário.",
        "human": "Claro. {human_handoff}",
        "thanks": "De nada. Estou aqui se precisar de algo mais.",
        "general": "Obrigado por escrever. Pode enviar mais detalhes para eu ajudar corretamente?",
    },
    "fr": {"general": "Merci pour votre message. Pouvez-vous partager plus de details afin que je vous aide correctement?"},
    "it": {"general": "Grazie per il messaggio. Puoi condividere qualche dettaglio in piu per aiutarti correttamente?"},
    "de": {"general": "Danke fuer Ihre Nachricht. Koennen Sie bitte mehr Details teilen, damit ich richtig helfen kann?"},
    "ja": {"general": "お問い合わせありがとうございます。正しくご案内するため、もう少し詳しく教えてください。"},
}


def omni_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def detect_language(text: str, requested_locale: str | None = None) -> str:
    if requested_locale:
        requested = requested_locale.lower().split("-")[0]
        if requested in SUPPORTED_LOCALES:
            return requested
    lowered = text.lower()
    scores = {
        locale: sum(1 for hint in hints if hint in lowered)
        for locale, hints in LANGUAGE_HINTS.items()
    }
    best_locale, best_score = max(scores.items(), key=lambda item: item[1])
    if best_score:
        return best_locale
    if re.search(r"[áéíóúñ¿¡]", lowered):
        return "es"
    return "en"


def classify_intent(text: str) -> tuple[str, float]:
    lowered = text.lower()
    scores = {
        intent: sum(1 for keyword in keywords if keyword in lowered)
        for intent, keywords in INTENT_KEYWORDS.items()
    }
    if scores.get("greeting") and any(
        score for intent, score in scores.items() if intent not in {"greeting", "thanks"}
    ):
        scores["greeting"] = 0
    best_intent, score = max(scores.items(), key=lambda item: item[1])
    if not score:
        return "general", 0.54
    return best_intent, round(min(0.95, 0.62 + score * 0.11), 2)


def detect_sentiment(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in NEGATIVE_HINTS):
        return "negative"
    if any(word in lowered for word in ("gracias", "thanks", "excelente", "great", "perfecto")):
        return "positive"
    return "neutral"


def clean_business_profile(payload: dict[str, Any]) -> dict[str, Any]:
    profile = dict(DEFAULT_BUSINESS)
    raw_profile = payload.get("business") or payload.get("business_profile") or {}
    if isinstance(raw_profile, dict):
        for key in DEFAULT_BUSINESS:
            if raw_profile.get(key) not in (None, ""):
                profile[key] = raw_profile[key]
    profile["pricing_note"] = profile["pricing_note"] or "Pricing depends on the selected product or service."
    profile["hours"] = profile["hours"] or "please check the latest business hours with our team"
    profile["location"] = profile["location"] or "our official business location or online store"
    profile["shipping_note"] = profile["shipping_note"] or "Shipping or delivery depends on the destination and selected service."
    profile["appointment_url"] = profile["appointment_url"] or "Please share your preferred day and time."
    profile["human_handoff"] = profile["human_handoff"] or "A team member will continue the conversation as soon as possible."
    return profile


def apply_tone(reply: str, tone: str) -> str:
    tone = normalize_text(tone).lower()
    if tone in {"short", "concise", "breve"}:
        return reply.split(". ")[0].strip() + "."
    if tone in {"formal", "corporate", "profesional"}:
        return reply.replace("Hi,", "Hello,")
    return reply


def fill_template(locale: str, intent: str, profile: dict[str, Any]) -> str:
    templates = REPLY_TEMPLATES.get(locale, REPLY_TEMPLATES["en"])
    template = templates.get(intent) or templates.get("general") or REPLY_TEMPLATES["en"]["general"]
    return apply_tone(template.format(**profile), str(profile.get("tone", "")))


def quick_replies(locale: str, intent: str) -> list[str]:
    if locale == "es":
        options = {
            "pricing": ["Ver planes", "Hablar con ventas", "Enviar detalle"],
            "shipping": ["Enviar pedido", "Consultar entrega", "Hablar con soporte"],
            "appointment": ["Agendar turno", "Cambiar horario", "Hablar con asesor"],
            "complaint": ["Enviar reclamo", "Hablar con una persona", "Adjuntar datos"],
            "general": ["Ver opciones", "Hablar con una persona", "Enviar más detalles"],
        }
    else:
        options = {
            "pricing": ["View plans", "Talk to sales", "Send details"],
            "shipping": ["Send order", "Check delivery", "Talk to support"],
            "appointment": ["Book time", "Change time", "Talk to advisor"],
            "complaint": ["Send complaint", "Talk to a person", "Add details"],
            "general": ["View options", "Talk to a person", "Send more details"],
        }
    return options.get(intent, options["general"])


def should_escalate(intent: str, sentiment: str, confidence: float, text: str) -> bool:
    lowered = text.lower()
    high_risk = any(
        phrase in lowered
        for phrase in ("legal", "lawyer", "abogado", "demanda", "medical", "doctor", "emergency", "urgencia", "fraud", "estafa")
    )
    return intent in {"human", "complaint", "refund"} or sentiment == "negative" or confidence < 0.58 or high_risk


def build_reply(payload: dict[str, Any]) -> dict[str, Any]:
    channel = normalize_text(payload.get("channel", "webchat")).lower() or "webchat"
    if channel not in SUPPORTED_CHANNELS:
        channel = "webchat"
    message = normalize_text(payload.get("message") or payload.get("text"))
    context = payload.get("context") if isinstance(payload.get("context"), list) else []
    context = context[-MAX_CONTEXT_MESSAGES:]
    context_text = " ".join(normalize_text(item.get("text") if isinstance(item, dict) else item) for item in context)
    combined = normalize_text(f"{context_text} {message}")
    locale = detect_language(combined, payload.get("locale") or payload.get("language"))
    intent, confidence = classify_intent(combined)
    sentiment = detect_sentiment(combined)
    profile = clean_business_profile(payload)
    escalation = should_escalate(intent, sentiment, confidence, combined)
    return {
        "api": OMNI_API_NAME,
        "version": OMNI_API_VERSION,
        "generated_at": omni_now_iso(),
        "channel": channel,
        "locale": locale,
        "detected_language": locale,
        "intent": intent,
        "sentiment": sentiment,
        "confidence": confidence,
        "reply": fill_template(locale, intent, profile),
        "quick_replies": quick_replies(locale, intent),
        "escalation_required": escalation,
        "recommended_action": "human_handoff" if escalation else "send_reply",
        "safety": {
            "contains_sensitive_data": bool(re.search(r"\b\d{12,19}\b", combined)),
            "policy_note": "Do not send irreversible, legal, medical, financial or account-changing answers without human review.",
        },
        "metadata": {
            "input_length": len(message),
            "context_messages": len(context),
        },
    }


def extract_telegram_message(update: dict[str, Any]) -> dict[str, Any]:
    msg = (
        update.get("message")
        or update.get("edited_message")
        or update.get("business_message")
        or update.get("channel_post")
        or {}
    )
    user = msg.get("from", {}) if isinstance(msg, dict) else {}
    chat = msg.get("chat", {}) if isinstance(msg, dict) else {}
    return {
        "channel": "telegram",
        "message": normalize_text(msg.get("text") or msg.get("caption") or ""),
        "locale": user.get("language_code"),
        "source": {
            "update_id": update.get("update_id"),
            "chat_id": chat.get("id"),
            "message_id": msg.get("message_id"),
            "username": user.get("username"),
        },
    }


def extract_meta_messages(payload: dict[str, Any]) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            metadata = value.get("metadata", {})
            for message in value.get("messages", []):
                text = message.get("text", {}).get("body") or message.get("button", {}).get("text") or ""
                messages.append(
                    {
                        "channel": "whatsapp",
                        "message": normalize_text(text),
                        "source": {
                            "message_id": message.get("id"),
                            "from": message.get("from"),
                            "phone_number_id": metadata.get("phone_number_id"),
                            "change_field": change.get("field"),
                        },
                    }
                )
    for entry in payload.get("entry", []):
        for event in entry.get("messaging", []):
            text = event.get("message", {}).get("text") or event.get("postback", {}).get("title") or ""
            messages.append(
                {
                    "channel": "messenger",
                    "message": normalize_text(text),
                    "source": {
                        "sender_id": event.get("sender", {}).get("id"),
                        "recipient_id": event.get("recipient", {}).get("id"),
                        "timestamp": event.get("timestamp"),
                    },
                }
            )
    return [message for message in messages if message.get("message")]


def verify_telegram_secret(tenant_id: str) -> bool:
    expected = (
        os.environ.get(f"TELEGRAM_WEBHOOK_SECRET_{tenant_id.upper().replace('-', '_')}")
        or os.environ.get("TELEGRAM_WEBHOOK_SECRET")
    )
    provided = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    return bool(expected and hmac.compare_digest(provided, expected))


def verify_meta_token(tenant_id: str, token: str) -> bool:
    expected = (
        os.environ.get(f"META_VERIFY_TOKEN_{tenant_id.upper().replace('-', '_')}")
        or os.environ.get("META_VERIFY_TOKEN")
    )
    return bool(expected and hmac.compare_digest(token, expected))


@omni_blueprint.get("/")
def omni_index():
    return jsonify(
        {
            "api": OMNI_API_NAME,
            "version": OMNI_API_VERSION,
            "message": "Paid multilingual AI reply API for business messaging channels.",
            "health": "/omni/health",
            "openapi": "/omni/openapi.json",
            "commercial_endpoints": ["/omni/reply", "/omni/batch/reply", "/omni/channels"],
        }
    )


@omni_blueprint.get("/health")
def omni_health():
    return jsonify(
        {
            "api": OMNI_API_NAME,
            "version": OMNI_API_VERSION,
            "status": "ok",
            "updated_at": omni_now_iso(),
            "channels": sorted(SUPPORTED_CHANNELS),
            "locales": sorted(SUPPORTED_LOCALES),
        }
    )


@omni_blueprint.get("/channels")
def omni_channels():
    return jsonify(
        {
            "channels": [
                {
                    "id": channel,
                    "label": channel.title(),
                    "supports_webhook_normalization": channel in {"telegram", "whatsapp", "messenger", "instagram", "meta"},
                }
                for channel in sorted(SUPPORTED_CHANNELS)
            ],
            "locales": sorted(SUPPORTED_LOCALES),
        }
    )


@omni_blueprint.post("/reply")
def omni_reply():
    payload = request.get_json(silent=True) or {}
    if not normalize_text(payload.get("message") or payload.get("text")):
        return jsonify({"error": "message_required", "message": "Provide message or text."}), 400
    return jsonify(build_reply(payload))


@omni_blueprint.post("/batch/reply")
def omni_batch_reply():
    payload = request.get_json(silent=True) or {}
    items = payload.get("messages")
    if not isinstance(items, list) or not items:
        return jsonify({"error": "messages_required", "message": "Provide a non-empty messages list."}), 400
    if len(items) > MAX_BATCH_SIZE:
        return jsonify({"error": "batch_too_large", "max_batch_size": MAX_BATCH_SIZE}), 400
    business = payload.get("business") or payload.get("business_profile") or {}
    results = []
    for item in items:
        item_payload = {"message": item} if isinstance(item, str) else dict(item or {})
        item_payload.setdefault("business", business)
        item_payload.setdefault("locale", payload.get("locale"))
        results.append(build_reply(item_payload))
    return jsonify({"api": OMNI_API_NAME, "count": len(results), "results": results})


@omni_blueprint.post("/webhooks/telegram/<tenant_id>")
def omni_telegram_webhook(tenant_id: str):
    if not verify_telegram_secret(tenant_id):
        return jsonify({"error": "invalid_telegram_webhook_secret"}), 403
    update = request.get_json(silent=True) or {}
    normalized = extract_telegram_message(update)
    if not normalized["message"]:
        return jsonify({"ok": True, "ignored": True, "reason": "no_text_message"})
    result = build_reply({"business": {"business_name": os.environ.get("DEFAULT_BUSINESS_NAME", "the business")}, **normalized})
    response = {"ok": True, "normalized": normalized, "reply": result}
    if request.args.get("telegram_inline_method") == "true" and normalized.get("source", {}).get("chat_id"):
        response["telegram_method"] = {
            "method": "sendMessage",
            "chat_id": normalized["source"]["chat_id"],
            "text": result["reply"],
        }
    return jsonify(response)


@omni_blueprint.get("/webhooks/meta/<tenant_id>")
def omni_meta_webhook_verify(tenant_id: str):
    mode = request.args.get("hub.mode", "")
    token = request.args.get("hub.verify_token", "")
    challenge = request.args.get("hub.challenge", "")
    if mode == "subscribe" and verify_meta_token(tenant_id, token):
        return challenge, 200, {"Content-Type": "text/plain"}
    return jsonify({"error": "invalid_meta_verify_token"}), 403


@omni_blueprint.post("/webhooks/meta/<tenant_id>")
def omni_meta_webhook_post(tenant_id: str):
    token = request.args.get("verify_token") or request.headers.get("X-Meta-Verify-Token", "")
    if token and not verify_meta_token(tenant_id, token):
        return jsonify({"error": "invalid_meta_verify_token"}), 403
    payload = request.get_json(silent=True) or {}
    normalized_messages = extract_meta_messages(payload)
    replies = [
        build_reply(
            {
                **item,
                "business": {"business_name": os.environ.get("DEFAULT_BUSINESS_NAME", "the business")},
            }
        )
        for item in normalized_messages
    ]
    return jsonify({"ok": True, "count": len(replies), "messages": normalized_messages, "replies": replies})


@omni_blueprint.get("/openapi.json")
def omni_openapi():
    return jsonify(
        {
            "openapi": "3.0.3",
            "info": {
                "title": OMNI_API_NAME,
                "version": OMNI_API_VERSION,
                "description": "Paid multilingual AI reply API for WhatsApp, Telegram, Messenger, Instagram, webchat, SMS and email workflows.",
            },
            "servers": [{"url": "https://worldcup-travel-deals-api.onrender.com/omni"}],
            "paths": {
                "/health": {"get": {"summary": "Public health check", "responses": {"200": {"description": "OK"}}}},
                "/reply": {"post": {"summary": "Generate one business reply", "responses": {"200": {"description": "Reply generated"}, "402": {"description": "Payment required"}}}},
                "/batch/reply": {"post": {"summary": "Generate multiple business replies", "responses": {"200": {"description": "Replies generated"}, "402": {"description": "Payment required"}}}},
                "/webhooks/telegram/{tenant_id}": {"post": {"summary": "Normalize Telegram webhook update", "responses": {"200": {"description": "Webhook processed"}}}},
                "/webhooks/meta/{tenant_id}": {"get": {"summary": "Meta webhook verification challenge"}, "post": {"summary": "Normalize WhatsApp and Messenger webhook payloads"}},
            },
        }
    )
