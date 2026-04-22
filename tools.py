import requests
from datetime import datetime
from langchain.tools import tool

# ── Tool 1: Current Time ──────────────────────────────────────────────────────
# The @tool decorator tells LangChain this function is a tool the agent can call
@tool
def get_current_time(timezone: str = "local") -> str:
    """Returns the current date and time. Input can be a timezone name like 'US/Eastern', 'US/Pacific', or 'local'."""
    now = datetime.now()
    return f"Current time ({timezone}): {now.strftime('%A, %B %d, %Y at %H:%M:%S')}"

# ── Tool 2: Weather ───────────────────────────────────────────────────────────
# wttr.in is a free weather service — no API key needed, just a simple HTTP call
@tool
def get_weather(city: str) -> str:
    """Gets the current weather for a given city. Input should be a city name."""
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        result = response.text.strip()

        # wttr.in returns "Unknown location" or empty for bad city names
        if not result or "Unknown location" in result or len(result) < 5:
            return f"I couldn't find a city called '{city}'. Please check your spelling and try again."

        return result
    except Exception as e:
        return f"Couldn't fetch weather right now. Please try again in a moment."
