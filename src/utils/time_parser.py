from datetime import datetime, timedelta

def parse_time(time_str: str) -> datetime:
    """Parse time string into datetime"""
    try:
        if time_str.endswith('h'):
            hours = int(time_str[:-1])
            return datetime.utcnow() - timedelta(hours=hours)
        elif time_str.endswith('d'):
            days = int(time_str[:-1])
            return datetime.utcnow() - timedelta(days=days)
        return None
    except ValueError:
        return None