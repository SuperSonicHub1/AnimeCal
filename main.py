"""TODO:
* change show_name to show_title
* create an Episode TypedDict
"""

from animecal import create_app

app = create_app()
app.run(host='0.0.0.0', port=8080)
