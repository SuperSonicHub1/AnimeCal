from datetime import datetime
import json
import re
from ..session import session
from ..calendar import create_calendar

SCHEDULE_URL = "https://www.funimation.com/schedule/table/streaming/"
_JSON_REXEX = r"var scheduleItems = (.*);"

def _parse_events(item: dict) -> dict:
	internal_item = item["item"]

	show_slug = internal_item["titleSlug"]
	episode_slug = internal_item["episodeSlug"]

	thumbnail = item["image"]
	available_time = datetime.fromisoformat(item["startDate"])
	episode_number = internal_item["episodeNum"]
	episode_title = internal_item["episodeName"]
	season_number = int(internal_item["seasonOrder"])

	show_name = " ".join([internal_item["titleName"], internal_item["seasonTitle"]])
	show_url = f"https://www.funimation.com/en/shows/{show_slug}/"
	episode_url = show_url + episode_slug
	uid = "/".join([show_slug, episode_slug])

	
	return {
		"show_name": show_name,
		"show_slug": show_slug,
		"show_url": show_url,
		"season_number": season_number,
		"episode_title": episode_title,
		"episode_slug": episode_slug,
		"episode_number": episode_number,
		"episode_url": episode_url,
		"description": None,
		"available_time": available_time,
		"thumbnail": thumbnail,
		"uid": uid,
		"_original": item,
	}

def get_events():
	res = session.get(SCHEDULE_URL)
	res.raise_for_status()
	text = res.text
	matches = re.search(_JSON_REXEX, text)

	if not matches:
		return []

	parsed_events = json.loads(matches.group(1))

	events = map(_parse_events, parsed_events)

	return events


def get_calendar():
	return create_calendar("Funimation", get_events())
