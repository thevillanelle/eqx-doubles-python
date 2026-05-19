# Procfile — tells Railway (and Heroku-compatible platforms) how to start the app.
#
# "web:" means this is a web process (HTTP server).
# `gunicorn` is a production-grade Python web server — much more robust than
# Flask's built-in development server (`app.run()`).
#
# Flask's dev server is fine on your laptop, but it's single-threaded and not
# designed to handle real internet traffic. Gunicorn can handle multiple
# concurrent requests.
#
# The format is:  gunicorn <module_name>:<flask_app_variable>
# Our module is `app.py` → module name is `app`
# Our Flask app variable is `app` (the line: app = Flask(__name__))
web: gunicorn app:app
