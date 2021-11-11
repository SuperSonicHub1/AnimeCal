import json
from selectolax.parser import HTMLParser
from datetime import datetime
from ..calendar import create_calendar
from ..session import session

SCHEDULE_URL = "https://www.adultswim.com/videos/toonami"

def _parse_events(item: dict, apollo_state: dict) -> dict:
	show_slug = item["show"]["id"]
	show = apollo_state[show_slug]

	show_name = show["title"]
	show_url = f"https://www.adultswim.com/videos/{show_slug}"
	# Gotta remove that Z
	start_time = item["startTime"]
	available_time = datetime.fromisoformat(start_time[:-1])
	episode_title = item["title"]

	uid = "/".join([show_slug, start_time])

	# For the completeness of _original
	item["showObject"] = show

	return {
		"show_name": show_name,
		"show_slug": show_slug,
		"show_url": show_url,
		"season_number": None,
		"episode_title": episode_title,
		"episode_slug": None,
		"episode_number": None,
		"episode_url": show_url,
		"description": None,
		"available_time": available_time,
		"thumbnail": None,
		"uid": uid,
		"_original": item,
	}

def get_events():
	res = session.get(SCHEDULE_URL)
	res.raise_for_status()
	text = res.text
	tree = HTMLParser(text)
	
	next_data_element = tree.css_first("script#__NEXT_DATA__")
	
	if not next_data_element:
		return []

	next_data = json.loads(next_data_element.text())
	apollo_state = next_data["props"]["pageProps"]["__APOLLO_STATE__"]
	
	schedule_nodes = {
		k: v
		for k, v
		in apollo_state.items()
		if "schedule.nodes" in k
	}

	events = map(lambda x: _parse_events(x, apollo_state), schedule_nodes.values())

	return events


def get_calendar():
	return create_calendar("Toonami", get_events())
