from functools import partial
from flask import Blueprint, Response, render_template, jsonify
from .providers import (
	funimation,
	hidive,
	toonami,
	crunchyroll,
)

calendar_response = partial(Response, mimetype="text/calendar")

views = Blueprint("views", __name__, url_prefix="/")

@views.route('/')
def index():
  return render_template("index.html")

@views.route('/crunchyroll.ics')
def crunchyroll_cal():
	ical = crunchyroll.get_calendar().to_ical()
	return calendar_response(response=ical)

@views.route('/crunchyroll.json')
def crunchyroll_json():
	return jsonify(list(crunchyroll.get_events()))

@views.route('/funimation.ics')
def funimation_cal():
	ical = funimation.get_calendar().to_ical()
	return calendar_response(response=ical)

@views.route('/funimation.json')
def funimation_json():
	return jsonify(list(funimation.get_events()))

@views.route('/hidive.ics')
def hidive_cal():
	ical = hidive.get_calendar().to_ical()
	return calendar_response(response=ical)

@views.route('/hidive.json')
def hidive_json():
	return jsonify(list(hidive.get_events()))

@views.route('/toonami.ics')
def toonami_cal():
	ical = toonami.get_calendar().to_ical()
	return calendar_response(response=ical)

@views.route('/toonami.json')
def toonami_json():
	return jsonify(list(toonami.get_events()))

