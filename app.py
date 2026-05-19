# =============================================================================
# app.py  —  EQX Doubles Finder (Python + Flask edition)
# =============================================================================
#
# WHAT IS PYTHON?
# ---------------
# Python is a programming language — a set of rules for writing instructions
# that a computer can execute. Unlike languages such as Swift, Go, or C++,
# Python is *interpreted*, which means there is NO build step. You write a
# .py file, run `python app.py`, and the Python interpreter reads your file
# line by line, top to bottom, and executes each instruction immediately.
#
# WHAT IS A .py FILE?
# --------------------
# A .py file is just a plain text file containing Python source code. Your
# code editor shows it with syntax highlighting, but underneath it's the same
# as any .txt file. The .py extension tells the operating system (and your
# editor) that this file contains Python code.
#
# WHAT DOES "INTERPRETED" MEAN?
# ------------------------------
# Imagine two ways to translate a book from French to English:
#
#   Compiled  → Hire a translator to convert the ENTIRE book to English
#               BEFORE anyone reads it. The reader gets the English copy.
#               (Swift, C, Go, Rust — they produce a binary before you run it)
#
#   Interpreted → Hire a live translator who sits with the reader and
#                 translates each sentence ON THE SPOT as they read it.
#                 (Python, Ruby, JavaScript — the interpreter runs your source
#                 code directly, no pre-compilation needed)
#
# The tradeoff: compiled languages are generally faster at runtime; interpreted
# languages have a faster "write → run" cycle, which makes them great for
# web apps, scripts, data analysis, and prototyping.
#
# =============================================================================

# ---------------------------------------------------------------------------
# IMPORTS — loading the libraries we need
# ---------------------------------------------------------------------------
# The `import` statement loads a Python module (a library of pre-written code)
# into our program. Think of it like: "hey Python, go find this toolkit and
# bring it into my workspace so I can use its tools."

# Flask is a lightweight web framework. It turns this Python file into a web
# server that can receive HTTP requests (from browsers) and send back responses
# (HTML pages, JSON data, etc.). "Micro framework" means it gives you just the
# essentials with no magic — you stay in control of everything.
from flask import Flask, render_template, request, jsonify

# Our own module (supabase_client.py in the same folder). We import the
# already-configured `supabase` client from it so we can call the database.
from supabase_client import supabase

# ---------------------------------------------------------------------------
# CREATE THE FLASK APPLICATION
# ---------------------------------------------------------------------------
# Flask(__name__) creates a new Flask "application object." The __name__
# argument tells Flask what the root package of our app is — Flask uses it
# to find template files, static files, etc. When you run this file directly,
# __name__ equals the string "__main__".
#
# WHAT IS AN OBJECT?
# ------------------
# An object is a bundle of data + behavior (methods) living in memory. Here,
# `app` is a Flask object that knows how to start a server, register URL
# routes, and handle requests. We call its methods (like @app.route) to
# configure it.
app = Flask(__name__)

# ---------------------------------------------------------------------------
# DATA — CLUBS and CATEGORIES
# ---------------------------------------------------------------------------
#
# WHAT IS A LIST?
# ---------------
# A list is an ordered, changeable collection of items. You write it with
# square brackets: [item1, item2, item3]. Lists can hold anything — numbers,
# strings, other lists, dictionaries, etc.
# You access items by their index (position), starting at 0:
#   CLUBS[0]  → the first club
#   CLUBS[-1] → the last club
#
# WHAT IS A DICTIONARY (dict)?
# ----------------------------
# A dictionary maps keys to values — like a real dictionary maps words to
# definitions. You write it with curly braces: {"key": value, "key2": value2}.
# You look up values by their key:
#   club["name"]  → the club's name string
#   club["id"]    → the club's numeric ID
#
# Below, CLUBS is a LIST of DICTS — a list where every item is a dictionary
# describing one gym location.
# ---------------------------------------------------------------------------

