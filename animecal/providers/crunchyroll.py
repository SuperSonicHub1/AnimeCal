"""Crunchyroll has Cloudflare DDOS protection, so I can't do anything.
Until that changes, this will act as an archive.
"""

from datetime import datetime
from os.path import split
from selectolax.parser import HTMLParser, Node
from ..session import session
from ..calendar import create_calendar


SCHEDULE_URL = "https://cc.bingj.com/cache.aspx?d=4582189182750113&w=cSvvUercM4MjvWhlVn6b4QDYZ81pMSsj"

def _parse_release_html(node: Node) -> dict:
	# Episode number, show slug
	# Don't convert the episode number to an int, you can
	# run into stuff like "SP3"
	episode_number = node.attributes["data-episode-num"]
	show_slug = node.attributes["data-slug"]
	
	# Available time
	available_time_node = node.css_first("time.available-time")
	available_time = datetime.fromisoformat(available_time_node.attributes["datetime"])

	# Season name and URL
	# season_name_node = node.css_first("h1.season-name")
	season_link = node.css_first("a.js-season-name-link")
	show_url = season_link.css_first("a.js-season-name-link").attributes["href"]
	show_name = season_link.text(strip=True)

	# Episode URL and thumbnail
	# featured_episode_node = node.css_first("article.featured-episode")	
	featured_episode_title = node.css_first("article.featured-episode h1")
	episode_title = featured_episode_title.text(strip=True) if featured_episode_title else None
	episode_url = node.css_first("a.episode-info").attributes["href"]
	episode_slug = split(episode_url)[1]
	thumbnail = node.css_first("img.thumbnail").attributes["src"]
	uid = "/".join([show_slug, episode_slug])

	return {
		"show_name": show_name,
		"show_slug": show_slug,
		"show_url": show_url,
		"season_number": None,
		"episode_slug": episode_slug,
		"episode_title": episode_title,
		"episode_number": episode_number,
		"episode_url": episode_url,
		"description": None,
		"available_time": available_time,
		"thumbnail": thumbnail, 
		"uid": uid,
	}

def get_events() -> dict:
	res = session.get(SCHEDULE_URL)
	res.raise_for_status()
	text = res.text
	tree = HTMLParser(text)
	events = map(_parse_release_html, tree.css("article.release"))
	return events

def get_calendar():
	return create_calendar("Crunchyroll", get_events())
