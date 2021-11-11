# ADD HIDIVE: https://www.hidive.com/schedule
# TODO: Look into API usage: https://github.com/BeeeQueue/yuna/blob/master/src/lib/hidive.ts
from datetime import datetime
from os.path import split
import re
from dateutil import parser
from dateutil.relativedelta import relativedelta
from selectolax.parser import HTMLParser, Node
from ..calendar import create_calendar
from ..session import session

_EPISODE_SLUG_REGEX = r"s(\d*)e(\d*)"
ROOT_URL = "https://www.hidive.com"
SCHEDULE_URL = "https://www.hidive.com/schedule"
A_YEAR = relativedelta(years=1)

def _parse_events(item: Node) -> dict:
	episode_title = item.css_first("h4.episode").attributes["data-original-title"]
	description = item.css_first("p.summary").text(strip=True)
	thumbnail = "https:" + item.css_first("div.showImg img").attributes["src"]

	now = datetime.now()
	
	airdate = item.parent.parent.css_first("h3 small").text()
	airtime = item.css_first("div.ribbon").text()
	available_time = parser.parse(" ".join([airdate, airtime]))
	# Accounting for month overflow when scraping the December calendar and it includes a little bit of January
	if available_time.month < now.month and available_time.month == 1:
		available_time = available_time + A_YEAR

	title = item.css_first("h4.title")
	partial_show_url = title.css_first("a").attributes["href"]
	show_name = title.text()
	show_url = ROOT_URL + partial_show_url
	show_slug = split(partial_show_url)[1]

	partial_episode_url = item.css_first("div.player a").attributes["href"]
	episode_url = ROOT_URL + partial_episode_url
	episode_slug = split(partial_episode_url)[1]

	matches = re.search(_EPISODE_SLUG_REGEX, episode_slug)
	season_number, episode_number = (int(matches.group(1)), int(matches.group(2))) if matches else (None, None)

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
		"description": description,
		"available_time": available_time,
		"thumbnail": thumbnail,
		"uid": uid,
	}

def get_events():
	res = session.get(SCHEDULE_URL)
	res.raise_for_status()
	text = res.text
	tree = HTMLParser(text)

	events = map(_parse_events, tree.css("section.listing"))

	return events


def get_calendar():
	return create_calendar("HIDIVE", get_events())
