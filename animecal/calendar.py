from datetime import timedelta
from icalendar import Calendar, Event
from typing import Iterable

THIRTY_MINUTES = timedelta(minutes=30)

def create_event(info: dict) -> Event:
	event = Event()
	event.add('dtstart', info["available_time"])
	event.add('dtend', info["available_time"] + THIRTY_MINUTES)
	event.add('location', info['episode_url'])
	event.add('uid', info["uid"])

	summary = info['show_name']
	season_episode = f"{'S' + str(info['season_number']) if info['season_number'] else ''}{'E' + str(info['episode_number']) if info['episode_number'] else ''}"
	if season_episode:
		summary += " " + season_episode
	if info["episode_title"]:
		summary += ": " + info["episode_title"]
	event.add('summary', summary)

	if info["description"]: 
		event.add('description', info["description"])

	return event

def create_calendar(name: str, events: Iterable[dict]):
	cal = Calendar()
	cal.add('prodid', '-//KAWCCO (@supersonichub1)/EN')
	cal.add('version', '2.0')
	cal.add('name', f'{name} Schedule')
	cal.add("method", "PUBLISH")

	for event in map(create_event, events):
		cal.add_component(event)
	
	return cal
