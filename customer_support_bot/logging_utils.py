from datetime import datetime, UTC

LOGS = []

def log(event_type: str, details: dict):
    entry = {
        "time": datetime.now(UTC).isoformat(),
        "type": event_type,
        "details": details,
    }
    LOGS.append(entry)
    print("LOG:", entry)
