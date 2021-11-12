import json
from selectolax.parser import HTMLParser
from datetime import datetime
from ..calendar import create_calendar
from ..session import session

SCHEDULE_URL = "https://www.adultswim.com/videos/toonami"

def _parse_events(item: dict, apollo_state: dict) -> dict:
	schedule_item = {
		"season_number": None,
		"episode_slug": None,
		"episode_number": None,
		"description": None,
		"thumbnail": None,
	}

	# Why is dict.get not working?
	show_slug = (item.get("show") or {}).get("id") or ""
	if show_slug:
		show = apollo_state[show_slug]
		schedule_item["show_name"] = show["title"]
		schedule_item["show_url"] = f"https://www.adultswim.com/videos/{show_slug}"
		schedule_item["episode_title"] = item["title"]
		# For the completeness of _original
		item["showObject"] = show
		schedule_item["_original"] = item
	else:
		schedule_item["show_name"] = item["title"]
		schedule_item["show_url"] = f"https://www.adultswim.com/videos"
		schedule_item["episode_title"] = None

	schedule_item["episode_url"] = schedule_item["show_url"]

	start_time = item["startTime"]
	# Gotta remove that Z
	schedule_item["available_time"] = datetime.fromisoformat(start_time[:-1])
	schedule_item["uid"] = "/".join([show_slug, start_time])

	return schedule_item

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