# All 36 NYC Equinox locations with their database IDs and neighborhoods.
# These IDs must match the `id` column in the Supabase `clubs` table.
CLUBS = [
    {"id": 110, "name": "Wall Street",        "neighborhood": "Downtown & Tribeca", "lat": 40.7074, "lng": -74.0113},
    {"id": 128, "name": "Brookfield Place",   "neighborhood": "Downtown & Tribeca", "lat": 40.7136, "lng": -74.0150},
    {"id": 111, "name": "Tribeca",            "neighborhood": "Downtown & Tribeca", "lat": 40.7163, "lng": -74.0086},
    {"id": 122, "name": "Orchard Street",     "neighborhood": "LES & SoHo",         "lat": 40.7194, "lng": -73.9884},
    {"id": 114, "name": "SoHo",               "neighborhood": "LES & SoHo",         "lat": 40.7230, "lng": -73.9997},
    {"id": 135, "name": "Bond Street",        "neighborhood": "LES & SoHo",         "lat": 40.7264, "lng": -73.9924},
    {"id": 124, "name": "Printing House",     "neighborhood": "West Village & Chelsea", "lat": 40.7262, "lng": -74.0081},
    {"id": 162, "name": "Hudson Square",      "neighborhood": "West Village & Chelsea", "lat": 40.7278, "lng": -74.0072},
    {"id": 112, "name": "Greenwich Avenue",   "neighborhood": "West Village & Chelsea", "lat": 40.7350, "lng": -74.0021},
    {"id": 116, "name": "High Line",          "neighborhood": "West Village & Chelsea", "lat": 40.7484, "lng": -74.0048},
    {"id": 102, "name": "Flatiron",           "neighborhood": "Flatiron & Nomad",    "lat": 40.7393, "lng": -73.9908},
    {"id": 136, "name": "Gramercy",           "neighborhood": "Flatiron & Nomad",    "lat": 40.7385, "lng": -73.9840},
    {"id": 160, "name": "Nomad",              "neighborhood": "Flatiron & Nomad",    "lat": 40.7448, "lng": -73.9882},
    {"id": 138, "name": "Hudson Yards",       "neighborhood": "Hudson Yards",        "lat": 40.7540, "lng": -74.0009},
    {"id": 127, "name": "Bryant Park",        "neighborhood": "Midtown South",       "lat": 40.7540, "lng": -73.9836},
    {"id": 108, "name": "East 43rd Street",   "neighborhood": "Midtown South",       "lat": 40.7521, "lng": -73.9754},
    {"id": 109, "name": "East 44th Street",   "neighborhood": "Midtown South",       "lat": 40.7536, "lng": -73.9739},
    {"id": 126, "name": "Rockefeller Center", "neighborhood": "Midtown South",       "lat": 40.7587, "lng": -73.9787},
    {"id": 133, "name": "East 53rd Street",   "neighborhood": "Midtown East",        "lat": 40.7591, "lng": -73.9736},
    {"id": 106, "name": "East 54th Street",   "neighborhood": "Midtown East",        "lat": 40.7593, "lng": -73.9716},
    {"id": 115, "name": "Park Avenue",        "neighborhood": "Midtown East",        "lat": 40.7605, "lng": -73.9726},
    {"id": 139, "name": "E Madison Avenue",   "neighborhood": "Midtown East",        "lat": 40.7640, "lng": -73.9721},
    {"id": 107, "name": "West 50th Street",   "neighborhood": "Midtown West",        "lat": 40.7616, "lng": -73.9866},
    {"id": 113, "name": "Columbus Circle",    "neighborhood": "Midtown West",        "lat": 40.7680, "lng": -73.9819},
    {"id": 132, "name": "East 61st Street",   "neighborhood": "Upper East Side",     "lat": 40.7629, "lng": -73.9660},
    {"id": 105, "name": "East 63rd Street",   "neighborhood": "Upper East Side",     "lat": 40.7648, "lng": -73.9649},
    {"id": 117, "name": "East 74th Street",   "neighborhood": "Upper East Side",     "lat": 40.7732, "lng": -73.9561},
    {"id": 104, "name": "East 85th Street",   "neighborhood": "Upper East Side",     "lat": 40.7780, "lng": -73.9547},
    {"id": 129, "name": "East 92nd Street",   "neighborhood": "Upper East Side",     "lat": 40.7815, "lng": -73.9502},
    {"id": 131, "name": "Sports Club NY",     "neighborhood": "Upper West Side",     "lat": 40.7650, "lng": -73.9820},
    {"id": 121, "name": "West 76th Street",   "neighborhood": "Upper West Side",     "lat": 40.7818, "lng": -73.9803},
    {"id": 103, "name": "West 92nd Street",   "neighborhood": "Upper West Side",     "lat": 40.7873, "lng": -73.9742},
    {"id": 130, "name": "Brooklyn Heights",   "neighborhood": "Brooklyn",            "lat": 40.6936, "lng": -73.9926},
    {"id": 134, "name": "DUMBO",              "neighborhood": "Brooklyn",            "lat": 40.7034, "lng": -73.9892},
    {"id": 161, "name": "Domino",             "neighborhood": "Brooklyn",            "lat": 40.7134, "lng": -73.9647},
    {"id": 137, "name": "Williamsburg",       "neighborhood": "Brooklyn",            "lat": 40.7081, "lng": -73.9571},
]

