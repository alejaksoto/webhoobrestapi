def handle_incoming_message(message, sender_info):
    sender_id = sender_info.get("wa_id")
    text = message.get("text", {}).get("body")

    if sender_id and text:
        print(f"Mensaje recibido de {sender_id}: {text}")
