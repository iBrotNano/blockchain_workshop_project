from datetime import datetime


striped_str_is_not_empty = lambda text: bool(text.strip())


def iso8601_str_is_valid(value: str) -> bool:
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False