# All supported class category values. These match what the `category` column
# in the Supabase `classes` table stores. "any" is a special UI value meaning
# "don't filter by category."
CATEGORIES = [
    # Each item is a (group_name, [list of options]) tuple.
    # The template does: {% for group_name, opts in categories %}
    # then: {% for cat in opts %} using cat.v and cat.l
    ("BARRE", [
        {"v": "barre-all",  "l": "Any Barre"},
        {"v": "true-barre", "l": "True Barre"},
        {"v": "figure4",    "l": "Figure 4 (PURE)"},
        {"v": "pilates",    "l": "Any Pilates"},
    ]),
    ("SCULPT & STRENGTH", [
        {"v": "sculpt-all", "l": "Any Sculpt / Strength"},
        {"v": "sculpt",     "l": "Sculpt"},
        {"v": "hiit",       "l": "HIIT / MetCon / Tabata"},
        {"v": "strength",   "l": "Pure Strength"},
    ]),
    ("CARDIO", [
        {"v": "cardio-all", "l": "Any Cardio"},
        {"v": "cycling",    "l": "Cycling / Ride"},
        {"v": "running",    "l": "Running / Tread"},
        {"v": "boxing",     "l": "Boxing / Kickboxing"},
        {"v": "dance",      "l": "Dance"},
    ]),
    ("YOGA & MIND-BODY", [
        {"v": "yoga-all",   "l": "Any Yoga"},
        {"v": "yoga",       "l": "Yoga"},
        {"v": "stretch",    "l": "Stretch / Recovery"},
        {"v": "meditation", "l": "Meditation"},
    ]),
    ("AQUATICS", [
        {"v": "swim",       "l": "Swim / Aqua"},
    ]),
    ("WILDCARD", [
        {"v": "any",        "l": "Any Class"},
    ]),
]

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------
#
# WHAT IS A ROUTE?
# ----------------
# A route is a mapping between a URL path and a Python function. When a browser
# visits http://localhost:5000/something, Flask looks through all registered
# routes to find one whose path matches "/something", then calls the function
# attached to that route and sends the function's return value back to the
# browser as an HTTP response.
#
# Routes are registered using the @app.route() decorator. A decorator is
# a special Python syntax that wraps one function with another. Here:
#
#   @app.route("/")
#   def index():
#       ...
#
# ...is equivalent to saying: "Flask, whenever someone requests '/', call
# my `index` function and return what it returns."
#
# WHAT IS A DECORATOR?
# ---------------------
# A decorator starts with @. It sits directly above a function definition and
# modifies or registers that function. @app.route("/") calls app.route("/")
# and passes our `index` function to it, which registers the URL mapping.
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """
    WHAT IS A DOCSTRING?
    ---------------------
    The triple-quoted string right below a function definition is called a
    docstring. It's a built-in way to document what the function does. Python
    tools, IDEs, and the `help()` command all display docstrings automatically.

    This route handles GET requests to "/" — the home page.
    It renders the index.html template and passes two pieces of data to it:
    - clubs: the full list of gym locations
    - categories: the full list of class categories
    """

    # render_template() reads templates/index.html, processes any Jinja2
    # template tags ({% for %}, {{ variable }}, etc.), and returns the
    # resulting HTML string.
    #
    # The keyword arguments after the filename become variables available
    # inside the template. So `clubs=CLUBS` means the template can use
    # {{ clubs }} or {% for club in clubs %}.
    return render_template("index.html", clubs=CLUBS, categories=CATEGORIES)



@app.route("/clubs")
def clubs():
    """Serve the club directory page."""
    return render_template("clubs.html")

