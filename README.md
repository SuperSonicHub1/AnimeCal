# AnimeCal

Simplified access to the schedules of American anime distribution networks through iCalendar and JSON.

## Supported Networks
* Crunchyroll
* Funimation
* HIDIVE
* Toonami by Adult Swim
If you have any suggestions, open an issue.

## Install
```bash
poetry install
# For the lazy...
python3 main.py 
# For the more upstanding
gunicorn 'animecal:create_app()'
```