@app.route("/api/doubles", methods=["POST"])
def api_doubles():
    """
    This route handles POST requests to "/api/doubles".
    It receives search parameters as JSON from the browser's fetch() call,
    queries Supabase, and returns results as JSON.

    WHAT IS POST vs GET?
    ---------------------
    HTTP has several "methods" (also called verbs) that describe the intent
    of a request:

      GET  → "give me a resource" (read-only, parameters in the URL)
      POST → "here's data for you to process" (write/submit, data in the body)

    Our search form sends a POST request with a JSON body containing the
    search parameters. Flask reads that body and passes it to Supabase.

    WHAT IS JSON?
    -------------
    JSON (JavaScript Object Notation) is a text format for representing
    structured data. It looks like Python dicts and lists:
      {"name": "Alice", "scores": [10, 20, 30]}
    It's the universal language of web APIs — browsers and servers pass data
    back and forth as JSON strings.
    """

    # ---------------------------------------------------------------------------
    # WHAT IS try/except?
    # --------------------
    # Errors in Python are called "exceptions." If a line of code fails (e.g.,
    # the database is unreachable, the input is malformed), Python raises an
    # exception. Without handling it, the whole program crashes.
    #
    # try/except lets you "catch" exceptions and decide what to do instead:
    #
    #   try:
    #       <code that might fail>
    #   except SomeErrorType as e:
    #       <what to do if that error happens>
    #
    # `Exception` (capital E) is the base class for almost all Python errors —
    # using it catches everything. `as e` binds the error object to the name `e`
    # so we can read its message with str(e).
    # ---------------------------------------------------------------------------
    try:
        # request.get_json() parses the body of the incoming POST request
        # as JSON and returns a Python dict. If parsing fails, it returns None.
        body = request.get_json()

        # ---------------------------------------------------------------------------
        # WHAT IS .get() ON A DICT?
        # --------------------------
        # dict.get("key", default) looks up "key" in the dictionary. If the key
        # doesn't exist, it returns `default` instead of raising a KeyError.
        # This is safer than body["key"] which would crash if "key" is missing.
        #
        # WHAT IS A LIST COMPREHENSION?
        # ------------------------------
        # [expression for item in iterable] is a compact way to build a list.
        # For example:
        #   [x * 2 for x in [1, 2, 3]]  →  [2, 4, 6]
        #
        # Below we use one to convert each item in club_ids to an int,
        # because JSON numbers sometimes arrive as strings depending on the
        # client sending them.
        # ---------------------------------------------------------------------------

        # Read each parameter from the JSON body with sensible defaults.
        club_ids   = [int(x) for x in body.get("club_ids", [])]
        day        = body.get("day", "MONDAY")
        cat1       = body.get("cat1", "any")
        cat2       = body.get("cat2", "any")
        max_gap    = int(body.get("max_gap", 30))
        pair_order = body.get("pair_order", "either")
        win_start  = int(body.get("win_start", 300))
        win_end    = int(body.get("win_end", 1380))

        # Build the parameter dict for the Postgres function.
        # WHAT IS A DICT LITERAL?
        # ------------------------
        # {key: value, ...} creates a new dictionary right here inline.
        # These keys must exactly match the parameter names the Postgres
        # function `find_doubles` expects.
        params = {
            "p_club_ids":   club_ids,
            "p_day":        day,
            "p_cat1":       cat1,
            "p_cat2":       cat2,
            "p_max_gap":    max_gap,
            "p_pair_order": pair_order,
            "p_win_start":  win_start,
            "p_win_end":    win_end,
        }

        # Call the Supabase RPC (Remote Procedure Call) — this executes the
        # Postgres function `find_doubles` on the database server with our
        # params. .execute() actually sends the HTTP request to Supabase and
        # waits for the response. The result lives in response.data.
        response = supabase.rpc("find_doubles", params).execute()

        # ---------------------------------------------------------------------------
        # WHAT IS jsonify()?
        # -------------------
        # jsonify() is a Flask helper that:
        #   1. Converts a Python dict (or list) into a JSON string
        #   2. Wraps it in an HTTP response with Content-Type: application/json
        # The browser's fetch() call will receive this JSON and parse it back
        # into a JavaScript object.
        # ---------------------------------------------------------------------------

        # Return the results. response.data is a list of dicts — each dict is
        # one "double" (a pair of back-to-back classes). We wrap it in our own
        # dict so the browser can check `data.results` and `data.count`.
        return jsonify({
            "results": response.data,   # list of result rows
            "count":   len(response.data),  # len() returns the length of a list
        })

    except Exception as e:
        # Something went wrong. Return a JSON error response with HTTP status
        # code 500 (Internal Server Error). The second argument to jsonify()
        # when used as a tuple with an int is the HTTP status code.
        #
        # WHAT IS AN F-STRING?
        # ---------------------
        # f"text {variable}" is an f-string (formatted string literal). The f
        # before the opening quote tells Python to evaluate anything inside {}
        # and insert the result into the string. So f"Error: {str(e)}" becomes
        # "Error: connection refused" (or whatever the error says).
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
#
# WHAT IS if __name__ == "__main__"?
# ------------------------------------
# Every Python file has a special built-in variable called __name__.
#
#   - When you run a file DIRECTLY (`python app.py`), Python sets
#     __name__ = "__main__" for that file.
#
#   - When a file is IMPORTED by another file (`from app import ...`),
#     Python sets __name__ = "app" (the module's own name) instead.
#
# This guard means: "only start the web server if this file is run directly,
# not if it's imported as a module by something else." Without this guard,
# importing anything from app.py would accidentally start a web server!
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=True enables two Flask superpowers during development:
    #   1. Auto-reload: Flask watches your .py files and restarts the server
    #      automatically whenever you save a change. No need to Ctrl-C and
    #      re-run manually.
    #   2. Debugger: If your code raises an exception, Flask shows a detailed
    #      error page in the browser instead of a blank 500 error.
    # NEVER use debug=True in production — it's a security risk!
    app.run(debug=True)
